import git_story as gs
import sys
import argparse
from manim.utils.file_ops import open_file as open_media_file

def main():
    parser = argparse.ArgumentParser("git-story")
    parser.add_argument("--commits", help="The number of commits to display in the Git animation", type=int)
    parser.add_argument("--title", help="The title to display at the beginning of the animation", type=str, default="Git Story, by initialcommit.com")
    parser.add_argument("--logo", help="The path to a custom logo to add into the animation intro/outro", type=str)
    parser.add_argument("--no-intro", help="Omit the intro sequence from the animation", action='store_true')
    parser.add_argument("--no-outro", help="Omit the outro sequence from the animation", action='store_true')
    
    scene = gs.GitStory(parser.parse_args())
    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)

if __name__ == '__main__':
    main()
