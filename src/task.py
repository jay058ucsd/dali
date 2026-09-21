import base64
import json
import re
import os
from pydantic import BaseModel
from typing import TypedDict
from langgraph.graph import StateGraph, END
from pathlib import Path

from src.agent import Agent, OutputFormat
from src.config import AppConfig
from src.context import TaskContext
from src.logger import get_logger

class Step(BaseModel):
    id: int
    action: str
    expected_result: str

class TaskPlanState(TypedDict):
    loop_index: int
    llm_output: str
    status: str

class TaskPlan:
    def __init__(self, context: TaskContext) -> None:
        self.task_context_ = context
        self.logger = get_logger("task plan", context.config_.sandbox.log_dir)

    def principle_(self, state: TaskPlanState) -> TaskPlanState:
        print(f"principle: query={self.task_context_.user_query_}")
        self.logger.info(f"In principle_, state: {state}")
        self.task_context_.add_record("user", f"The final goal is: {self.task_context_.user_query_}")
        return {"status": "success"}

    def planner_(self, state: TaskPlanState) -> TaskPlanState:
        self.logger.info(f"loop_index: {state['loop_index']}")
        planner = Agent("system", "planner", "data scientist", self.task_context_, self.task_context_.history_)
        rv = planner.complete_chat()
        data = json.loads(rv)
        if "plan" in data:
            steps = [Step(id = 1, action=data['plan']['action'], expected_result=data['plan']['action'])]
        else:
            steps = [Step(**step) for step in data["steps"]]
        result = "\n".join(json.dumps(step.model_dump()) for step in steps)
        self.logger.info(f"Plan {state['loop_index']} {len(steps)} steps:\n{result}")
        print(f"plan {state['loop_index']} in {len(steps)} steps:\n{result}")
        self.task_context_.init_sub_context()
        for step in steps:
            task = TaskResearch(self.task_context_.sub_context_, step.action, step.expected_result)
            rv = task.run()
            print(f"action: {step.action} - {rv}")
            if (rv == "failed"):
                return {"llm_output": " ".join(str(item) for item in self.task_context_.sub_context_.history_), "status": "failed"}
        return {"llm_output": " ".join(str(item) for item in self.task_context_.sub_context_.history_), "status": "success"}

    def reviewer_(self, state: TaskPlanState) -> TaskPlanState:
        self.logger.info(f"In reviewer_, state: {state}")
        reviewer = Agent("system", "reviewer", "data scientist", self.task_context_, self.task_context_.sub_context_.history_)
        rv = reviewer.complete_chat()
        data = json.loads(rv)
        summary = ' '.join([data['summary'], data['analysis']])
        next_action = data['next_action']['description']
        self.task_context_.add_record("assistant", summary)
        self.task_context_.add_record("user", next_action)
        self.task_context_.clear_sub_context()
        print(f"reviewer:\nsummary:{summary}\nnext action:{next_action}")
        return {"loop_index": state["loop_index"] + 1, "llm_output": '\n'.join([summary, next_action])}

    def finalizer_(self, state: TaskPlanState) -> TaskPlanState:
        self.logger.info(f"In finalizer_, state: {state}")
        file_path = os.path.join(self.task_context_.config_.sandbox.output_dir, "main.py")
        with open(file_path, "w") as f:
            f.write("\n".join(self.task_context_.code_history_))
        file_path = os.path.join(self.task_context_.config_.sandbox.output_dir, "output.txt")
        with open(file_path, "w") as f:
            f.write("###\n")
            f.write("\n###\n".join(self.task_context_.output_history_))
        if self.task_context_.config_.sandbox.refactory.lower() == "y":
            tmp_dir = f"{self.task_context_.config_.sandbox.output_dir}/tmp"
            os.makedirs(tmp_dir, exist_ok=True)
            for output_file in Path(self.task_context_.config_.sandbox.output_dir).glob("*.*"):
                destination = f"{tmp_dir}/{output_file.name}"
                output_file.rename(destination)
            self.task_context_.init_sub_context()
            task = TaskResearch(self.task_context_.sub_context_, "", "Code refactoring successful.")
            rv = task.run()
            if (rv == "success"):
                file_path = os.path.join(self.task_context_.config_.sandbox.output_dir, "main.py")
                with open(file_path, "w") as f:
                    f.write("\n".join(self.task_context_.code_history_))
                file_path = os.path.join(self.task_context_.config_.sandbox.output_dir, "output.txt")
                with open(file_path, "w") as f:
                    f.write("###\n")
                    f.write("\n###\n".join(self.task_context_.output_history_))
            else:
                self.logger.info(f"In finalizer_, Python code refactory failed")
        return {"llm_output": f"{self.task_context_.user_query_} is finished."}

    def reviewer_next_(self, state: TaskPlanState) -> str:
        if state["loop_index"] >= self.task_context_.config_.llm.max_rounds:
            return "finalizer"
        elif state["status"] == "failed":
            return "finalizer"
        else:
            return "planner"

    def run(self) -> str:
        graph = StateGraph(TaskPlanState)
        graph.add_node("principle", self.principle_)
        graph.add_node("planner", self.planner_)
        graph.add_node("reviewer", self.reviewer_)
        graph.add_node("finalizer", self.finalizer_)
        graph.set_entry_point("principle")
        graph.add_edge("principle", "planner")
        graph.add_edge("planner", "reviewer")
        graph.add_conditional_edges("reviewer", self.reviewer_next_)
        graph.add_edge("finalizer", END)
        workflow = graph.compile()
        result = workflow.invoke({"loop_index": 0, "status": "success"}, config={"recursion_limit": 200})
        complete_code = '\n'.join(self.task_context_.code_history_)
        print(f"Code generated:\n{complete_code}")
        print(f"TaskPlan: query={self.task_context_.user_query_}, result={result['status']}")
        return f"Running task: {self.task_context_.user_query_} retruns {result['status']}"

