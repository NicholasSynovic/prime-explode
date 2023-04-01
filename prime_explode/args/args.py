from argparse import ArgumentParser, Namespace, _SubParsersAction
from importlib.metadata import version
from pathlib import Path


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="PRIME Explode",
        usage="prime-explode",
        description="To explode a code repository into a directories organized by commit",
        epilog="Authors: Nicholas M. Synovic",
    )

    subParsers: _SubParsersAction = parser.add_subparsers(
        title="VCS Options", help="Types of VCS that are supported by this tool"
    )
    parser.add_argument(
        "-v",
        "--verson",
        action="version",
        version=f"PRIME Explode {version(distribution_name='prime-explode')}",
    )

    gitParser: ArgumentParser = subParsers.add_parser(
        name="git", help="Options for interfacing with Git repositories"
    )
    gitParser.add_argument(
        "-s",
        "--src-directory",
        type=Path,
        required=True,
        help="Directory containing the repository to explode",
        dest="gitSrc",
    )
    gitParser.add_argument(
        "-d",
        "--dest-directory",
        type=Path,
        required=True,
        help="Directory to explode into",
        dest="gitDest",
    )

    return parser.parse_args()
