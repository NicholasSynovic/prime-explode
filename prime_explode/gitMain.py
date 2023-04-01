from argparse import Namespace
from itertools import pairwise
from pathlib import Path
from typing import List

from pygit2 import Repository

from prime_explode.utils import filesystem
from prime_explode.vcs import git


def checkFileSystem(args: Namespace) -> None:
    # Steps

    # 1. Check if the src directory exists
    # 2. Check if the src directory contains a git repo
    # If not, exit with reason
    # 3. Check if the dest directory exists
    # If it does, exit with reason

    if filesystem.testIfDirectory(path=args.gitSrc) is False:
        print(f"{args.gitSrc} is not a valid source directory")
        exit(code=1)

    dotGitFolder: Path = git.getRepoPath(path=args.gitSrc)

    if filesystem.testIfDirectory(path=dotGitFolder) is False:
        print(f"{args.gitSrc.resolve()} is not a valid Git repository")
        exit(code=2)

    if filesystem.testIfDirectory(args.gitDest):
        print(f"{args.gitDest.resolve()} already exists.")
        exit(code=3)


def main(args: Namespace) -> None:
    # Steps:

    # 5. Checkout the repository to the HEAD commit
    # 4. Get a list of branches

    checkFileSystem(args=args)

    gitRepo: Repository = Repository(path=gitRepoSrc)

    branches: List[str] = git.getBranchesList(repo=gitRepo)

    data: List[iter] = []

    branch: str
    for branch in branches:
        git.checkoutBranch(repo=gitRepo, branch=branch)
        data.append(gitRepo.walk(gitRepo.head.target))

    dp: pairwise = pairwise(data)

    for d in dp:
        print(d[0] == d[1])
