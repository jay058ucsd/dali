import re
from enum import Enum

from src.logger import get_logger
from src.prompt import get_prompt
from src.context import TaskContext

class OutputFormat(Enum):
    JSON = "json"
    CODE = "code"
    TEXT = "test"

class Agent:
    def __init__(self, type: str, role: str, description: str, context: TaskContext, chat_history: [], output_format: OutputFormat = OutputFormat.JSON) -> None:
        self.type_ = type
        self.role_ = role
        self.description_ = description
        self.logger_ = get_logger(f"agent {self.role_}", context.config_.sandbox.log_dir)
        self.context_ = context
        self.chat_history_ = chat_history
        self.output_format_ = output_format

    @property
    def prompt(self) -> str:
        return get_prompt(self.role_)

    def extract_json_block(self, text: str) -> str:
        s = text.strip()
        start = s.find("{")
        if start == -1:
            raise ValueError("No '{' found in input")
        end = s.rfind("}")
        if end == -1:
            raise ValueError("No '}' found in input")
        return s[start:end+1]

    def repair_multiline_strings(self, json_text: str) -> str:
        # Find "key": " ... " blocks that contain raw newlines
        pattern = r'("code"\s*:\s*")([\s\S]*?)(")'
        
        def replacer(match):
            start, content, end = match.groups()
            # Escape newlines and quotes inside the content
            escaped = content.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
            return f'{start}{escaped}{end}'
        
        return re.sub(pattern, replacer, json_text)

    def clean_llm_code(self, text: str) -> str:
        lines = text.splitlines()
        while lines and (lines[0].strip() in ("'''", '```', '```python')):
            lines.pop(0)
        while lines and (lines[-1].strip() in ("'''", '```')):
            lines.pop()
        if lines and lines[0].strip() == "python":
            lines.pop(0)
        return "\n".join(lines).strip()

    def complete_chat(self) -> str:
        history = self.chat_history_ + [{"role": self.type_, "content": self.prompt}]
        llm_input = "\n".join(f"{h['role']}: {h['content']}" for h in history)
        self.logger_.info(f"LLM input: {len(history)} records:\n{llm_input}")
        llm_output = self.context_.proxy_.chat(history, self.context_.config_.llm.model)
        self.logger_.info(f"LLM output:\n{llm_output}")
        if self.output_format_ == OutputFormat.JSON:
            return self.extract_json_block(llm_output)
        return llm_output

    def complete_coding(self) -> str:
        current_code = ''
        if len(self.context_.code_history_) > 0:
            current_code = ""
            if self.role_ == "developer":
                current_code = """
            You will be given existing source code. Your job is to generate ONLY:
            - new code that must be added, OR
            - modified versions of existing functions or lines.

            Rules:
            - Do NOT repeat or rewrite any code that already exists in the provided source.
            - Do NOT output the full file.
            - Output ONLY the new or modified code.
            - If no new code is needed, output an empty string.
            Below is the complete code already exists:\n
"""
            else:
                current_code = """
            You will be given existing source code. Your job is to:
            - Refactory the current code, make it more readable, compact and professional.
            - Remove code redundancy.
            - Do not change any functionality.
            Below is the complete code already exists:\n
"""
            current_code += '\n'.join(self.context_.code_history_)
            if self.role_ == "developer":
                current_code += '\nNever repeat existing code above. This is non-negotiable.'
        data_file = ''
        if self.context_.data_file_:
            data_file = f"If you need to load any data, the data file is at: {self.context_.data_file_}"
        prompt = self.prompt.format(current_code=current_code, data_file=data_file)
        history = self.chat_history_ + [{"role": self.type_, "content": prompt}]
        llm_input = "\n".join(f"{h['role']}: {h['content']}" for h in history)
        self.logger_.info(f"LLM input: {len(history)} records:\n{llm_input}")
        self.logger_.info(f"history json:\n{history}")
        llm_output = self.context_.proxy_.chat(history, self.context_.config_.llm.coding_model)
        self.logger_.info(f"LLM output:\n{llm_output}")
        return self.clean_llm_code(llm_output)

    def run_python(self, code: str):
        return self.context_.proxy_.run_python(code)
