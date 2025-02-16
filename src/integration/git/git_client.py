import shlex
import subprocess
from datetime import datetime
from src.utils.logger_setup import global_logger as logger
from src.utils.logger_setup import log_with_project as project_logger



def run_git_command(repo_path: str, git_command: str) -> tuple[int, str]:
    """
    Executes a Git command within the given Git repository and returns the result.

    Args:
        repo_path (str): Path to the Git repository.
        git_command (str): Git command to execute (e.g., "status --porcelain").

    Returns:
        tuple[int, str]: Returns (exit_code, output).
    """
    try:
        command = ["git"] + git_command.split()
        result = subprocess.run(
            command,
            cwd=repo_path,
            capture_output=True, 
            text=True, 
            check=False
        )

        exit_code = result.returncode
        output = result.stdout.strip() if result.stdout else result.stderr.strip()

        return exit_code, output

    except Exception as e:
        return 1, f"❌ Error executing Git command: {str(e)}"



def stash_uncommitted_changes(repo_path):
     # 1. Check for changes using 'git status --porcelain'
    project_logger("Checking git status for changes...", repo_path)
    status_command = "status --porcelain"
    ret_code, status_output = run_git_command(repo_path, status_command)
    
    # If the status command returns an error
    if ret_code != 0:
        project_logger(f"Error running git status: {status_output}", repo_path, level="error")
        return False

    # If status_output is not empty, it means there are changes
    if status_output:
        project_logger("Changes detected in repository. Stashing changes...", repo_path)
        ret_code, stash_output = run_git_command(repo_path, "stash")
        if ret_code != 0:
            project_logger(f"Error stashing changes: {stash_output}", repo_path, level="error")
            return False
        project_logger("Changes stashed successfully.", repo_path)
    else:
        project_logger("No changes detected. No need to stash.", repo_path)
    return True    
    
def checkout_main_branch(repo_path):
    project_logger("Determining the main branch name...", repo_path)
    ret_code, branch_output = run_git_command(repo_path, "branch -r")
    if ret_code != 0:
        project_logger(f"Error listing remote branches: {branch_output}",repo_path, level="error")
        return False, None

    main_branch = "master" if "origin/master" in branch_output else "main"
    project_logger(f"Main branch determined to be '{main_branch}'", repo_path)
    ret_code, checkout_output = run_git_command(repo_path, f"checkout {main_branch}")
    if ret_code != 0:
        project_logger(f"Error checking out {main_branch} branch: {checkout_output}", repo_path, level="error")
        return False, None
    project_logger(f"Checked out to {main_branch} branch successfully.", repo_path)
    return True, main_branch


def create_and_checkout_new_branch(repo_path):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")

    new_branch_name = f"automated/library_update_{timestamp}"
    project_logger(f"Creating new branch '{new_branch_name}' from master...", repo_path)
    ret_code, branch_output = run_git_command(repo_path, f"checkout -b {new_branch_name}")
    if ret_code != 0:
        project_logger(f"Error creating new branch: {branch_output}", repo_path, level="error")
        return False
    project_logger(f"New branch '{new_branch_name}' created successfully.", repo_path)
    return True


def has_changes(repo_path):
    if not repo_path:
        project_logger("Error: repo_path is empty in has_changes", repo_path, level="error")
        return False

    project_logger("Checking for changes in the repository...", repo_path)
    ret_code, status_output = run_git_command(repo_path, "status --porcelain")
    if ret_code != 0:
        project_logger(f"Error running git status: {status_output}", repo_path, level="error")
        return False

    if status_output:
        project_logger("Changes detected in the repository.", repo_path)
        return True
    else:
        project_logger("No changes detected in the repository.", repo_path)
        return False


def git_add_and_commit(repo_path):
    if not repo_path:
        project_logger("Error: repo_path is empty in git_add_and_commit", repo_path, level="error")
        return False

    # Add changes
    project_logger("Adding changes to staging area...", repo_path)
    ret_code, add_output = run_git_command(repo_path, "add pom.xml")
    if ret_code != 0:
        project_logger(f"Error adding changes: {add_output}", repo_path, level="error")
        return False

    # chek if there is a change
    ret_code, status_output = run_git_command(repo_path, "status --porcelain")
    project_logger(f"Git status output: {status_output}", repo_path)
    if not status_output.strip():
        project_logger("No changes detected. Nothing to commit.", repo_path, level="warning")
        return False

    # Commit changes
    commit_message = "automated_library_updating"
    safe_commit_message = shlex.quote(commit_message)
    project_logger(f"Committing changes with message: '{commit_message}'", repo_path)
    ret_code, commit_output = run_git_command(repo_path, f'commit -m "{safe_commit_message}"')
    if ret_code != 0:
        project_logger(f"Error committing changes: {commit_output}", repo_path, level="error")
        return False

    project_logger("Changes committed successfully.", repo_path)
    return True


def git_push_changes(repo_path):
    if not repo_path:
        project_logger("Error: repo_path is empty in git_push_changes", repo_path, level="error")
        return False

    # Get the current branch name
    project_logger("Getting current branch name...", repo_path)
    ret_code, branch_output = run_git_command(repo_path, "rev-parse --abbrev-ref HEAD")
    if ret_code != 0:
        project_logger(f"Error getting current branch name: {branch_output}", repo_path, level="error")
        return False

    current_branch = branch_output.strip()
    project_logger(f"Current branch is '{current_branch}'", repo_path)

    # Push changes to remote repository with upstream
    project_logger(f"Pushing changes to remote repository for branch '{current_branch}'", repo_path)
    ret_code, push_output = run_git_command(repo_path, f"push --set-upstream origin {current_branch}")
    if ret_code != 0:
        project_logger(f"Error pushing changes: {push_output}", repo_path, level="error")
        return False

    project_logger("Changes pushed to remote repository successfully.", repo_path)
    return True



