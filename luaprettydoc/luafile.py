from pathlib import Path

from luaparser import ast

from .tags import CommentTag, CommentTagSingle, get_tag_line
from .templates import Templates
from .visitor import Visitor


class LuaFile:

    # Docs path
    DocFilePath = "docs"
    TestFilePath = Path("yaml")

    # Footer
    Footer = "_Generated by luaprettydoc {} / {}_"

    def __init__(self, output_dir: Path, filepath: Path, debug: bool = False):
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

            self.module = get_tag_line(__metadata[0], 1)
            self.module_brief = get_tag_line(__metadata[1], 1)

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
        self.outname = f"{str(output_dir)}/{__filename}.md"

    def handle_parameter_returns(self, line: str) -> str:
        """Handle when we get a @param or @return tag"""

        __param_return = get_tag_line(line, 1)

        if __param_return:
            return Templates.TEMPLATE_RETURN_PARAM.format(__param_return)

        return str()

    def handle_note(self, line: str) -> str:
        """Handle when we get a @note tag"""

        __note = get_tag_line(line, 1)

        if __note is not None:
            return __note

        return str()

    def create_function(self, data: dict) -> None:
        """Creates a Function's markdown data"""

        __args = ", ".join(data["args"])

        __call = None
        __brief, __params = None, ""
        __notes, __returns = list(), ""

        __generate_function = True
        for comment in data["comments"]:
            if CommentTag.COMMENT_TAG_BRIEF in comment:
                if __brief is None:
                    __brief = get_tag_line(comment, 1)
            elif CommentTag.COMMENT_TAG_PARAM in comment:
                __params += self.handle_parameter_returns(comment)
            elif CommentTag.COMMENT_TAG_RETURN in comment:
                __returns += self.handle_parameter_returns(comment)
            elif CommentTag.COMMENT_TAG_NOTE in comment:
                __notes.append(self.handle_note(comment))
            elif CommentTag.COMMENT_TAG_DEFINE in comment:
                if __call is None:
                    __call = Templates.TEMPLATE_DEFINE.format(
                        get_tag_line(comment, 1))
            elif CommentTagSingle.COMMENT_TAG_SINGLE_EXCLUDE in comment:
                __generate_function = False

        if __generate_function:
            if __call is None:
                __call = Templates.TEMPLATE_FUNC.format(
                    source=data["source"], index=data["notation"],
                    name=data["name"], args=__args)

            self.buffer += __call

            if __brief is None:
                __brief = "No description available."

            self.buffer += Templates.TEMPLATE_FUNC_BRIEF.format(__brief)

            if __params:
                self.buffer += Templates.TEMPLATE_PARAMS.format(__params)

            if __returns:
                self.buffer += Templates.TEMPLATE_RETURNS.format(__returns)

            if __notes:
                __notes_joined = " ".join(__notes)
                self.buffer += Templates.TEMPLATE_NOTES.format(__notes_joined)

            self.buffer += Templates.TEMPLATE_ENDING

    def debug_export(self, visitor: Visitor, filepath: Path) -> None:
        """Exports the Lua File to YAML for debug purposes"""

        __directory = Path(LuaFile.TestFilePath)
        if filepath.parent.name != Path().cwd().name:
            __directory = Path(
                f"{LuaFile.TestFilePath}/{filepath.parent.name}")

        __directory.mkdir(parents=True, exist_ok=True)
        __output = __directory / filepath.with_suffix('.yml').name

        with open(__output, "w") as file:
            file.write(visitor.dump_data())

    def export(self, version: str, date: str) -> None:
        """Exports the Lua File to Markdown"""

        if not self.output:
            return

        with open(self.outname, "w", encoding="utf-8") as file:
            print(f"{self.buffer}{LuaFile.Footer.format(version, date)}", file=file)
