import json
import shlex
import subprocess
import os
import re
from collections import defaultdict
from src.utils.logger_setup import global_logger as logger
from src.utils.logger_setup import log_with_project as project_logger




def has_dependency_conflict(project_path):
    """
    Checks for dependency conflicts in the specified Maven project.
    
    Args:
        project_path (str): The directory where the Maven project is located.
    
    Returns:
        bool: Returns True if there are no conflicts, False otherwise.
    """
    project_logger(f"⏳ Checking dependencies in project: {project_path}", project_path)

    try:
        command_args = shlex.split("mvn dependency:tree -DoutputType=json")
        project_logger(f"Running command: {command_args}", project_path,level="debug")

        result = subprocess.run(
            command_args, 
            cwd=project_path, 
            capture_output=True, 
            shell=True,
            text=True
        )

        if result.returncode != 0:
            project_logger(
                f"Command failed (code={result.returncode}): {result.stderr}",
                project_path,
                level="error"
            )   
            return False, result.stderr

    except FileNotFoundError as e:
        project_logger(f"command not found: {e}", project_path, level="error")
        return False, str(e)
    except Exception as e:
        project_logger(f"Unexpected error while running command: {e}", project_path, level="error")
        return False, str(e)

    try:
        project_logger(f"⏳ Loading json data: {project_path}", project_path, level="debug")
        conflicts = parse_dependency_tree(result.stdout)
        project_logger(f"⏳ Loaded json data", project_path, level="debug")

    except ValueError as e:
        project_logger(f"❌ {e}",project_path, level="error")
        return False

    if conflicts:
        project_logger("🚨 Dependency version conflicts detected!",project_path)
        for dep, versions in conflicts.items():
            project_logger(f"🔴 {dep} has multiple versions: {', '.join(versions)}", project_path)
        return False

    project_logger("✅ No dependency conflicts detected.", project_path)
    return True



def parse_dependency_tree(output):
    try:
        # Extract JSON part from the output
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        json_output = output[json_start:json_end]

        logger.debug(f"Extracted JSON: {json_output}")

        # Remove [INFO] prefixes
        json_output = re.sub(r'\[INFO\]\s*', '', json_output)

        logger.debug(f"Preprocessed JSON: {json_output}")

        # Preprocess the JSON output to ensure all keys are properly quoted
        json_output = re.sub(r'([a-zA-Z_][a-zA-Z0-9_-]*)\s*:', r'"\1":', json_output)

        logger.debug(f"Preprocessed JSON: {json_output}")

        dependency_data = json.loads(json_output)
        dependency_versions = defaultdict(set)

        for dependency in dependency_data.get("dependencies", []):
            group_artifact = f"{dependency['groupId']}:{dependency['artifactId']}"
            version = dependency["version"]
            dependency_versions[group_artifact].add(version)

        conflicts = {dep: versions for dep, versions in dependency_versions.items() if len(versions) > 1}

        return conflicts
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing Maven output as JSON: {e}")
        raise ValueError(f"Error parsing Maven output as JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise ValueError(f"Unexpected error: {e}")

