import re
from enum import Enum


class CommentTag(str, Enum):
    COMMENT_TAG_HEADER = "@header"
    """Header config name (default: 'Module')"""

    COMMENT_TAG_FILE = "@module"
    """Module/Header name (default: filename)"""

    COMMENT_TAG_BRIEF = "@brief"
    """Short description (default: 'No description available.')"""

    COMMENT_TAG_PARAM = "@param"
    """Parameter type and description"""

    COMMENT_TAG_RETURN = "@return"
    """Return type and description"""

    COMMENT_TAG_NOTE = "@note"
    """Additional notes"""

    COMMENT_TAG_EXCLUDE = "@exclude"
    """Excludes the function from being markdown'd"""

    @staticmethod
    def get_tag_line(line: str, group_id: int = 0) -> str | None:
        """Get the line from the comment that matches the regex search.\n
        It's actually quite hilarious."""

        for comment_type in CommentTag:
            __pattern = rf"{comment_type.value}\s(.+)"
            __match = re.search(__pattern, line)

            if __match and len(__match.groups()) > 0:
                return __match.group(group_id)

        return None
