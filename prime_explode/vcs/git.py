import subprocess
from collections import OrderedDict
from os.path import isdir
from pathlib import Path
from subprocess import DEVNULL, PIPE, CompletedProcess
from typing import List, Tuple

from pygit2 import Repository
from pygit2.repository import Branches


def getRepoPath(path: Path) -> Path:
    return Path(path, ".git")


def getBranchesList(repo: Repository, remote: bool = True) -> set[str]:
    remoteBranches: List[str] = []
    branches: Branches = repo.branches

    localBranches: List[str] = list(branches.local)

    if remote:
        remoteBranches: List[str] = [
            "/".join(branch.split("/")[1::])
            for branch in list(branches.remote)
            if branch != "origin/HEAD"
        ]

    data: List[str] = localBranches + remoteBranches

    return list(OrderedDict.fromkeys(data).keys())
