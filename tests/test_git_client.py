import unittest
from unittest.mock import patch, MagicMock
from src.integration.git.git_client import run_git_command, stash_uncommitted_changes, checkout_main_branch, create_and_checkout_new_branch, has_changes, git_add_and_commit, git_push_changes

class TestGitClient(unittest.TestCase):

    @patch('src.integration.git.git_client.run_git_command')
    def test_stash_uncommitted_changes(self, mock_run_git_command):
        mock_run_git_command.side_effect = [
            (0, ' M modified_file.txt'),  # git status --porcelain
            (0, 'Stashed changes'),       # git stash
        ]
        result = stash_uncommitted_changes('/path/to/repo')
        self.assertTrue(result)
        self.assertEqual(mock_run_git_command.call_count, 2)

    @patch('src.integration.git.git_client.run_git_command')
    def test_checkout_main_branch(self, mock_run_git_command):
        mock_run_git_command.side_effect = [
            (0, '  origin/master'),  # git branch -r
            (0, 'Switched to branch master')  # git checkout master
        ]
        result, branch = checkout_main_branch('/path/to/repo')
        self.assertTrue(result)
        self.assertEqual(branch, 'master')
        self.assertEqual(mock_run_git_command.call_count, 2)

    @patch('src.integration.git.git_client.run_git_command')
    def test_create_and_checkout_new_branch(self, mock_run_git_command):
        mock_run_git_command.return_value = (0, 'Switched to a new branch')
        result = create_and_checkout_new_branch('/path/to/repo')
        self.assertTrue(result)
        self.assertEqual(mock_run_git_command.call_count, 1)

    @patch('src.integration.git.git_client.run_git_command')
    def test_has_changes(self, mock_run_git_command):
        mock_run_git_command.return_value = (0, ' M modified_file.txt')
        result = has_changes('/path/to/repo')
        self.assertTrue(result)
        self.assertEqual(mock_run_git_command.call_count, 1)

    @patch('src.integration.git.git_client.run_git_command')
    def test_git_add_and_commit(self, mock_run_git_command):
        mock_run_git_command.side_effect = [
            (0, ''),  # git add pom.xml
            (0, ' M modified_file.txt'),  # git status --porcelain
            (0, 'Committed changes')  # git commit
        ]
        result = git_add_and_commit('/path/to/repo')
        self.assertTrue(result)
        self.assertEqual(mock_run_git_command.call_count, 3)

    @patch('src.integration.git.git_client.run_git_command')
    def test_git_push_changes(self, mock_run_git_command):
        mock_run_git_command.side_effect = [
            (0, 'current_branch'),  # git rev-parse --abbrev-ref HEAD
            (0, 'Pushed changes')  # git push
        ]
        result = git_push_changes('/path/to/repo')
        self.assertTrue(result)
        self.assertEqual(mock_run_git_command.call_count, 2)

if __name__ == '__main__':
    unittest.main()
