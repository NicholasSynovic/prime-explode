from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Generator, List, Tuple

from progress.bar import Bar
from pygit2 import Walker

from prime_explode.utils import filesystem
from prime_explode.vcs import git


def testFileSystem(src: Path, dest: Path) -> None:
    # Steps

    # 1. Check if the src directory exists
    # 2. Check if the src directory contains a git repo
    # If not, exit with reason
    # 3. Check if the dest directory exists
    # If it does, exit with reason

    if filesystem.testIfDirectory(path=src) is False:
        print(f"{src} is not a valid source directory")
        exit(code=1)

    dotGitFolder: Path = git.getRepoPath(path=src)

    if filesystem.testIfDirectory(path=dotGitFolder) is False:
        print(f"{src.resolve()} is not a valid Git repository")
        exit(code=2)

    if filesystem.testIfDirectory(dest):
        print(f"{dest.resolve()} already exists.")
        exit(code=3)


def getCommitWalkers(gitPath: Path) -> List[Tuple[str, Walker]]:
    # Steps:

    # 1. Get a list of branches
    # 2. For each branch, get an iterator of commits
    # 3. Return a list of iterators for each branch

    commitWalkers: List[Tuple[str, Walker]] = []
    branches: List[str] = git.getBranchesList(path=gitPath)

    with Bar(
        "Getting iterators of commits from each branch...", max=len(branches)
    ) as bar:
        branch: str
        for branch in branches:
            git.checkoutBranch(path=gitPath, branch=branch)
            commitWalker: Walker = git.getCommitWalker(path=gitPath)

            pair: Tuple[str, Walker] = (branch, commitWalker)

            commitWalkers.append(pair)
            bar.next()

    return commitWalkers


def createDestTree(branches: List[str], srcPath: Path, destPath: Path) -> None:
    filesystem.createDirectory(path=destPath)

    with Bar("Cloning branches into destination...", max=len(branches)) as bar:
        with ThreadPoolExecutor() as executor:

            def _run(branch: str) -> None:
                tmpDestPath: Path = Path(destPath, "_tmp", branch.replace("/", "_"))
                tmpBranchPath: Path = git.cloneBranch(
                    srcPath=srcPath, destPath=tmpDestPath, branch=branch
                )
                bar.next()
                return tmpBranchPath

            clonePaths: Generator[Path] = executor.map(_run, branches)

    for branch in branches:
        _branch: str = branch.replace("/", "_")
        branchPath: Path = Path(destPath, _branch)
        filesystem.createDirectory(path=branchPath)


def main(args: Namespace) -> None:
    testFileSystem(src=args.gitSrc, dest=args.gitDest)

    commitWalkers: List[Tuple[str, Walker]] = getCommitWalkers(gitPath=args.gitSrc)

    branches: List[str] = [pair[0] for pair in commitWalkers]

    createDestTree(branches=branches, srcPath=args.gitSrc, destPath=args.gitDest)
