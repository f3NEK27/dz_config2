import unittest
from unittest.mock import patch, MagicMock
from git_visualizer import GitDependencyVisualizer


class TestGitDependencyVisualizer(unittest.TestCase):
    @patch("subprocess.run")
    def test_get_commit_dependencies(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(stdout="commit1 commit2\ncommit2\n")
        visualizer = GitDependencyVisualizer("/path/to/repo", "v1.0")
        visualizer.get_commit_dependencies()
        self.assertEqual(visualizer.dependencies, {"commit1": ["commit2"], "commit2": []})

    @patch("subprocess.run")
    def test_visualize(self, mock_subprocess):
        visualizer = GitDependencyVisualizer("/path/to/repo", "v1.0")
        visualizer.dependencies = {"commit1": ["commit2"], "commit2": []}
        puml_code = visualizer.generate_puml_tree()
        self.assertIn('"commit2" -> "commit1";', puml_code)
