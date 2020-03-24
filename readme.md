# Python project to manage gateoverflow links.

# Requirements

- python3
- sqlite3
- dateutil
- tabulate

# Todo

- Create a CLI that opens a link in the browser, when question id is provided.
- Creating lists for questions, categorizing them.
- Modes: i.e. in open mode, on number input, the link is automatically opened. **Edit:** way too trivial so added as default. Cannot think of any other mode for now so...
- usage of arrow keys to select, make UX amazing.
- fetch all question from lists
- a "sync" mechanism that will be used to upload the db file to web, and will be shared across somehow.
- create a gui maybe a web app that starts a http browser locally and opens a link in browser, like expo does?
- maybe firebase
- add gifs of usage

# Done

- CLI (check status of individual commands below)
- crawler routine for scraping metadata of each question, which will be important later on.

# CLI Commands

| Command     | Description                                  | Status             |
| ----------- | -------------------------------------------- | ------------------ |
| `q`         | Alias to quit. Exit the program normally.    | :heavy_check_mark: |
| `h`         | Alias to help. Shows available commands.     | :heavy_check_mark: |
| `l`         | Alias to tags. List of all tags.             | :x:                |
| `r`         | Alias to Recents. Recently opened questions. | :x:                |
| `o`         | Alias to open-mode. Go into open mode.       | :heavy_check_mark: |
| `quit`      | Exit the program normally.                   | :heavy_check_mark: |
| `crawler`   | Update question data(title and description). | :heavy_check_mark: |
| `help`      | Shows available commands.                    | :heavy_check_mark: |
| `clear`     | Clear output screen.                         | :heavy_check_mark: |
| `tags`      | List of all tags.                            | :x:                |
| `open-mode` | Go into open-mode.                           | :heavy_check_mark: |

# Changelog

1. Crawler routine added, can be used by `crawler` command. Stores question title, description and preview image.
2. added `debug-toggle` command to show/hide debug output. (WIP).
3. added new dependancy of `tabulate` to pretty print tables (maybe with colors?)
4. tags relation (WIP)
