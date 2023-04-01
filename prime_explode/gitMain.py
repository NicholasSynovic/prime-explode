from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Tuple

from progress.bar import Bar
from progress.spinner import Spinner
from pygit2 import Commit, Walker

from prime_explode.utils import filesystem
from prime_explode.vcs import git

TEMP_GIT_CLONE_PATH: str = "_tmp"


def testFileSystem(src: Path, dest: Path) -> None:
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
                tmpDestPath: Path = Path(
                    destPath, TEMP_GIT_CLONE_PATH, branch.replace("/", "_")
                )
                git.cloneBranch(srcPath=srcPath, destPath=tmpDestPath, branch=branch)
                bar.next()

            executor.map(_run, branches)

    for branch in branches:
        _branch: str = branch.replace("/", "_")
        branchPath: Path = Path(destPath, _branch)
        filesystem.createDirectory(path=branchPath)


def main(args: Namespace) -> None:
    testFileSystem(src=args.gitSrc, dest=args.gitDest)

    commitWalkers: List[Tuple[str, Walker]] = getCommitWalkers(gitPath=args.gitSrc)
    branches: List[str] = [pair[0] for pair in commitWalkers]

    createDestTree(branches=branches, srcPath=args.gitSrc, destPath=args.gitDest)

    branch: str
    walker: Walker
    for branch, walker in commitWalkers:
        tmpGitRepoDirectory: Path = Path(
            args.gitDest, TEMP_GIT_CLONE_PATH, branch.replace("/", "_")
        )
        branchDirectory: Path = Path(args.gitDest, branch.replace("/", "_"))
        commits: List[Commit] = list(walker)

        with Bar(f"Creating directories of commit for branch: {branch}...") as bar:
            with ThreadPoolExecutor() as executor:

                def _run(commit: Commit) -> None:
                    commitID: str = commit.id.hex
                    commitDirectory: Path = Path(branchDirectory, commitID)
                    git.checkoutCommit(
                        srcPath=tmpGitRepoDirectory,
                        destPath=commitDirectory,
                        commitID=commitID,
                    )
                    bar.next()

                executor.map(_run, commits)
