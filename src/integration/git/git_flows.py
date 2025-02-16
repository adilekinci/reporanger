from src.integration.git.git_client import checkout_main_branch, create_and_checkout_new_branch, has_changes, stash_uncommitted_changes, git_add_and_commit, git_push_changes, has_changes
from src.utils.logger_setup import global_logger as logger
from src.utils.logger_setup import log_with_project as project_logger
from src.config.settings_reader import get_config



def git_flow_start(repo_path):
    # Path to the git repository; update this to your actual repository path
    project_logger("Git Flow Starts", repo_path)
    if not repo_path:
        project_logger("Error: repo_path is empty", repo_path, level="error")
        return
    # 1. Clean up existing changes
    changes_cleaned_up = stash_uncommitted_changes(repo_path)
    if not changes_cleaned_up:
        return

    # 2. Checkout main branch
    success, main_branch = checkout_main_branch(repo_path)
    if not success:
        return
    
    # 3. Create a new branch from master
    return create_and_checkout_new_branch(repo_path)


def git_flow_finish(repo_path):
    if not repo_path:
        project_logger("Error: repo_path is empty", repo_path, level="error")
        return

    # Check if there are uncommitted changes
    if has_changes(repo_path):
        if not git_add_and_commit(repo_path):
            project_logger("Error: Failed to add and commit changes", repo_path, level="error")
            return

        # Check if pushing to remote is enabled in settings
        send_to_remote = get_config("send_to_remote", False)
        if send_to_remote:
            # Push changes to the remote repository
            if not git_push_changes(repo_path):
                project_logger("Error: Failed to push changes", repo_path, level="error")
                return
    else:
        project_logger("There are no changes", repo_path)

    project_logger("Git flow finish completed successfully", repo_path)