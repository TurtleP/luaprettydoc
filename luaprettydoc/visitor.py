import re
from enum import Enum

from luaparser.ast import ASTVisitor
from luaparser.astnodes import Invoke, Name, Varargs


class CommentItem(str, Enum):
    COMMENT_FILE = "@file"
    COMMENT_BRIEF = "@brief"
    COMMENT_PARAM = "@param"
    COMMENT_RETURN = "@return"
    COMMENT_NOTE = "@note"


class Visitor(ASTVisitor):

    def __init__(self) -> None:
        super().__init__()

        self.last_method = None
        self.items = list()

    def handle_comment_buffer(self, comment_line) -> str | None:
        __match = None
        for comment_type in CommentItem:
            __pattern = rf"{comment_type.value}\s(.+)"
            __match = re.search(__pattern, comment_line)

            if __match:
                break

        if __match:
            return __match.group(0)

    def visit_Comment(self, node):
        if node.is_multi_line:
            __comment_line = node.s.split("\n")
            __comment_data = list()

            for line in __comment_line:
                __data = self.handle_comment_buffer(line)

                if __data:
                    __comment_data.append(__data)

            if self.last_method is not None and len(__comment_data) > 0:
                __metadata = {"comments": __comment_data}
                if CommentItem.COMMENT_FILE in __comment_data[0]:
                    self.items.append({"metdata": __metadata})
                else:
                    dict.update(self.items[self.last_method], __metadata)

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def get_items(self):
        return self.items

    def visit_Method(self, node):
        __source = node.source.id
        __method = node.name.id

        __args = list()
        for element in node.args:
            if isinstance(element, Name):
                __args.append(element.id)
            elif isinstance(element, Varargs):
                __args.append("...")

        __metadata = {"source": f"{__source}",
                      "name": f"{__method}", "args": str(__args), "comments": None}

        self.last_method = len(self.items)
        self.items.append(__metadata)

    def visit_Function(self, node):
        # print(node.name)
        pass

    def visit_LocalFunction(self, node):
        # print(node.name, node.args)
        pass
