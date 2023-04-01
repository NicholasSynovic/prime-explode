import subprocess
from collections import OrderedDict
from pathlib import Path
from subprocess import PIPE, CompletedProcess
from typing import List

from pygit2 import GIT_SORT_REVERSE, Repository, Walker
from pygit2.repository import Branches


def getRepoPath(path: Path) -> Path:
    return Path(path, ".git")


def getBranchesList(path: Path, remote: bool = True) -> List[str]:
    repo: Repository = Repository(path)
    branches: Branches = repo.branches

    localBranches: List[str] = list(branches.local)
    remoteBranches: List[str] = []

    if remote:
        remoteBranches: List[str] = [
            "/".join(branch.split("/")[1::])
            for branch in list(branches.remote)
            if branch != "origin/HEAD"
        ]

    data: List[str] = localBranches + remoteBranches

    return list(OrderedDict.fromkeys(data).keys())


def checkoutBranch(path: Path, branch: str) -> None:
    cmd: str = f"git -C {path.resolve()} checkout {branch}"
    subprocess.run(args=cmd, stdout=PIPE, stderr=PIPE, shell=True)


def getCommitWalker(path: Path) -> Walker:
    repo: Repository = Repository(path=path)
    return repo.walk(repo.head.target, GIT_SORT_REVERSE)


def cloneBranch(srcPath: Path, destPath: Path, branch: str) -> Path:
    destPath: Path = Path(destPath, branch)
    cmd: str = (
        f"git clone --branch {branch} --quiet {srcPath.resolve()} {destPath.resolve()}"
    )
    subprocess.run(args=cmd, stdout=PIPE, shell=True)
    return destPath
