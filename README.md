## Lua Pretty Docs

This is a python program that will parse Lua file comments and output them into a nice markdown file.

### Installation

This is the standard way to install `luaprettydoc` . However, *stable* releases will be published/announced accordingly on the Releases page.

Run `pip install -U git+git://github.com/TurtleP/luaprettydoc.git`

> Note: On Linux, you may need to run as `sudo` . Some systems use `pip3` instead, so you might need to use that instead.

### Documentation Tags

To document a function, simply make a multiline comment with one (or more) of the following Tags.

| Tag       | Description                          | Notes                                                               |
|-----------|--------------------------------------|---------------------------------------------------------------------|
| `@module` | Name of the module                   | Typically created at the top of the file. Otherwise, uses filename. |
| `@brief` | Short description                    |                                                                     |
| `@param` | Parameter type and description       |                                                                     |
| `@note` | Any special notes about the function |                                                                     |
| `@return` | Return type and description          |                                                                     |
