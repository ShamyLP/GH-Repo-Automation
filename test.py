import unittest
from unittest.mock import MagicMock, patch
from github import Github
from datetime import datetime, timedelta
import openpyxl
import json
import yaml
from script import get_package_manager, get_dependency_management, get_semantic_release, get_gha, get_workflow_info


class TestLPGitHubRepoAnalysis(unittest.TestCase):

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_package_manager_package_lock(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value = ['file1', 'file2', 'package-lock.json']
        self.assertEqual(get_package_manager(repo), 'Yes (NPM)')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_package_manager_yarn_lock(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value = ['file1', 'file2', 'yarn.lock']
        self.assertEqual(get_package_manager(repo), 'Yes (Yarn)')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_package_manager_no_lock_files(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value = ['file1', 'file2']
        self.assertEqual(get_package_manager(repo), 'No')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_dependency_management_dependabot(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_pulls.return_value.totalCount = 3
        self.assertEqual(get_dependency_management(repo), 'Yes (Dependabot)')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_dependency_management_renovate(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_pulls.return_value.totalCount = 5
        self.assertEqual(get_dependency_management(repo), 'Yes (Renovate)')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_dependency_management_no_management(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_pulls.return_value.totalCount = 0
        self.assertEqual(get_dependency_management(repo), 'No')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_semantic_release_present(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value.decoded_content = json.dumps({"devDependencies": {"semantic-release": "^2.0.0"}}).encode('utf-8')
        self.assertEqual(get_semantic_release(repo), 'Yes')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_semantic_release_not_present(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value.decoded_content = json.dumps({"devDependencies": {"other-package": "^1.0.0"}}).encode('utf-8')
        self.assertEqual(get_semantic_release(repo), 'No')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_semantic_release_invalid_json(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value.decoded_content = "Invalid JSON".encode('utf-8')
        self.assertEqual(get_semantic_release(repo), 'No')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_gha_workflows_used_within_last_year(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        workflow1 = MagicMock()
        workflow1.last_modified = datetime.now() - timedelta(days=100)
        workflow2 = MagicMock()
        workflow2.last_modified = datetime.now() - timedelta(days=200)
        repo.get_contents.return_value = [workflow1, workflow2]
        self.assertEqual(get_gha(repo), 'Yes')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_gha_workflows_not_used_within_last_year(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        workflow1 = MagicMock()
        workflow1.last_modified = datetime.now() - timedelta(days=400)
        workflow2 = MagicMock()
        workflow2.last_modified = datetime.now() - timedelta(days=500)
        repo.get_contents.return_value = [workflow1, workflow2]
        self.assertEqual(get_gha(repo), 'No')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_gha_no_workflows(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value = []
        self.assertEqual(get_gha(repo), 'No')

    @patch('builtins.input', side_effect=["token", "repo_name"])
    def test_get_workflow_info(self, mock_input):
        # Create a mock repository object for testing
        repo = MagicMock()
        workflow1 = MagicMock()
        workflow1.name = 'workflow1.yaml'
        workflow1.path = '.github/workflows/workflow1.yaml'
        workflow1.decoded_content = b"""
        name: Test Workflow 1
        on:
          push:
            branches:
              - main
        env:
          INTEGRATION_SUITE: true
        concurrency:
          group: integration
        steps:
          - name: Step 1
            run: echo "Step 1"
          - name: Step 2
            run: echo "Step 2"
        """
        workflow2 = MagicMock()
        workflow2.name = 'workflow2.yaml'
        workflow2.path = '.github/workflows/workflow2.yaml'
        workflow2.decoded_content = b"""
        name: Test Workflow 2
        on:
          push:
            branches:
              - main
        env:
          INTEGRATION_SUITE: false
        concurrency:
          group: integration
        steps:
          - name: Step 1
            run: echo "Step 1"
          - name: Step 2
            run: echo "Step 2"
        """
        repo.get_contents.return_value = [workflow1, workflow2]
        expected_result = {
            'workflow1.yaml': {
                'Integration Suite (GHA)': 'true',
                'Concurrency Rule (GHA)': 'integration',
                'Mend (GHA)': None
            },
            'workflow2.yaml': {
                'Integration Suite (GHA)': 'false',
                'Concurrency Rule (GHA)': 'integration',
                'Mend (GHA)': None
            }
        }
        self.assertEqual(get_workflow_info(repo), expected_result)


if __name__ == '__main__':
    unittest.main()
