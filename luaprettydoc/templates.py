from enum import Enum


class Templates(str, Enum):
    TEMPLATE_START = ("# Module {}"
                      "\n\n"
                      "_{}_"
                      "\n\n"
                      "## Functions"
                      "\n\n")

    TEMPLATE_DEFINE = ("### {source}{index}{name}({args})"
                       "\n\n")

    TEMPLATE_FUNC_BRIEF = ("_{}_"
                           "\n\n")

    TEMPLATE_PARAMS = ("**Argument(s)**:"
                       "\n"
                       "{}"
                       "\n\n")

    TEMPLATE_RETURNS = ("**Return(s)**:"
                        "\n"
                        "{}"
                        "\n\n")

    TEMPLATE_RETURN_PARAM = " - {}"

    TEMPLATE_NOTES = ("> Note: {} "
                      "\n\n")
