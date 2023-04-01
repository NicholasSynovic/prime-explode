from argparse import Namespace

from prime_explode.utils import filesystem
from prime_explode.vcs import git


def main(args: Namespace) -> None:
    # Steps:

    # 1. Check if the src directory exists
    # 2. Check if the src directory contains a git repo
    # If not, exit with reason
    # 3. Check if the dest directory exists
    # If it does, exit with reason
    # 5. Checkout the repository to the HEAD commit
    # 4. Get a list of branches

    if filesystem.testIfDirectory(path=args.gitSrc) is False:
        print(f"{args.gitSrc} is not a valid source directory")
        exit(code=1)

    if git.testIfGitRepo(path=args.gitSrc) is False:
        print(f"{args.gitSrc} is not a valid Git repository")
        exit(code=2)

    if filesystem.testIfDirectory(args.gitDest):
        print(f"{args.gitDest} already exists.")
        exit(code=3)
