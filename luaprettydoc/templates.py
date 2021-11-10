from enum import Enum


class Templates(str, Enum):
    TEMPLATE_START = "# Module {}\n" \
                     "_{}_\n\n" \
                     "## Functions\n\n"
