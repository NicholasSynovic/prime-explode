import subprocess
from os.path import isdir
from pathlib import Path
from subprocess import PIPE, CompletedProcess


def testIfGitRepo(path: Path) -> bool:
    gitDir: Path = Path(path, ".git")
    return isdir(s=gitDir)


def checkoutHEAD(repo: Path) -> None:
    cmd: str = f"git -C {repo.resolve()} checkout HEAD --quiet"
    process: CompletedProcess = subprocess.run(args=cmd, stdout=PIPE, shell=True)
