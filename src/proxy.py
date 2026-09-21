import os
from together import Together
from src.config import AppConfig, LLMConfig
from src.logger import get_logger
from src.sandbox import PersistentSandbox

class ExecutionResult:
    def __init__(self, status, outputs, error_message) -> None:
        self.status_ = status
        self.outputs_ = outputs
        self.error_message_ = error_message

class LLMProxy:
    def __init__(self, config: AppConfig) -> None:
        self.llm_config_ = config.llm
        self.sandbox_config_ = config.sandbox
        self.client_ = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
        self.sandbox_ = PersistentSandbox(self.sandbox_config_.timeout, self.sandbox_config_.runtime, self.sandbox_config_.output_dir)
        self.logger_ = get_logger("proxy", config.sandbox.log_dir)

    def close(self):
        if self.sandbox_:
            self.sandbox_.close()

    def chat(self, messages: list[dict], model: str) -> str:
        response = self.client_.chat.completions.create(
            model = model,
            messages = messages,
            max_tokens = self.llm_config_.max_tokens,
            temperature = self.llm_config_.temperature,
            stream=False)
        self.logger_.info(f"LLM chat response: {response}")
        if response.choices[0].message.reasoning:
            self.logger_.info(f"LLM reasoning:\n{response.choices[0].message.reasoning}")
        return response.choices[0].message.content

    def run_python(self, code: str) -> ExecutionResult:
        try:
            response = self.sandbox_.run(code)
            self.logger_.info(f"LLM execute response: {response}")
            if response['stderr']:
                return ExecutionResult("error", response['stdout'], response['stderr'])
            elif response['exception'] != 'None':
                return ExecutionResult("error", response['stdout'], response['exception'])
            else:
                if len(response['stdout']) > self.llm_config_.max_stdout:
                    return ExecutionResult("success", f"First {self.llm_config_.max_stdout} characters of execution output: " + response['stdout'][:self.llm_config_.max_stdout], "")
                else:
                    return ExecutionResult("success", response['stdout'], "")
        except Exception as e:
            return ExecutionResult("exception", "", str(e))
