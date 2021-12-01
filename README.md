## Lua Pretty Docs

This is a python program that will parse Lua file comments and output them into a nice markdown file.

### Installation

This is the standard way to install `luaprettydoc` .

Run `pip install -U git+git://github.com/TurtleP/luaprettydoc.git`

> Note: On Linux, you may need to run as `sudo` . Some systems use `pip3` instead, so you might need to use that instead.

### Documentation Tags

To document a function, simply make a multiline comment with one (or more) of the following Tags.

| Tag           | Description                                    | Notes                                         |
|---------------|------------------------------------------------|-----------------------------------------------|
| `@type` | Type of file ( `Library` or `Module` )         | Metadata only. If omitted, uses `Module` |
| `@name` | Name of the `@type` (e.g. library/module name) | Metadata only. If omitted, uses the filename. |
| `@brief` | Short description                              |                                               |
| `@param` | Parameter type and description                 |                                               |
| `@note` | Any special notes about the function           |                                               |
| `@return` | Return type and description                    |                                               |
| `@exclude` | Exclude the function from markdown output      |                                               |
| `@definition` | Override the default function definition       |                                               |
