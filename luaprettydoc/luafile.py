import pprint
from pathlib import Path

from luaparser import ast
from luaparser.astnodes import Node

from .visitor import Visitor


class LuaFile:

    # Docs path
    DocFilePath = "docs"

    # File header
    FileHeader = "## Module"

    def __init__(self, filepath: Path, debug: bool = False):
        print(f"Parsing {filepath.name}..")

        __tree_info = None
        with open(filepath.resolve(), "r") as file:
            __tree_info = ast.parse(file.read())

        self.filepath = filepath

        # Visit Comments, Methods, Functions, and Local Functions
        visitor = Visitor()
        visitor.visit(__tree_info)

        # Handle the data
        __header_ref = filepath.name
        if visitor.has_metadata():
            __metadata = visitor.get_metadata()

            __header_ref = __metadata[0]

        self.buffer = f"{LuaFile.FileHeader} {__header_ref}"

        self.output = True
        if visitor.is_empty():
            self.output = False
        else:
            if debug:
                self.debug_export(visitor, filepath)

        __filename = filepath.with_suffix("").name
        self.outname = f"{LuaFile.DocFilePath}/{__filename}.md"

    def debug_export(self, visitor, filepath):
        Path("docs/test").mkdir(exist_ok=True)
        with open(f"docs/test/{filepath.stem}.yaml", "w") as file:
            file.write(visitor.dump_data())

    def export(self):
        if not self.output:
            return

        with open(self.outname, "w") as file:
            file.write(self.buffer)
