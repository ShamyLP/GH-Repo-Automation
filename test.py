import unittest
from unittest.mock import MagicMock, patch
from github import Github
from datetime import datetime, timedelta
from script import get_package_manager, get_dependency_management, get_semantic_release, get_gha, get_workflow_info


class TestLPGitHubRepoAnalysis(unittest.TestCase):

    def test_get_package_manager_package_lock(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value = ['file1', 'file2', 'package-lock.json']
        self.assertEqual(get_package_manager(repo), 'NPM')

    def test_get_package_manager_yarn_lock(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value = ['file1', 'file2', 'yarn.lock']
        self.assertEqual(get_package_manager(repo), 'Yarn')

    def test_get_package_manager_no_lock_files(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value = ['file1', 'file2']
        self.assertEqual(get_package_manager(repo), 'No')

    def test_get_dependency_management_dependabot(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_pulls.return_value.totalCount = 3
        self.assertEqual(get_dependency_management(repo), 'Dependabot')

    def test_get_dependency_management_renovate(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_pulls.return_value.totalCount = 5
        self.assertEqual(get_dependency_management(repo), 'Renovate')

    def test_get_dependency_management_no_management(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_pulls.return_value.totalCount = 0
        self.assertEqual(get_dependency_management(repo), 'No')

    def test_get_semantic_release_present(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value.decoded_content = b'{"devDependencies": {"semantic-release": "^2.0.0"}}'
        self.assertEqual(get_semantic_release(repo), 'Yes')

    def test_get_semantic_release_not_present(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value.decoded_content = b'{"devDependencies": {"other-package": "^1.0.0"}}'
        self.assertEqual(get_semantic_release(repo), 'No')

    def test_get_semantic_release_invalid_json(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value.decoded_content = b'Invalid JSON'
        self.assertEqual(get_semantic_release(repo), 'No')

    def test_get_gha_workflows_used_within_last_year(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        workflow1 = MagicMock()
        workflow1.last_modified = datetime.now() - timedelta(days=100)
        workflow2 = MagicMock()
        workflow2.last_modified = datetime.now() - timedelta(days=200)
        repo.get_contents.return_value = [workflow1, workflow2]
        self.assertEqual(get_gha(repo), 'Yes')

    def test_get_gha_workflows_not_used_within_last_year(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        workflow1 = MagicMock()
        workflow1.last_modified = datetime.now() - timedelta(days=400)
        workflow2 = MagicMock()
        workflow2.last_modified = datetime.now() - timedelta(days=500)
        repo.get_contents.return_value = [workflow1, workflow2]
        self.assertEqual(get_gha(repo), 'No')

    def test_get_gha_no_workflows(self):
        # Create a mock repository object for testing
        repo = MagicMock()
        repo.get_contents.return_value = []
        self.assertEqual(get_gha(repo), 'No')

    def test_get_workflow_info(self):
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
                'Integration Suite': 'true',
                'Concurrency Rule': 'integration',
                'Mend': None
            },
            'workflow2.yaml': {
                'Integration Suite': 'false',
                'Concurrency Rule': 'integration',
                'Mend': None
            }
        }
        self.assertEqual(get_workflow_info(repo), expected_result)


if __name__ == '__main__':
    unittest.main()
