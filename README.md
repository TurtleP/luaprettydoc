## Lua Pretty Docs

This is a python program that will parse Lua file comments and output them into a nice markdown file.

### Documentation Formats

To document a function, simply make a multiline comment with one (or more) of the following Tags.

| Tag       | Description                          | Notes                                                              |
|-----------|--------------------------------------|--------------------------------------------------------------------|
| `@module` | Name of the module                   | Typically created at the top of the file. Otherwise, uses filename |
| `@brief` | Short description                    |                                                                    |
| `@param` | Parameter type and description       |                                                                    |
| `@note` | Any special notes about the function |                                                                    |
| `@return` | Return type and description          |                                                                    |
