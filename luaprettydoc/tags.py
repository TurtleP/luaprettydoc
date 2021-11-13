import re
from enum import Enum


class CommentTag(str, Enum):
    COMMENT_TAG_HEADER = "@header"
    """{@header} Header config name (default: 'Module')"""

    COMMENT_TAG_FILE = "@module"
    """{@module} Module/Header name (default: filename)"""

    COMMENT_TAG_DEFINE = "@define"
    """{@define} Definition override"""

    COMMENT_TAG_BRIEF = "@brief"
    """{@brief} Short description (default: 'No description available.')"""

    COMMENT_TAG_PARAM = "@param"
    """{@param} Parameter type and description"""

    COMMENT_TAG_RETURN = "@return"
    """{@return} Return type and description"""

    COMMENT_TAG_NOTE = "@note"
    """{@note} Additional notes"""


class CommentTagSingle(str, Enum):
    COMMENT_TAG_SINGLE_EXCLUDE = "@exclude"
    """{@exclude} Excludes the function from being markdown'd"""


def get_tag_line(line: str, group_id: int = 0) -> str | None:
    """Get the line from the comment that matches the regex search.\n
    It's actually quite hilarious."""

    for comment_type in CommentTag:
        __pattern = rf"{comment_type.value}\s(.+)"
        __match = re.search(__pattern, line)

        if __match:
            return __match.group(group_id)

    for comment_type in CommentTagSingle:
        __pattern = rf"({comment_type.value})"
        __match = re.search(__pattern, line)

        if __match:
            return __match.group(1)

    return None
