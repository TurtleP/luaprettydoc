import shutil
import sys
from argparse import ArgumentParser
from os import mkdir
from pathlib import Path

from .luafile import LuaFile


# If there's no args, we want
# to set up the cwd as the path
# otherwise, use the provided one
def main(commandline: list = None):
    parser = ArgumentParser("luaprettydoc")

    parser.add_argument("scan_dir", type=str, help="root directory to scan")
    parser.add_argument("--clean", type=bool, help="clean the docs directory")

    parsed_args = parser.parse_args()

    __scan_dir = Path(parsed_args.scan_dir)
    (__scan_dir / "docs").mkdir(exist_ok=True)

    for tree_iter in __scan_dir.rglob("*.lua"):
        _ = LuaFile(tree_iter, True).export()


if __name__ == "__main__":
    main(sys.argv)
