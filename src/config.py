from pydantic import BaseModel, Field
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # Python <= 3.10

class LLMConfig(BaseModel):
    max_rounds: int = Field(8, ge=1, le=50)
    max_retry: int = Field(8, ge=1, le=50)
    max_token_cost: float = Field(0.5, ge=0)
    max_tokens: int = Field(16, ge=2048, le=8192)
    max_stdout: int = Field(16, ge=1024, le=8192)
    model: str = "gpt-4o-mini"
    coding_model: str = "gpt-4o-mini"
    temperature: float = Field(0.0, ge=0)

class SandboxConfig(BaseModel):
    timeout: int = Field(8, ge=10, le=3600)
    runtime: str = "sandbox"
    output_dir: str = ""
    user_query: str = ""
    data_file: str = ""
    refactory: str = "N"
    log_dir: str = "logs"

class AppConfig(BaseModel):
    llm: LLMConfig
    sandbox: SandboxConfig

def load_config(path: str) -> AppConfig:
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return AppConfig(**raw)
