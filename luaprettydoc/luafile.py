import pprint
from pathlib import Path

from luaparser import ast
from luaparser.astnodes import Node

from .visitor import Visitor


class LuaFile:

    # Docs path
    DocFilePath = "docs"

    # File header
    FileHeader = "## {} File Reference,"

    def __init__(self, filepath: Path):
        print(f"Parsing {filepath.name}..")

        __tree_info = None
        with open(filepath.resolve(), "r") as file:
            __tree_info = ast.parse(file.read())

        self.filepath = filepath
        self.buffer = LuaFile.FileHeader.format(filepath.name)

        # Visit Comments, Methods, Functions, and Local Functions
        visitor = Visitor()
        visitor.visit(__tree_info)

        self.output = True
        if visitor.is_empty():
            self.output = False

        if self.output:
            _printer = pprint.PrettyPrinter(indent=4)
            _printer.pprint(visitor.get_items())

        # self.buffer += str(visitor.get_buffer())

    def fetch_file_summary(self, node: Node):
        print(node)

    def export(self):
        if not self.output:
            return

        __filename = f"{LuaFile.DocFilePath}/{self.filepath.stem}.md"
        # with open(__filename, "w") as file:
        #     file.write(self.buffer)
