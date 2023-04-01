import subprocess
from os.path import isdir
from pathlib import Path
from subprocess import DEVNULL, PIPE, CompletedProcess
from typing import List


def getRepoPath(path: Path) -> Path:
    return Path(path, ".git")


def getBranches(repo: Path) -> List:
    pass


def checkoutHEAD(repo: Path) -> None:
    cmd: str = f"git -C {repo.resolve()} checkout HEAD --quiet"
    subprocess.run(args=cmd, stdout=PIPE, stderr=DEVNULL, shell=True)
