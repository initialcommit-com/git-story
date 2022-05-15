from manim import *
import git

class GitStory(MovingCameraScene):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.drawnCommits = {}
        self.commits = []
        self.children = {}
        self.offsetLevel = 0
        self.childChainLength = 0

        if ( self.args.light_mode ):
            self.fontColor = BLACK
        else:
            self.fontColor = WHITE

    def measureChildChain(self, commit):
        try:
            if ( len(self.children[commit.hexsha]) > 0 ):
                for child in self.children[commit.hexsha]:
                    self.childChainLength += 1
                    return self.measureChildChain(child)
            else:
                return self.childChainLength
        except KeyError:
            return self.childChainLength
            

    def construct(self):
        self.repo = git.Repo(search_parent_directories=True)
        self.commits = list(self.repo.iter_commits(self.args.commit_id))[:self.args.commits]

        if ( not self.args.reverse ):
            self.commits.reverse()
            for commit in self.commits:
                if ( len(commit.parents) > 0 ):
                    for parent in commit.parents:
                        self.children.setdefault(parent.hexsha, []).append(commit)
            z = 1
            while ( self.measureChildChain(self.commits[0]) < self.args.commits-1 ):
                self.commits = list(self.repo.iter_commits(self.args.commit_id))[:self.args.commits + z]
                self.commits.reverse()
                self.children = {}
                for commit in self.commits:
                    if ( len(commit.parents) > 0 ):
                        for parent in commit.parents:
                            self.children.setdefault(parent.hexsha, []).append(commit)
                z += 1

        commit = self.commits[0]

        logo = ImageMobject(self.args.logo)
        logo.width = 3

        if ( self.args.show_intro ):
            self.add(logo)

            initialCommitText = Text(self.args.title, font="Monospace", font_size=36, color=self.fontColor).to_edge(UP, buff=1)
            self.add(initialCommitText)
            self.wait(2)
            self.play(FadeOut(initialCommitText))
            self.play(logo.animate.scale(0.25).to_edge(UP, buff=0).to_edge(RIGHT, buff=0))
    
            self.camera.frame.save_state()
            self.play(FadeOut(logo))

        else:
            logo.scale(0.25).to_edge(UP, buff=0).to_edge(RIGHT, buff=0)
            self.camera.frame.save_state()

        i = 0
        prevCircle = None
        toFadeOut = Group()
        self.parseCommits(commit, i, prevCircle, toFadeOut, False)

        self.play(self.camera.frame.animate.move_to(toFadeOut.get_center()))
        self.play(self.camera.frame.animate.scale_to_fit_width(toFadeOut.get_width()*1.1))

        if ( toFadeOut.get_height() >= self.camera.frame.get_height() ):
            self.play(self.camera.frame.animate.scale_to_fit_height(toFadeOut.get_height()*1.25))

        self.wait(3)

        self.play(FadeOut(toFadeOut))

        if ( self.args.show_outro ):

            self.play(Restore(self.camera.frame))

            self.play(logo.animate.scale(4).set_x(0).set_y(0))

            outroTopText = Text(self.args.outro_top_text, font="Monospace", font_size=36, color=self.fontColor).to_edge(UP, buff=1)
            self.play(AddTextLetterByLetter(outroTopText))

            outroBottomText = Text(self.args.outro_bottom_text, font="Monospace", font_size=36, color=self.fontColor).to_edge(DOWN, buff=1)
            self.play(AddTextLetterByLetter(outroBottomText))

            self.wait(3)

    def parseCommits(self, commit, i, prevCircle, toFadeOut, offset):
        if ( i < self.args.commits ):

            if ( len(commit.parents) <= 1 ):
                commitFill = RED
            else:
                commitFill = GRAY

            circle = Circle(stroke_color=commitFill, fill_color=commitFill, fill_opacity=0.25)
            circle.height = 1

            if prevCircle:
                circle.next_to(prevCircle, RIGHT, buff=1.5)

            if ( offset ):
                circle.next_to(circle, DOWN, buff=3.5)

                if ( not self.offsetLevel ):
                    self.play(self.camera.frame.animate.scale(1.5))
                    self.offsetLevel += 1

            self.play(self.camera.frame.animate.move_to(circle.get_center()))

            isNewCommit = commit.hexsha not in self.drawnCommits

            if ( not self.args.reverse ):
                if ( not offset and isNewCommit ):
                    arrow = Arrow(start=RIGHT, end=LEFT, color=self.fontColor).next_to(circle, LEFT, buff=0)
                elif ( offset and isNewCommit ):
                    arrow = Arrow(end=prevCircle.get_center(), start=circle.get_center(), color=self.fontColor)
                elif ( offset and not isNewCommit ):
                    arrow = Arrow(end=prevCircle.get_center(), start=self.drawnCommits[commit.hexsha].get_center(), color=self.fontColor)
                elif ( not offset and not isNewCommit ):
                    arrow = Arrow(end=prevCircle.get_center(), start=self.drawnCommits[commit.hexsha].get_center(), color=self.fontColor)

            else:
                if ( not offset and isNewCommit ):
                    arrow = Arrow(start=LEFT, end=RIGHT, color=self.fontColor).next_to(circle, LEFT, buff=0)
                elif ( offset and isNewCommit ):
                    arrow = Arrow(start=prevCircle.get_center(), end=circle.get_center(), color=self.fontColor)
                elif ( offset and not isNewCommit ):
                    arrow = Arrow(start=prevCircle.get_center(), end=self.drawnCommits[commit.hexsha].get_center(), color=self.fontColor)
                elif ( not offset and not isNewCommit ):
                    arrow = Arrow(start=prevCircle.get_center(), end=self.drawnCommits[commit.hexsha].get_center(), color=self.fontColor)

            arrow.width = 1

            commitId = Text(commit.hexsha[0:6], font="Monospace", font_size=20, color=self.fontColor).next_to(circle, UP)

            newlineIndexes = []
            cm = commit.message[:100]
            c = 0
            while ( len(cm) / 20 > 1 ):
               newlineIndexes.append(cm.rfind(" ", 0, 20)+20*c)
               cm = cm[20:]
               c += 1

            for n in newlineIndexes:
                commit.message = commit.message[:n] + "\n" + commit.message[n+1:]

            message = Text(commit.message[:100], font="Monospace", font_size=14, color=self.fontColor).next_to(circle, DOWN)

            if ( isNewCommit ):
                self.play(Create(circle), AddTextLetterByLetter(commitId), AddTextLetterByLetter(message))
                self.drawnCommits[commit.hexsha] = circle

                prevRef = commitId
                if ( commit.hexsha == self.repo.head.commit.hexsha ):
                    head = Rectangle(color=BLUE, fill_color=BLUE, fill_opacity=0.25)
                    head.width = 1
                    head.height = 0.4
                    head.next_to(commitId, UP)
                    headText = Text("HEAD", font="Monospace", font_size=20, color=self.fontColor).move_to(head.get_center())
                    self.play(Create(head), Create(headText))
                    toFadeOut.add(head, headText)
                    prevRef = head

                x = 0
                for branch in self.repo.heads:
                    if ( commit.hexsha == branch.commit.hexsha ):
                        branchText = Text(branch.name, font="Monospace", font_size=20, color=self.fontColor)
                        branchRec = Rectangle(color=GREEN, fill_color=GREEN, fill_opacity=0.25, height=0.4, width=branchText.width+0.25)

                        branchRec.next_to(prevRef, UP)
                        branchText.move_to(branchRec.get_center())

                        prevRef = branchRec 

                        self.play(Create(branchRec), Create(branchText))
                        toFadeOut.add(branchRec, branchText)

                        x += 1
                        if ( x >= self.args.max_branches_per_commit ):
                            break

                x = 0
                for tag in self.repo.tags:
                    if ( commit.hexsha == tag.commit.hexsha ):
                        tagText = Text(tag.name, font="Monospace", font_size=20, color=self.fontColor)
                        tagRec = Rectangle(color=YELLOW, fill_color=YELLOW, fill_opacity=0.25, height=0.4, width=tagText.width+0.25)

                        tagRec.next_to(prevRef, UP)
                        tagText.move_to(tagRec.get_center())

                        prevRef = tagRec

                        self.play(Create(tagRec), Create(tagText))
                        toFadeOut.add(tagRec, tagText)

                        x += 1
                        if ( x >= self.args.max_tags_per_commit ):
                            break

            else:
                self.play(Create(arrow))
                toFadeOut.add(arrow)
                return


            if ( prevCircle ):
                self.play(Create(arrow))
                toFadeOut.add(arrow)

            prevCircle = circle

            toFadeOut.add(circle, commitId, message)

            if ( self.args.reverse ):
                if ( len(commit.parents) > 0 ):
                    if ( self.args.hide_merged_chains ):
                        self.parseCommits(commit.parents[0], i+1, prevCircle, toFadeOut, False)
                    else:
                        for p in range(len(commit.parents)):
                            self.parseCommits(commit.parents[p], i+1, prevCircle, toFadeOut, False if ( p == 0 ) else True)

            else:
                try:
                    if ( len(self.children[commit.hexsha]) > 0 ):
                        if ( self.args.hide_merged_chains ):
                            self.parseCommits(self.children[commit.hexsha][0], i+1, prevCircle, toFadeOut, False)
                        else:
                            for p in range(len(self.children[commit.hexsha])):
                                self.parseCommits(self.children[commit.hexsha][p], i+1, prevCircle, toFadeOut, False if ( p == 0 ) else True)
                except KeyError:
                    pass

        else:
            return
