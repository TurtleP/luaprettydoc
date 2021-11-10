import pprint
import re
from enum import Enum
from pathlib import Path

from luaparser import ast

from .templates import Templates
from .visitor import CommentItem, Visitor


class LuaFile:

    # Docs path
    DocFilePath = "docs"

    def __init__(self, filepath: Path, debug: bool = False):
        """Scans a Lua file for parsing"""

        __tree_info = None
        with open(filepath.resolve(), "r") as file:
            __tree_info = ast.parse(file.read())

        self.filepath = filepath

        # Visit Comments, Methods, Functions, and Local Functions
        visitor = Visitor()
        visitor.visit(__tree_info)

        # Handle the data
        self.module = filepath.name
        self.module_brief = "No description available"

        if visitor.has_metadata():
            __metadata = visitor.get_metadata()

            self.module = __metadata[0].split(CommentItem.COMMENT_FILE)[1]
            self.module_brief = __metadata[1].split(
                CommentItem.COMMENT_BRIEF)[1]

        self.buffer = Templates.TEMPLATE_START.format(
            self.module, self.module_brief)

        __functions = visitor.get_functions()
        for function_info in __functions:
            self.create_function(function_info)

        # Output
        self.output = True
        if visitor.is_empty():
            self.output = False
        else:
            if debug:
                self.debug_export(visitor, filepath)

        __filename = filepath.with_suffix("").name
        self.outname = f"{LuaFile.DocFilePath}/{__filename}.md"

    def handle_parameter(self, param: str) -> str:
        __info = Visitor.prepare_data(
            param.split(CommentItem.COMMENT_PARAM))[1]

        return f"  - {__info}\n"

    def handle_note(self, note: str) -> str:
        __info = Visitor.prepare_data(
            note.split(CommentItem.COMMENT_NOTE))[1]

        return f"{__info } "

    def handle_return(self, retval: str) -> str:
        __info = Visitor.prepare_data(
            retval.split(CommentItem.COMMENT_RETURN))[1]

        return f"  - {__info}\n"

    def create_function(self, data):
        """Creates a Function's markdown data"""

        __args = ", ".join(data["args"])
        __call = f"### {data['source']}:{data['name']}({__args})\n\n"

        __brief, __params, __notes, __return = None, "", "", ""
        for comment in data["comments"]:
            if CommentItem.COMMENT_BRIEF in comment:
                __brief = Visitor.prepare_data(
                    comment.split(CommentItem.COMMENT_BRIEF))[1]
            elif CommentItem.COMMENT_PARAM in comment:
                __params += self.handle_parameter(comment)
            elif CommentItem.COMMENT_NOTE in comment:
                __notes += self.handle_note(comment)
            elif CommentItem.COMMENT_RETURN in comment:
                __return += self.handle_return(comment)

        self.buffer += __call

        __output = "_{}_\n\n"

        if __brief:
            self.buffer += __output.format(__brief)
        else:
            self.buffer += __output.format("No description available.")

        if __params:
            self.buffer += "**Arguments**\n"
            self.buffer += f"{__params}\n"

        if __notes:
            self.buffer += f"> Note: {__notes}\n\n"

        if __return:
            self.buffer += "**Returns**\n"
            self.buffer += f"{__return}\n"

        self.buffer += "---\n\n"

    def debug_export(self, visitor, filepath):
        Path("docs/test").mkdir(parents=True, exist_ok=True)
        with open(f"docs/test/{filepath.stem}.yaml", "w") as file:
            file.write(visitor.dump_data())

    def export(self):
        if not self.output:
            return

        with open(self.outname, "w", encoding="utf-8") as file:
            file.write(self.buffer)
