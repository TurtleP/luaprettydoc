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
def main(_: list = None):
    __parser = ArgumentParser("luaprettydoc", "Lua Documentation to Markdown")

    __parser.add_argument(
        "--version", action='version', version='%(prog)s {}'.format(__version__))

    __parser.add_argument("--headers",
                          action="store_true", default=False,
                          help="Only output files with proper header commentary")

    __parsed = __parser.parse_args()

    # Return early if we want only version info
    if hasattr(__parsed, "version"):
        return

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

        lua_file = LuaFile(__output_dir, tree_iter, __parsed.headers)
        lua_file.export(__version__, __date_time)


if __name__ == "__main__":
    main(sys.argv)
