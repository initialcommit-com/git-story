from manim import *
import git

class GitStory(Scene):
    def __init__(self, numberOfCommits):
        super().__init__()
        self.numberOfCommits = numberOfCommits

    def construct(self):
        repo = git.Repo(search_parent_directories=True)
        commits = list(repo.iter_commits('HEAD'))
        commits.reverse()

        initialCommitLogo = ImageMobject("logo.png")
        self.add(initialCommitLogo)

        initialCommitText = Text("Git Story, by initialcommit.com", font="Monospace", font_size=36).to_edge(UP, buff=1)
        self.add(initialCommitText)
        self.wait(2)
        self.play(FadeOut(initialCommitText))
        self.play(initialCommitLogo.animate.scale(0.25).to_edge(UP, buff=0).to_edge(RIGHT, buff=0))

        i = 1
        prevCircle = None
        toFadeOut = Group()
        for commit in commits[:self.numberOfCommits]:
            circle = Circle()
            circle.height = 1

            if prevCircle:
                circle.next_to(prevCircle, RIGHT, buff=1.5)
            else:
                circle.to_edge(LEFT)

            arrow = Arrow(start=RIGHT, end=LEFT).next_to(circle, LEFT, buff=0)
            arrow.width = 1

            commitId = Text(commit.hexsha[0:6], font="Monospace", font_size=20).next_to(circle, UP)

            threeDots = ''
            if ( len(commit.message) > 18 ):
                threeDots = '...'

            message = Text(commit.message[:18] + threeDots, font="Monospace", font_size=14).next_to(circle, DOWN)

            self.play(Create(circle), AddTextLetterByLetter(commitId), AddTextLetterByLetter(message))

            if ( prevCircle ):
                self.play(Create(arrow))
                toFadeOut.add(arrow)

            prevCircle = circle

            toFadeOut.add(circle, commitId, message)
            i += 1

        self.wait(3)

        self.play(FadeOut(toFadeOut))

        self.play(initialCommitLogo.animate.scale(4).set_x(0).set_y(0))

        thankYouText= Text("Thanks for using Initial Commit!", font="Monospace", font_size=36).to_edge(UP, buff=1)
        self.play(AddTextLetterByLetter(thankYouText))

        learnMoreText = Text("Learn more at initialcommit.com", font="Monospace", font_size=36).to_edge(DOWN, buff=1)
        self.play(AddTextLetterByLetter(learnMoreText))

        self.wait(3)
