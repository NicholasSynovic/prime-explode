from os.path import isdir
from pathlib import Path


def testIfDirectory(path: Path) -> bool:
    return isdir(s=path)
