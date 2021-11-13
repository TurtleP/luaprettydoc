import re

import yaml
from luaparser.ast import ASTVisitor
from luaparser.astnodes import Comment, Index, Invoke, Name, Node, Varargs

from .tags import CommentTag, get_tag_line


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
                return item["metadata"]

        return None

    def get_functions(self) -> list | None:
        __functions = list()
        for item in self.items:
            if "metadata" not in item:
                __functions.append(item)

        return __functions

    def has_metadata(self) -> bool:
        return self.get_metadata() is not None

    def dump_data(self) -> str:
        return yaml.dump(self.items)

    def get_comment_buffer(self, node: Node) -> list:
        __result = list()
        __lines = list()

        if isinstance(node, Comment):
            if node.is_multi_line:
                __lines = node.s.split("\n")

        for line in __lines:
            __data = get_tag_line(line)

            if __data:
                __result.append(__data)

        return __result

    def visit_Comment(self, node):
        """If it's a global comment, check if it's metadata"""

        __comments = self.get_comment_buffer(node)

        if len(__comments) > 0:
            if CommentTag.COMMENT_TAG_FILE in __comments[0]:
                return self.items.append({"metadata": __comments})

    def get_comments(self, node: Node) -> list:
        __comments = list()
        if node.comments:
            for comment in node.comments:
                __comments = self.get_comment_buffer(comment)

        return __comments

    def get_arguments(self, node: Node) -> list:
        __arguments = list()

        for element in node.args:
            if isinstance(element, Name):
                __arguments.append(element.id)
            elif isinstance(element, Varargs):
                __arguments.append("...")

        return __arguments

    def visit_Method(self, node):
        """Called when the Visitor visits a Method\n
        (`function source:name(args) ... end`)"""

        __source = node.source.id
        __method = node.name.id

        __comments = self.get_comments(node)
        __arguments = self.get_arguments(node)

        __metadata = {"source": __source,
                      "name": __method, "args": __arguments,
                      "comments": __comments, "notation": ":"}

        self.items.append(__metadata)

    def visit_Function(self, node):
        """Called when the Visitor visits a Function\n
        (`function name(args) ... end`)"""

        __source, __name = "", None
        __arguments, __comments = None, None
        __notation = ""

        if isinstance(node.name, Name):
            __name = node.name.id
        elif isinstance(node.name, Index):
            __name = node.name.idx.id
            __source = node.name.value.id
            __notation = "."

        __comments = self.get_comments(node)
        __arguments = self.get_arguments(node)

        __metadata = {"source": __source,
                      "name": __name, "args": __arguments,
                      "comments": __comments, "notation": __notation}

        self.items.append(__metadata)
