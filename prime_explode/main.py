from argparse import Namespace

from prime_explode import gitMain
from prime_explode.args import args

if __name__ == "__main__":
    args: Namespace = args.getArgs()
    gitMain.main(args)
