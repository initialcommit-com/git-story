from manim import *
import git, sys, numpy

class GitStory(MovingCameraScene):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.drawnCommits = {}
        self.commits = []
        self.children = {}
        self.childChainLength = 0
        self.zoomOuts = 0

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
        try:
            self.repo = git.Repo(search_parent_directories=True)
        except git.exc.InvalidGitRepositoryError:
            print("git-story error: No Git repository found at current path.")
            sys.exit(1)
        
        try:
            self.commits = list(self.repo.iter_commits(self.args.commit_id))[:self.args.commits]
        except git.exc.GitCommandError:
            print("git-story error: No commits in current Git repository.")
            sys.exit(1)

        if ( len(self.commits) < self.args.commits ):
            self.args.commits = len(self.commits)

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

            if ( self.args.invert_branches ):
                for d in self.children:
                    if ( len(self.children[d]) > 1 ):
                        self.children[d].reverse()

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
        self.parseCommits(commit, i, prevCircle, toFadeOut)

        self.play(self.camera.frame.animate.move_to(toFadeOut.get_center()), run_time=1/self.args.speed)
        self.play(self.camera.frame.animate.scale_to_fit_width(toFadeOut.get_width()*1.1), run_time=1/self.args.speed)

        if ( toFadeOut.get_height() >= self.camera.frame.get_height() ):
            self.play(self.camera.frame.animate.scale_to_fit_height(toFadeOut.get_height()*1.25), run_time=1/self.args.speed)

        self.wait(3)

        self.play(FadeOut(toFadeOut), run_time=1/self.args.speed)

        if ( self.args.show_outro ):

            self.play(Restore(self.camera.frame))

            self.play(logo.animate.scale(4).set_x(0).set_y(0))

            outroTopText = Text(self.args.outro_top_text, font="Monospace", font_size=36, color=self.fontColor).to_edge(UP, buff=1)
            self.play(AddTextLetterByLetter(outroTopText))

            outroBottomText = Text(self.args.outro_bottom_text, font="Monospace", font_size=36, color=self.fontColor).to_edge(DOWN, buff=1)
            self.play(AddTextLetterByLetter(outroBottomText))

            self.wait(3)

    def parseCommits(self, commit, i, prevCircle, toFadeOut):
        if ( i < self.args.commits and commit in self.commits ):

            if ( len(commit.parents) <= 1 ):
                commitFill = RED
            else:
                commitFill = GRAY

            circle = Circle(stroke_color=commitFill, fill_color=commitFill, fill_opacity=0.25)
            circle.height = 1

            if prevCircle:
                circle.next_to(prevCircle, RIGHT, buff=1.5)

            offset = 0
            while ( any((circle.get_center() == c).all() for c in self.getCenters()) ):
                circle.next_to(circle, DOWN, buff=3.5)
                offset += 1
                if ( self.zoomOuts == 0 ):
                    self.play(self.camera.frame.animate.scale(1.5), run_time=1/self.args.speed)
                self.zoomOuts += 1

            isNewCommit = commit.hexsha not in self.drawnCommits

            if ( not self.args.reverse ):
                if ( isNewCommit ):
                    start = circle.get_center()
                    end = prevCircle.get_center() if prevCircle else LEFT
                else:
                    start = self.drawnCommits[commit.hexsha].get_center()
                    end = prevCircle.get_center()

            else:
                if ( isNewCommit ):
                    start = prevCircle.get_center() if prevCircle else LEFT
                    end = circle.get_center()
                else:
                    start = prevCircle.get_center()
                    end = self.drawnCommits[commit.hexsha].get_center()

            arrow = Arrow(start, end, color=self.fontColor)
            length = numpy.linalg.norm(start-end) - ( 1.5 if start[1] == end[1] else 3  )
            arrow.set_length(length)

            angle = arrow.get_angle()
            lineRect = Rectangle(height=0.1, width=length, color="#123456").move_to(arrow.get_center()).rotate(angle)

            for commitCircle in self.drawnCommits.values():
                inter = Intersection(lineRect, commitCircle)
                if ( inter.has_points() ):
                    arrow = CurvedArrow(start, end)
                    if ( start[1] == end[1]  ):
                        arrow.shift(UP*1.25)
                    if ( start[0] < end[0] and start[1] == end[1] ):
                        arrow.flip(RIGHT).shift(UP)
                
            commitId = Text(commit.hexsha[0:6], font="Monospace", font_size=20, color=self.fontColor).next_to(circle, UP)

            commitMessage = commit.message[:40].replace("\n", " ")
            message = Text('\n'.join(commitMessage[j:j+20] for j in range(0, len(commitMessage), 20))[:100], font="Monospace", font_size=14, color=self.fontColor).next_to(circle, DOWN)

            if ( isNewCommit ):

                self.play(self.camera.frame.animate.move_to(circle.get_center()), Create(circle), AddTextLetterByLetter(commitId), AddTextLetterByLetter(message), run_time=1/self.args.speed)
                self.drawnCommits[commit.hexsha] = circle

                prevRef = commitId
                if ( commit.hexsha == self.repo.head.commit.hexsha ):
                    head = Rectangle(color=BLUE, fill_color=BLUE, fill_opacity=0.25)
                    head.width = 1
                    head.height = 0.4
                    head.next_to(commitId, UP)
                    headText = Text("HEAD", font="Monospace", font_size=20, color=self.fontColor).move_to(head.get_center())
                    self.play(Create(head), Create(headText), run_time=1/self.args.speed)
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

                        self.play(Create(branchRec), Create(branchText), run_time=1/self.args.speed)
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

                        self.play(Create(tagRec), Create(tagText), run_time=1/self.args.speed)
                        toFadeOut.add(tagRec, tagText)

                        x += 1
                        if ( x >= self.args.max_tags_per_commit ):
                            break

            else:
                self.play(self.camera.frame.animate.move_to(self.drawnCommits[commit.hexsha].get_center()), run_time=1/self.args.speed)
                self.play(Create(arrow), run_time=1/self.args.speed)
                toFadeOut.add(arrow)
                return


            if ( prevCircle ):
                self.play(Create(arrow), run_time=1/self.args.speed)
                toFadeOut.add(arrow)

            prevCircle = circle

            toFadeOut.add(circle, commitId, message)

            if ( self.args.reverse ):
                commitParents = list(commit.parents)
                if ( len(commitParents) > 0 ):
                    if ( self.args.invert_branches ):
                        commitParents.reverse()

                    if ( self.args.hide_merged_chains ):
                        self.parseCommits(commitParents[0], i+1,  prevCircle, toFadeOut)
                    else:
                        for p in range(len(commitParents)):
                            self.parseCommits(commitParents[p], i+1, prevCircle, toFadeOut)

            else:
                try:
                    if ( len(self.children[commit.hexsha]) > 0 ):
                        if ( self.args.hide_merged_chains ):
                            self.parseCommits(self.children[commit.hexsha][0], i+1, prevCircle, toFadeOut)
                        else:
                            for p in range(len(self.children[commit.hexsha])):
                                self.parseCommits(self.children[commit.hexsha][p], i+1, prevCircle, toFadeOut)
                except KeyError:
                    pass

        else:
            return

    def getCenters(self):
        centers = []
        for commit in self.drawnCommits.values():
            centers.append(commit.get_center())
        return centers
