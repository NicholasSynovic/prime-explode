import subprocess
from os.path import isdir
from pathlib import Path
from subprocess import PIPE, CompletedProcess


def getRepoPath(path: Path) -> Path:
    return Path(path, ".git")


def checkoutHEAD(repo: Path) -> None:
    cmd: str = f"git -C {repo.resolve()} checkout HEAD --quiet"
    subprocess.run(args=cmd, stdout=PIPE, shell=True)
