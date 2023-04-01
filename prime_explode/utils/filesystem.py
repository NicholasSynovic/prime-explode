from os import mkdir
from os.path import isdir
from pathlib import Path


def testIfDirectory(path: Path) -> bool:
    return isdir(s=path)


def createDirectory(path: Path) -> None:
    mkdir(path=path)
