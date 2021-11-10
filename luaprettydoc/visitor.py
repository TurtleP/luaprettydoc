import re
from enum import Enum

import yaml
from luaparser.ast import ASTVisitor
from luaparser.astnodes import Comment, Invoke, Name, Node, Varargs


class CommentItem(str, Enum):
    COMMENT_FILE = "@module"
    COMMENT_BRIEF = "@brief"
    COMMENT_PARAM = "@param"
    COMMENT_RETURN = "@return"
    COMMENT_NOTE = "@note"


class Visitor(ASTVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.items = list()

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def get_items(self) -> list:
        return self.items

    def get_metadata(self) -> list | None:
        for item in self.items:
            if "metadata" in item:
                return Visitor.prepare_data(item["metadata"])

        return None

    def get_functions(self) -> list | None:
        __functions = list()
        for item in self.items:
            if "metadata" not in item:
                __functions.append(item)

        return __functions

    @staticmethod
    def prepare_data(data: list) -> list:
        return [re.sub(r"\s+", "", x, 1) for x in data]

    def has_metadata(self) -> bool:
        return self.get_metadata() is not None

    def dump_data(self) -> str:
        return yaml.dump(self.items)

    def handle_comment_buffer(self, comment_line: str) -> str | None:
        for comment_type in CommentItem:
            __pattern = rf"{comment_type.value}\s(.+)"
            __match = re.search(__pattern, comment_line)

            if __match:
                return __match.group(0)

        return None

    def get_comment_buffer(self, node: Node) -> list:
        __result = list()

        if isinstance(node, Comment):
            if node.is_multi_line:
                __lines = node.s.split("\n")

                for line in __lines:
                    __data = self.handle_comment_buffer(line)

                    if __data:
                        __result.append(__data)

        return __result

    def visit_Comment(self, node):
        """If it's a global comment, check if it's metadata"""
        __comments = self.get_comment_buffer(node)

        if len(__comments) > 0:
            if CommentItem.COMMENT_FILE in __comments[0]:
                return self.items.append({"metadata": __comments})

    def visit_Method(self, node):
        """Methods can have comments outside! Use this!"""
        __source = node.source.id
        __method = node.name.id
        __comments = list()

        if node.comments:
            for comment in node.comments:
                __comments = self.get_comment_buffer(comment)

        __args = list()
        for element in node.args:
            if isinstance(element, Name):
                __args.append(element.id)
            elif isinstance(element, Varargs):
                __args.append("...")

        __metadata = {"source": f"{__source}",
                      "name": f"{__method}", "args": __args,
                      "comments": __comments}

        self.last_method = len(self.items)
        self.items.append(__metadata)

    def visit_Function(self, node):
        # print(node.name)
        pass

    def visit_LocalFunction(self, node):
        # print(node.name, node.args)
        pass
