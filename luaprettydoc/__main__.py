import sys
from argparse import ArgumentParser
from datetime import datetime
from os import mkdir
from pathlib import Path

from . import __version__
from .luafile import LuaFile


# If there's no args, we want
# to set up the cwd as the path
# otherwise, use the provided one
def main(commandline: list = None):
    parser = ArgumentParser("luaprettydoc")

    parser.add_argument("scan_dir", type=str, help="root directory to scan")

    parsed_args = parser.parse_args()

    __scan_dir = Path(parsed_args.scan_dir)
    (__scan_dir / "docs").mkdir(exist_ok=True)

    for tree_iter in __scan_dir.rglob("*.lua"):
        _ = LuaFile(tree_iter, True).export(
            __version__, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main(sys.argv)
