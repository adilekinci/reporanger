import shlex
import subprocess
from typing import Tuple
from src.config.settings_reader import get_config
from src.utils.logger_setup import global_logger as logger
from src.utils.logger_setup import log_with_project as project_logger


def run_command(command, cwd)-> Tuple[bool, str]:
    """
    Function to safely run a subprocess.
    command: A string like "mvn versions:update-properties"
    cwd: The directory where the command will be executed
    return: (bool, str) -> (Success, stdout/stderr)
    """
    try:
        command_args = shlex.split(command)
        project_logger(f"Running command: {command}", cwd,level="debug")

        result = subprocess.run(
            command_args, 
            cwd=cwd, 
            capture_output=True, 
            shell=True,
            text=True
        )

        if result.returncode != 0:
            project_logger(
                f"Command failed (code={result.returncode}): {result.stderr}",
                cwd,
                level="error"
            )
            return False, result.stderr
        else:
            project_logger(f"Command finished: {command}", cwd, level="debug")
            return True, result.stdout

    except FileNotFoundError as e:
        project_logger(f"command not found: {e}", cwd, level="error")
        return False, str(e)
    except Exception as e:
        project_logger(f"Unexpected error while running command: {e}", cwd, level="error")
        return False, str(e)


def mvn_springboot_start(tui_app, project_path):
    project_logger(f"Starting Spring Boot application...", project_path)
    profile = get_config("spring_profile", "local")

    # Process başlatılıyor
    process = subprocess.Popen(
        shlex.split(f"mvn spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active={profile}"),
        cwd=project_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        shell=True
    )

    # Process referansını ve PID’yi kaydet
    tui_app.process = process
    
    tui_app._project_started(project_path, process.pid)
    project_name = None

    # Logları UI'ya yazdır
    for line in iter(process.stdout.readline, ''):
        if tui_app.process is None:
            break
        tui_app.call_from_thread(tui_app._append_log_line, line)

    # Process bittiğinde dictionary'den kaldır
    if project_name:
        del tui_app.running_projects[project_name]

    tui_app.call_from_thread(
        tui_app._append_log_line,
        "\n--- Spring Boot process finished ---\n"
    )

    tui_app.process = None


def mvn_update_plugins(project_path) -> Tuple[bool, str]:
    return run_command("mvn versions:display-plugin-updates", project_path)

def mvn_update_project(project_path) -> Tuple[bool, str]:
    project_logger("Maven update project started", project_path)
    return run_command("mvn versions:update-properties versions:update-parent versions:use-latest-versions versions:display-plugin-updates -Dversions.onlyReleases=true", project_path)

def mvn_test(project_path) -> Tuple[bool, str]:
    project_logger("Maven test started", project_path)
    return run_command("mvn clean test", project_path)

def mvn_package(project_path) -> Tuple[bool, str]:
    project_logger("Maven package started", project_path)
    return run_command("mvn clean package", project_path)

def mvn_update_parent_only_releases(project_path) -> Tuple[bool, str]:
    project_logger("Maven update parent only releases started", project_path)
    return run_command("mvn versions:update-parent -Dversions.onlyReleases=true", project_path)

def mvn_use_latest_versions_only_releases(project_path) -> Tuple[bool, str]:
    project_logger("Maven use latest versions only releases started", project_path)
    return run_command("mvn versions:use-latest-versions -Dversions.onlyReleases=true", project_path)

def mvn_update_properties_only_releases(project_path) -> Tuple[bool, str]:
    project_logger("Maven update properties only releases started", project_path)
    return run_command("mvn versions:update-properties -Dversions.onlyReleases=true", project_path)

# 
# def mvn_update_properties(project_path):
#     command = _load_commands().get("mvn_version_update_properties")
#     if command:
#         return run_command(command, project_path)
#     else:
#         logger.error("Maven update properties command not found in commands.json")