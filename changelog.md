# Changelog

### v0.3.1

1. listing recents shows title and description of the question now. Added a `column_width` field to state in order to ellipsis the longer rows.
2. added a field `crawl_attempts` in order to detect if the `question_id` is invalid. The `question_id`s are invalid if we fail to scrape their details for a certain number of times defined by `state.crawl_attempts_limit`.

### v0.3.0

1. Experimenting with `pip` to make a runnable CLI tool. Prior to this, it would require to be run via `pip -m gateoverflow`.
2. Orgainzed README.
3. Parser barely works, as specified in [Parser Commands](./README.md#usage)
4. Major refactor, queries and debug-outputs.
5. debug mode improved.

### v0.2.0

1. updated makefile to have a `build` target
2. changed behaviour of `ls` command. Now it only lists recents
3. refactor, and removing unnecessary code

### v0.0.3, v0.0.4

1. testing and figuring out pypi dependencies, works from scratch on `termux` so far.

### v0.0.2

1. super early release, stuff is broken, trying out `pip`.
2. basic things work, tags are broken
3. still figuring out stuff

### v0.0.1

1. Crawler routine added, can be used by `crawler` command. Stores question title, description and preview image.
2. added `debug-toggle` command to show/hide debug output.
3. added new dependancy of `tabulate` to pretty print tables (maybe with colors?)
4. tags relation (WIP)
