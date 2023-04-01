from argparse import Namespace
from pathlib import Path
from typing import List, Tuple

from pygit2 import Walker

from prime_explode.utils import filesystem
from prime_explode.vcs import git


def testFileSystem(args: Namespace) -> None:
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

    testFileSystem(args=args)

    commitWalkers: List[Tuple[str, Walker]] = []

    branches: List[str] = git.getBranchesList(path=args.gitSrc)

    branch: str
    for branch in branches:
        git.checkoutBranch(path=args.gitSrc, branch=branch)
        commitWalker: Walker = git.getCommitWalker(path=args.gitSrc)

        pair: Tuple[str, Walker] = (branch, commitWalker)

        commitWalkers.append(pair)

    for pair in commitWalkers:
        print(pair)
