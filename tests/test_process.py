import unittest
from unittest.mock import patch
from src.processor.process import quick_update_flow

class TestProcessFlows(unittest.TestCase):

    @patch('src.processor.process.git_flow_start')
    @patch('src.processor.process.git_flow_finish')
    @patch('src.processor.process.mvn_quick_update_flow')
    @patch('src.processor.process.has_dependency_conflict')
    def test_quick_update_flow(self, mock_has_dependency_conflict, mock_mvn_quick_update_flow, mock_git_flow_finish, mock_git_flow_start):
        project_path = '/path/to/project'

        # Test case where there is no dependency conflict
        mock_has_dependency_conflict.return_value = True
        result = quick_update_flow(project_path)
        self.assertTrue(result)
        mock_git_flow_start.assert_called_once_with(project_path)
        mock_mvn_quick_update_flow.assert_called_once_with(project_path)
        mock_git_flow_finish.assert_called_once_with(project_path)

        # Test case where there is a dependency conflict
        mock_has_dependency_conflict.return_value = False
        result = quick_update_flow(project_path)
        self.assertFalse(result)
        self.assertEqual(mock_git_flow_start.call_count, 2)
        self.assertEqual(mock_mvn_quick_update_flow.call_count, 2)
        self.assertEqual(mock_git_flow_finish.call_count, 1)

if __name__ == '__main__':
    unittest.main()
