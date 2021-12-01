import sys
from argparse import ArgumentParser
from datetime import datetime
from os import mkdir, scandir
from pathlib import Path

from . import __version__
from .luafile import LuaFile


def get_docs_dir() -> Path:
    new_path = Path().cwd() / "docs"
    new_path.mkdir(exist_ok=True)

    return new_path


def main(_: list = None):
    __parser = ArgumentParser("luaprettydoc", "Lua Documentation to Markdown")

    __parser.add_argument(
        "--version", action='version', version='%(prog)s {}'.format(__version__))

    __parser.add_argument("--headers",
                          action="store_true", default=False,
                          help="Only output files with proper header commentary")

    __group = __parser.add_mutually_exclusive_group()

    __group.add_argument("--dir", "-d")
    __group.add_argument("--file", "-f")

    __parsed = __parser.parse_args()

    # Return early if we want only version info
    if hasattr(__parsed, "version"):
        return

    # Compilation date and time
    __date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Directory stuff
    if __parsed.dir:
        __scan_dir = Path(__parsed.dir) or Path().cwd()

        if not __scan_dir.exists():
            return print(f"Cannot generate docs. Directory '{__scan_dir}' does not exist.")

        __base = get_docs_dir()

        # Documentation output
        __output_dir = __base

        for tree_iter in __scan_dir.rglob("*.lua"):
            if tree_iter.parent != __scan_dir:
                __output_dir = (__base / tree_iter.parent.stem)

            lua_file = LuaFile(__output_dir, tree_iter, __parsed.headers)
            lua_file.export(__version__, __date_time)
    elif __parsed.file:
        __file = Path(__parsed.file).resolve()

        if not __file.exists():
            return print(f"Cannot generate docs. File '{__file}' does not exist.")

        __base = get_docs_dir()

        if __file.parent != __base.parent:
            __base = (__base / __file.parent.stem)

        LuaFile(__base, __file, __parsed.headers).export(
            __version__, __date_time)


if __name__ == "__main__":
    main(sys.argv)
