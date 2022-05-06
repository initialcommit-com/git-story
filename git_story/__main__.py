import git_story as gs
import sys
from manim.utils.file_ops import open_file as open_media_file

def main():
    scene = gs.GitStory(int(sys.argv[1]))
    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)

if __name__ == '__main__':
    main()
