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
        """Check if empty"""

        return len(self.items) == 0

    def get_items(self) -> list:
        """Get the items"""

        return self.items

    def get_metadata(self) -> list | None:
        """Get the metadata info"""

        for item in self.items:
            if "metadata" in item:
                return item["metadata"]

        return None

    def get_functions(self) -> list | None:
        """Get all the functions"""

        __functions = list()
        for item in self.items:
            if "metadata" not in item:
                __functions.append(item)

        return __functions

    def has_metadata(self) -> bool:
        """Check if metadata exists"""

        return self.get_metadata() is not None

    def dump_data(self) -> str:
        """DEBUG -> dump to YAML"""

        return yaml.dump(self.items)

    def get_comment_buffer(self, node: Node) -> list:
        """Get comment data"""

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
        """Visited a global comment"""

        __comments = self.get_comment_buffer(node)

        if len(__comments) > 0:
            if CommentTag.COMMENT_TAG_HEADER in __comments[0] or CommentTag.COMMENT_TAG_NAME in __comments[0]:
                return self.items.append({"metadata": __comments})

    def get_comments(self, node: Node) -> list:
        """Get the comments from a Node"""

        __comments = list()
        if node.comments:
            for comment in node.comments:
                __comments = self.get_comment_buffer(comment)

        return __comments

    def get_arguments(self, node: Node) -> list:
        """Get the arguments for a Method/Function"""

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
