# git-story
---

Find and tag Git commits based on version numbers in commit messages.

If you're like me, you often add the version number for a commit into the commit message itself, something like:

```console
$ git commit -m "Bump version to 2.1.5"
```

If you're still like me you probably forget to create a tag for the new version and push
it to the remote repository. I end up having projects that have many un-tagged commits
from months or years ago that never get real tags.

I created `git-tagup` to conveniently search through the active branch in a Git repository
and find un-tagged commits containing version numbers in the commit message. For each one
it finds, the tool asks the user whether they want to create a tag for it.

Currently only [SemVer](http://semver.org/) versioning format is supported, but I'm happy
to take requests for other formats.

Happy tagging!

## Requirements
---

* Python 3.6 or greater
* Pip (Package manager for Python)

## Quickstart
---

1) Install `git-tagup`:

```console
$ pip install git-tagup
```

2) Browse to the Git repository you want to add tags to - this is usually your project root directory containing the `.git` directory:

```console
$ cd path/to/project/root
```

3) Run the program:

```console
$ git-tagup
```

4) If version numbers are found in the commit messages, answer the prompts with a `y` to create the tag or `n` to skip it.

5) Don't forget to push the new tags to your remote when done!

```console
$ git push --followtags
```

## Example
---

```console
$ cd path/to/project/root
$ git-tagup
Create the tag 'v0.1.1' for commit message 'Bump version to 0.1.1'? (y/n/q): n
Create the tag 'v0.1.2' for commit message 'Bump version to 0.1.2'? (y/n/q): y
Create the tag 'v0.1.3' for commit message 'Bump version to 0.1.3'? (y/n/q): q
```

## Installation
---

```console
$ pip install git-tagup
```

## Learn More
---

Learn more about this project on the [git-tagup project page](https://initialcommit.com/projects/git-tagup).

## Authors
---

* **Jacob Stopak** - on behalf of [Initial Commit](https://initialcommit.com)
