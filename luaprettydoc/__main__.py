import sys
from datetime import datetime
from os import mkdir
from pathlib import Path

from . import __version__
from .luafile import LuaFile


# If there's no args, we want
# to set up the cwd as the path
# otherwise, use the provided one
def main(_: list = None):
    # Directory stuff
    __scan_dir = Path().cwd()

    __docs_dir = (__scan_dir / "docs")
    __docs_dir.mkdir(exist_ok=True)

    # Documentation output
    __output_dir = __docs_dir

    # Compilation date and time
    __date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for tree_iter in __scan_dir.rglob("*.lua"):
        if tree_iter.parent != __scan_dir:
            __output_dir = (__docs_dir / tree_iter.parent.stem)
            if not __output_dir.exists():
                __output_dir.mkdir(exist_ok=True)

        _ = LuaFile(__output_dir, tree_iter).export(__version__, __date_time)


if __name__ == "__main__":
    main(sys.argv)
