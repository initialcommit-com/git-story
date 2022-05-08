from manim import *
import git

class GitStory(MovingCameraScene):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def construct(self):
        repo = git.Repo(search_parent_directories=True)
        commits = list(repo.iter_commits('HEAD'))

        if ( not self.args.reverse ):
            commits.reverse()

        logo = ImageMobject(self.args.logo)
        logo.width = 3

        if ( not self.args.no_intro ):
            self.add(logo)

            initialCommitText = Text(self.args.title, font="Monospace", font_size=36).to_edge(UP, buff=1)
            self.add(initialCommitText)
            self.wait(2)
            self.play(FadeOut(initialCommitText))
            self.play(logo.animate.scale(0.25).to_edge(UP, buff=0).to_edge(RIGHT, buff=0))
	
            self.camera.frame.save_state()
            self.play(FadeOut(logo))

        else:
            logo.scale(0.25).to_edge(UP, buff=0).to_edge(RIGHT, buff=0)
            self.camera.frame.save_state()

        i = 1
        prevCircle = None
        toFadeOut = Group()
        for commit in commits[:self.args.commits]:
            circle = Circle()
            circle.height = 1

            if prevCircle:
                circle.next_to(prevCircle, RIGHT, buff=1.5)

            self.play(self.camera.frame.animate.move_to(circle.get_center()))

            if ( not self.args.reverse ):
                arrow = Arrow(start=RIGHT, end=LEFT).next_to(circle, LEFT, buff=0)
            else:
                arrow = Arrow(start=LEFT, end=RIGHT).next_to(circle, LEFT, buff=0)

            arrow.width = 1

            commitId = Text(commit.hexsha[0:6], font="Monospace", font_size=20).next_to(circle, UP)

            message = Text('\n'.join(commit.message[i:i+20] for i in range(0, len(commit.message), 20))[:100], font="Monospace", font_size=14).next_to(circle, DOWN)

            self.play(Create(circle), AddTextLetterByLetter(commitId), AddTextLetterByLetter(message))

            prevRef = commitId
            if ( commit.hexsha == repo.head.commit.hexsha ):
                head = Rectangle(color=BLUE, fill_color=BLUE)
                head.width = 1
                head.height = 0.4
                head.next_to(commitId, UP)
                headText = Text("HEAD", font="Monospace", font_size=20).next_to(commitId, UP*1.5)
                self.play(Create(head), Create(headText))
                toFadeOut.add(head, headText)
                prevRef = head

            x = 0
            for branch in repo.heads:
                if ( commit.hexsha == branch.commit.hexsha ):
                    branchText = Text(branch.name, font="Monospace", font_size=20)
                    branchRec = Rectangle(color=GREEN, fill_color=GREEN, height=0.4, width=branchText.width+0.25)

                    branchRec.next_to(prevRef, UP)
                    branchText.next_to(prevRef, UP*1.5)

                    prevRef = branchRec 

                    self.play(Create(branchRec), Create(branchText))
                    toFadeOut.add(branchRec, branchText)

                    x += 1
                    if ( x >= self.args.max_branches_per_commit ):
                        break


            if ( prevCircle ):
                self.play(Create(arrow))
                toFadeOut.add(arrow)

            prevCircle = circle

            toFadeOut.add(circle, commitId, message)
            i += 1

        self.wait(3)

        self.play(FadeOut(toFadeOut))

        if ( not self.args.no_outro ):

            self.play(Restore(self.camera.frame))

            self.play(logo.animate.scale(4).set_x(0).set_y(0))

            outroTopText = Text(self.args.outro_top_text, font="Monospace", font_size=36).to_edge(UP, buff=1)
            self.play(AddTextLetterByLetter(outroTopText))

            outroBottomText = Text(self.args.outro_bottom_text, font="Monospace", font_size=36).to_edge(DOWN, buff=1)
            self.play(AddTextLetterByLetter(outroBottomText))

            self.wait(3)
