import os
import signal
from src.config.settings_reader import get_config
from src.utils.logger_setup import log_with_project as project_logger



def open_project_in_vscode(project_path):
    editor = get_config("editor", "code")
    os.system(f'{editor} "{project_path}"')


def kill_process(pid, project_name):
    try:
        os.kill(pid, signal.SIGTERM)
        project_logger(f"Project with Process {pid} terminated.", project_name)
        return True;
    except ProcessLookupError:
        project_logger(f"Project with Process {pid} not found.", project_name)
        return False;
