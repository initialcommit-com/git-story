# git-story
Tell the story of your Git project by creating video animations (.mp4)
of your commit history directly from your Git repo.

## Use cases
- Visualizing Git projects
- Sharing desired parts of your workflow with your team
- Creating animated Git videos for blog posts or YouTube
- Helping newer developers learn Git

## Features
- Run a single command in the terminal to generate a custom Git animation (.mp4) from your repo
- Specify any commit id or ref to start animating from (default: `HEAD`)
- Specify the number of commits to include (default: `8`)
- Ref labels are drawn by default for `HEAD`, branch names, and tags
- Reverse commit ordering and reorient branch layout
- Works best with simpler branching structures, but should work with more complex ones as well
- Add custom branded intro/outro sequences if desired
- Dark mode and light mode

## Video animation example
https://user-images.githubusercontent.com/49353917/179362209-48748966-6d6c-46ff-9424-b1a7266fc83f.mp4

## Requirements
* Python 3.9 or greater
* Pip (Package manager for Python)
* [Manim (Community version)](https://www.manim.community/)
* GitPython

## Quickstart
1) Install [manim and manim dependencies for your OS](https://www.manim.community/)

2) Install GitPython

```console
$ pip3 install gitpython
```

3) Install `git-story`:

```console
$ pip3 install git-story
```

3) Browse to the Git repository you want create an animation from:

```console
$ cd path/to/project/root
```

4) Run the program:

```console
$ git-story
```

5) A default animation `.mp4` file will be created using the most recent 8 commits on your checked-out Git branch. By default, video output file is created in the current directory, within a subdirectory called `git-story_media`. The location this subdirectory is customizeable using the command line flag `--media-dir=path/to/output`.

6) Use command-line options for customization, see usage:

```console
$ git-story -h

usage: git-story [-h] [--commits COMMITS] [--commit-id COMMIT_ID] [--hide-merged-chains] [--reverse] [--title TITLE] [--logo LOGO] [--outro-top-text OUTRO_TOP_TEXT]
                 [--outro-bottom-text OUTRO_BOTTOM_TEXT] [--show-intro] [--show-outro] [--max-branches-per-commit MAX_BRANCHES_PER_COMMIT] [--max-tags-per-commit MAX_TAGS_PER_COMMIT]
                 [--media-dir MEDIA_DIR] [--low-quality] [--light-mode] [--invert-branches]

optional arguments:
  -h, --help            show this help message and exit
  --commits COMMITS     The number of commits to display in the Git animation (default: 8)
  --commit-id COMMIT_ID
                        The ref (branch/tag), or first 6 characters of the commit to animate backwards from (default: HEAD)
  --hide-merged-chains  Hide commits from merged branches, i.e. only display mainline commits (default: False)
  --reverse             Display commits in reverse order in the Git animation (default: False)
  --title TITLE         Custom title to display at the beginning of the animation (default: Git Story, by initialcommit.com)
  --logo LOGO           The path to a custom logo to use in the animation intro/outro (default: /usr/local/lib/python3.9/site-packages/git_story/logo.png)
  --outro-top-text OUTRO_TOP_TEXT
                        Custom text to display above the logo during the outro (default: Thanks for using Initial Commit!)
  --outro-bottom-text OUTRO_BOTTOM_TEXT
                        Custom text to display below the logo during the outro (default: Learn more at initialcommit.com)
  --show-intro          Add an intro sequence with custom logo and title (default: False)
  --show-outro          Add an outro sequence with custom logo and text (default: False)
  --max-branches-per-commit MAX_BRANCHES_PER_COMMIT
                        Maximum number of branch labels to display for each commit (default: 2)
  --max-tags-per-commit MAX_TAGS_PER_COMMIT
                        Maximum number of tags to display for each commit (default: 1)
  --media-dir MEDIA_DIR
                        The path to output the animation data and video file (default: .)
  --low-quality         Render output video in low quality, useful for faster testing (default: False)
  --light-mode          Enable light-mode with white background (default: False)
  --invert-branches     Invert positioning of branches where applicable (default: False)
```

## Command Examples
Default - draw 8 commits starting from `HEAD`, from oldest to newest:

```console
$ cd path/to/project/root
$ git-story
```

Customize the start commit and number of commits, and reverse their display order:

```console
$ git-story --commit-id a1b2c3 --commits=6 --reverse
```

Invert the branch orientation, if multiple branches exist in the commit range:

```console
$ git-story --invert-branches
```

Add an intro with custom title and logo:

```console
$ git-story --commit-id dev --commits=10 --show-intro --title "My Git Repo" --logo path/to/logo.png
```

Add an outro with custom text and logo:

```console
$ git-story --show-outro --outro-top-text "My Git Repo" --outro-bottom-text "Thanks for watching!" --logo path/to/logo.png
```

Customize the output video directory location:

```console
$ git-story --media-dir=path/to/output
```

Use light mode for white background and black text, instead of the default black background with white text:

```console
$ git-story --light-mode
```

Generate output video in low quality to speed up rendering time (useful for repeated testing):

```console
$ git-story --low-quality
```

## Installation
See **QuickStart** section for details on installing manim and GitPython dependencies. Then run:

```console
$ pip3 install git-story
```

## Learn More
Learn more about this tool on the [git-story project page](https://initialcommit.com/tools/git-story).

## Authors
**Jacob Stopak** - on behalf of [Initial Commit](https://initialcommit.com)
