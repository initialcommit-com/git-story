import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git-story",
    version="0.0.1",
    author="Jacob Stopak",
    author_email="jacob@initialcommit.io",
    description="Generate basic Git animations from local Git repositories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://initialcommit.com/projects/git-story",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'gitpython',
        'manim'
    ],
    keywords='git story git-story manim animation gitanimation',
    project_urls={
        'Homepage': 'https://initialcommit.com/projects/git-story',
    },
    entry_points={
        'console_scripts': [
            'git-story=git_story.__main__:main',
            'gs=git_story.__main__:main',
        ],
    },
)
