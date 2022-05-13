import unittest, git, argparse
from manim import *

from git_story.git_story import GitStory


class TestGitStory(unittest.TestCase):

    def test_git_story(self):
        """Test git story."""

        gs = GitStory(argparse.Namespace())

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
