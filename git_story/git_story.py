from manim import *
import git

class GitStory(Scene):
    def construct(self):
        repo = git.Repo(search_parent_directories=True)
        commits = list(repo.iter_commits('HEAD'))