class TaskResearchState(TypedDict):
    retry: int
    code_output: str
    status: str

class TaskResearch:
    def __init__(self, context: TaskContext, query: str, expected_result: str) -> None:
        self.task_context_ = context
        self.query_ = query
        self.logger = get_logger("task research", context.config_.sandbox.log_dir)
        self.expected_result_ = expected_result
        self.development_state_ = len(query) > 0

    def scientist_(self, state: TaskResearchState) -> TaskResearchState:
        self.logger.info(f"In scientist_, state: {state}, query={self.query_}, development_state_={self.development_state_}")
        print(f"scientist: query={self.query_}, development_state_={self.development_state_}")
        if self.development_state_:
            self.task_context_.add_record("user", self.query_)
            scientist = Agent("system", "scientist", "data scientist", self.task_context_, self.task_context_.history_)
            rv = scientist.complete_chat()
            data = json.loads(rv)
            thought = data['thought']
            self.task_context_.add_record('assistant', thought)
        return {"retry": 0, "status": "success"}

    def developer_(self, state: TaskResearchState) -> TaskResearchState:
        self.logger.info(f"In developer_, state: {state}")
        role = "developer" if self.development_state_ else "refactory"
        developer = Agent("system", role, "python bioinformatics developer", self.task_context_, self.task_context_.history_, output_format = OutputFormat.CODE)
        rv = developer.complete_coding()
        while (self.task_context_.history_ and self.task_context_.history_[-1]['role'] == "user" and self.task_context_.history_[-1]['content'].startswith("Failed to ")):
            self.task_context_.history_.pop()
        code = rv.strip()
        if not code:
            print(f"developer generate no code")
        else:
            print(f"developer generate code:\n{code}")
            if not self.development_state_:
                self.task_context_.code_history_.clear()
                self.task_context_.output_history_.clear()
        return {"retry": state["retry"], "code_output": code, "status": "success"}

    def tester_(self, state: TaskResearchState) -> TaskResearchState:
        self.logger.info(f"In tester_, state: {state}")
        if not state["code_output"]:
            output_msg = f"Failed to test empty code output. Please re-generate code."
            self.task_context_.add_record("user", output_msg)
            return {"retry": state["retry"] + 1, "status": "failed"}
        tester = Agent("system", "tester", "python bioinformatics tester", self.task_context_, self.task_context_.history_)
        result = tester.run_python(state["code_output"])
        message = f"execution result: {result.status_}\nOutputs:\n{result.outputs_}"
        if result.error_message_:
            message += f"Error:\n{result.error_message_}"
        self.logger.info(message)
        print(message)
        if result.status_ == "success":
            output = result.outputs_ if result.outputs_ else "output is empty"
            self.task_context_.add_record("user", f"execute code:\n{state['code_output']}\noutput is:\n{output}")
            rv = tester.complete_chat()
            self.task_context_.history_.pop()
            data = json.loads(rv)
            output_result = data['result']
            rationale = data['rationale']
            if output_result == "success":
                self.task_context_.add_code(state["code_output"])
                self.task_context_.add_output(result.outputs_)
                result_msg = f"Achieve the expected results: {self.expected_result_}"
                if result.outputs_:
                    result_msg += f"\nOutputs:\n{result.outputs_}"
                self.task_context_.add_record("user", result_msg)
                return {"retry": 0, "status": "success"}
            else:
                rename_files = self.rename_png_files(output, self.task_context_.config_.sandbox.output_dir)
                if (len(rename_files) > 0):
                    rename_files_list = ','.join(rename_files)
                    self.logger.info(f"renamed following png files: {rename_files_list}, due to: {rationale}")
                output_msg = f"Failed to execute:\n{state['code_output']}\nfailed reason is: {rationale}.\nPlease re-generate code above and fix the error."
                self.task_context_.add_record("user", output_msg)
                return {"retry": state["retry"] + 1, "status": "failed"}
        else:
            output_msg = f"Failed to execute:\n{state['code_output']}\ngot error:\n{result.error_message_}\nPlease re-generate code above and fix the error."
            self.task_context_.add_record("user", output_msg)
            return {"retry": state["retry"] + 1, "status": "failed"}

    def rename_png_files(self, output_text, output_dir):
        target_prefix = "Created png file:"
        png_line = None
        for line in output_text.splitlines():
            if target_prefix in line:
                png_line = line
                break
        if not png_line:
            return []
        file_list_str = png_line.split(target_prefix, 1)[1].strip()
        filenames = [name.strip() for name in file_list_str.split(",") if name.strip()]
        renamed_files = []
        for filename in filenames:
            old_path = os.path.join(output_dir, filename)
            new_filename = f"delete_{filename}"
            new_path = os.path.join(output_dir, new_filename)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                renamed_files.append(new_filename)
        return renamed_files

    def tester_next_(self, state: TaskResearchState) -> str:
        if state["status"] == "failed":
            if state["retry"] >= self.task_context_.config_.llm.max_retry:
                return END
            else:
                return "developer"
        return END

    def run(self) -> str:
        graph = StateGraph(TaskResearchState)
        graph.add_node("scientist", self.scientist_)
        graph.add_node("developer", self.developer_)
        graph.add_node("tester", self.tester_)
        graph.set_entry_point("scientist")
        graph.add_edge("scientist", "developer")
        graph.add_edge("developer", "tester")
        graph.add_conditional_edges("tester", self.tester_next_)
        workflow = graph.compile()
        result = workflow.invoke({"loop_index": 0, "status": "success"}, config={"recursion_limit": 200})
        print(f"TaskResearch: query={self.query_}, result={result['status']}")
        return result["status"]
