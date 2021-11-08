import shutil
import sys
from os import mkdir
from pathlib import Path

from .luafile import LuaFile


# If there's no args, we want
# to set up the cwd as the path
# otherwise, use the provided one
def main(commandline: list = None):
    __scan_dir = None
    if len(commandline) == 1:
        if Path("docs").exists() and commandline[0] == "clean":
            return shutil.rmtree("docs")

        __scan_dir = Path(commandline[0]).resolve()
    else:
        __scan_dir = Path().cwd()

    Path("docs").mkdir(exist_ok=True)
    for tree_iter in __scan_dir.rglob("*.lua"):
        _ = LuaFile(tree_iter, True).export()


if __name__ == "__main__":
    main(sys.argv[-1:])
