# Python project to manage gateoverflow links.

# Requirements

- python3
- sqlite3

# Todo

- Create a CLI that opens a link in the browser, when question id is provided.
- Creating lists for questions, categorizing them.
- Modes: i.e. in open mode, on number input, the link is automatically opened.
- usage of arrow keys to select, make UX amazing.
- fetch all question from lists
- a "sync" mechanism that will be used to upload the db file to web, and will be shared across somehow.
- maybe firebase
- add gifs of usage

# CLI Commands

| Command     | Description                                  | Status             |
| ----------- | -------------------------------------------- | ------------------ |
| `q`         | Alias to quit. Exit the program normally.    | :heavy_check_mark: |
| `h`         | Alias to help. Shows available commands.     | :heavy_check_mark: |
| `l`         | Alias to tags. List of all tags.             | :x:                |
| `r`         | Alias to Recents. Recently opened questions. | :x:                |
| `o`         | Alias to open-mode. Go into open mode.       | :x:                |
| `quit`      | Exit the program normally.                   | :heavy_check_mark: |
| `help`      | Shows available commands.                    | :heavy_check_mark: |
| `clear`     | Clear output screen.                         | :heavy_check_mark: |
| `tags`      | List of all tags.                            | :x:                |
| `open-mode` | Go into open-mode.                           | :x:                |
