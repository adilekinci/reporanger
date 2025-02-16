from src.integration.git.git_flows import git_flow_finish, git_flow_start
from src.integration.maven.maven_conflict_checker import has_dependency_conflict
from src.integration.maven.maven_flow import mvn_quick_update_flow
from src.utils.logger_setup import global_logger as logger
from src.utils.logger_setup import log_with_project as project_logger



def full_update_run_push_flow(project_path):
    
    logger.info(f"git flow starts for {project_path}")
    git_flow_start(project_path)
    logger.info(f"maven flow starts for {project_path}")
    #mvn_update_properties(project_path)
    #mvn_update_parent(project_path)
    #mvn_run_tests(project_path)
    #mvn_build_project(project_path)
    logger.info(f"git flow pushes for {project_path}")
    git_flow_finish(project_path)


def quick_update_flow(project_path):
    project_logger("Git Flow quick update starting...", project_path)
    if not git_flow_start(project_path):
        project_logger(f"Git Flow start failed for {project_path}", project_path)
        return False
    project_logger("Maven Flow quick update starting...", project_path)
    mvn_quick_update_flow(project_path)
    isNoConflict = has_dependency_conflict(project_path)
    if not isNoConflict:
        project_logger(f"Conflicht Info for {project_path}", project_logger)
        return False
    project_logger("Git Flow quick update finishing...", project_path)
    git_flow_finish(project_path)
    project_logger("Git Flow quick update finishing...", project_path)

    return True
