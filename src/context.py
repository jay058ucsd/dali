from __future__ import annotations
from typing import List, Dict, Any, Optional
from src.config import AppConfig
from src.proxy import LLMProxy

class TaskContext:

    def __init__(self, config: AppConfig, proxy: LLMProxy, parent: Optional["TaskContext"] = None) -> None:
        self.parent_ = parent
        self.config_ = config
        self.proxy_ = proxy
        self.history_: List[Dict[str, Any]] = []
        if self.parent_ is None:
            self.code_history_ = []
            self.output_history_ = []
        else:
            self.code_history_ = self.parent_.code_history_
            self.output_history_ = self.parent_.output_history_
        self.sub_context_ = None
        self.user_query_ = None
        self.data_file_ = None

    @classmethod
    def init_context(cls, config: AppConfig) -> "TaskContext":
        proxy = LLMProxy(config)
        context = cls(config, proxy)
        if config.sandbox.data_file:
            context.set_data_file(config.sandbox.data_file)
        if config.sandbox.user_query:
            context.set_user_query(config.sandbox.user_query)
        return context
    
    def init_sub_context(self):
        if not self.sub_context_:
            self.sub_context_ = self.clone_context()

    def clear_sub_context(self):
        self.sub_context_ = None

    def clone_context(self) -> "TaskContext":
        task = TaskContext(self.config_, self.proxy_, self)
        task.set_data_file(self.data_file_)
        return task

    def add_record(self, role: str, content: str):
        self.history_.append({"role": role, "content": content})

    def add_code(self, code: str):
        self.code_history_.append(code)

    def add_output(self, message: str):
        self.output_history_.append(message)

    def set_data_file(self, file: str):
        self.data_file_ = file

    def set_user_query(self, query: str):
        self.user_query_ = query
