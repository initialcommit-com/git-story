import git_story as gs
import sys
import argparse
from manim.utils.file_ops import open_file as open_media_file

def main():
    parser = argparse.ArgumentParser("git-story")
    parser.add_argument("--commits", help="The number of commits to display in the Git animation", type=int)
    parser.add_argument("--reverse", help="Display commits in reverse order in the Git animation", action="store_true")
    parser.add_argument("--title", help="Custom title to display at the beginning of the animation", type=str, default="Git Story, by initialcommit.com")
    parser.add_argument("--logo", help="The path to a custom logo to use in the animation intro/outro", type=str, default="logo.png")
    parser.add_argument("--outro-toptext", help="Custom text to display above the logo during the outro", type=str, default="Thanks for using Initial Commit!")
    parser.add_argument("--outro-bottomtext", help="Custom text to display below the logo during the outro", type=str, default="Learn more at initialcommit.com")
    parser.add_argument("--no-intro", help="Omit the intro sequence from the animation", action="store_true")
    parser.add_argument("--no-outro", help="Omit the outro sequence from the animation", action="store_true")
    
    scene = gs.GitStory(parser.parse_args())
    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)

if __name__ == '__main__':
    main()
