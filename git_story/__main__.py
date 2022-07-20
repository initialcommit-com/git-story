from git_story import git_story as gs
import os
import argparse
import pathlib
from manim import config, WHITE
from manim.utils.file_ops import open_file as open_media_file

def main():
    parser = argparse.ArgumentParser("git-story", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--commits", help="The number of commits to display in the Git animation", type=int, default=8)
    parser.add_argument("--commit-id", help="The ref (branch/tag), or first 6 characters of the commit to animate backwards from", type=str, default="HEAD")
    parser.add_argument("--hide-merged-chains", help="Hide commits from merged branches, i.e. only display mainline commits", action="store_true")
    parser.add_argument("--reverse", help="Display commits in reverse order in the Git animation", action="store_true")
    parser.add_argument("--title", help="Custom title to display at the beginning of the animation", type=str, default="Git Story, by initialcommit.com")
    parser.add_argument("--logo", help="The path to a custom logo to use in the animation intro/outro", type=str, default=os.path.join(str(pathlib.Path(__file__).parent.resolve()), "logo.png"))
    parser.add_argument("--outro-top-text", help="Custom text to display above the logo during the outro", type=str, default="Thanks for using Initial Commit!")
    parser.add_argument("--outro-bottom-text", help="Custom text to display below the logo during the outro", type=str, default="Learn more at initialcommit.com")
    parser.add_argument("--show-intro", help="Add an intro sequence with custom logo and title", action="store_true")
    parser.add_argument("--show-outro", help="Add an outro sequence with custom logo and text", action="store_true")
    parser.add_argument("--max-branches-per-commit", help="Maximum number of branch labels to display for each commit", type=int, default=2)
    parser.add_argument("--max-tags-per-commit", help="Maximum number of tags to display for each commit", type=int, default=1)
    parser.add_argument("--media-dir", help="The path to output the animation data and video file", type=str, default=".")
    parser.add_argument("--low-quality", help="Render output video in low quality, useful for faster testing", action="store_true")
    parser.add_argument("--light-mode", help="Enable light-mode with white background", action="store_true")
    parser.add_argument("--invert-branches", help="Invert positioning of branches where applicable", action="store_true")
    parser.add_argument("--speed", help="A multiple of the standard 1x animation speed (ex: 2 = twice as fast, 0.5 = half as fast)", type=float, default=1)

    args = parser.parse_args()

    config.media_dir = os.path.join(args.media_dir, "git-story_media")

    if ( args.low_quality ):
        config.quality = "low_quality"

    if ( args.light_mode ):
        config.background_color = WHITE

    scene = gs.GitStory(args)
    scene.render()

    try:
        open_media_file(scene.renderer.file_writer.movie_file_path)
    except FileNotFoundError:
        print("Error automatically opening video player, please manually open the video file to view animation.")

if __name__ == '__main__':
    main()
