import argparse
from pathlib import Path
from src.config import AppConfig, load_config
from src.context import TaskContext
from src.task import TaskPlan

def archive_existing_logs(log_dir: str = "logs"):
    dir_path = Path(log_dir)
    if not dir_path.exists():
        return
    for log_file in dir_path.glob("*.log"):
        if log_file.is_file():
            epoch = int(log_file.stat().st_mtime)
            new_name = f"{log_file.name}_{epoch}"
            new_file_path = log_file.with_name(new_name)
            log_file.rename(new_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="dali")
    parser.add_argument(
        "-c", "--config",
        type=str,
        required=False,
        help="Path to the configure file"
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        required=False,
        help="User query"
    )
    parser.add_argument(
        "-d", "--data",
        type=str,
        required=False,
        help="Path to the data file"
    )
    config_file = "default.toml"
    args = parser.parse_args()
    if args.config:
        config_file = args.config
    config = load_config(config_file)
    log_dir = f"{config.sandbox.output_dir}/logs"
    archive_existing_logs(log_dir)
    config.sandbox.log_dir = log_dir
    context = TaskContext.init_context(config)
    if args.data:
        context.set_data_file(args.data)
    if args.query:
        context.set_user_query(args.query)
    if not context.user_query_:
        raise ValueError("No query")
    task = TaskPlan(context)
    rv = task.run()
    print(rv)
