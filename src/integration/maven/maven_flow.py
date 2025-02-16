from src.integration.maven.maven_client import mvn_update_project
from src.utils.logger_setup import global_logger as logger
from src.utils.logger_setup import log_with_project as project_logger


def mvn_quick_update_flow(project_path):
    success, output = mvn_update_project(project_path)
    if not success:
        project_logger(f"Maven update project failed: {output}", project_path, level="error")
        return False
    project_logger(f"Maven update project succeeded: {output}", project_path, level="debug")
    return True
    
def mvn_full_update_flow(project_path):
        project_logger("Mvn Full update flow not implemented yet", project_path)
        return