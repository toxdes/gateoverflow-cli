# Changelog

### v0.5.0

1. Added option to hide the title block (the logo-ish box of text in green color that appears on the top.), by setting `show_title` to either true or false.
2. Added `sample_config.toml` as `package_data`, which means, default config file is no longer read from a string constant. It's read from the `default_config.toml` file which will be included in the package.
3. Refactoring, Polished UI and Bugfixes.

### v0.4.8

1. Windows related bugfixes. It should run on windows as well, without any complaints.
2. Reverted back to `webbrowser` module because, obviously, cross-platform compatibility.

### v0.4.4 - v.0.4.7

1. fixed `latest_version_check`.
2. Fixing issues with the pypi's readme file (v0.4.5)
3. Fixed bugs.
4. Help message is improved.

### v0.4.3

1. Added version argument, on any of the `-v`, `-version`, `--version`, shows the current version of the program.
2. Added latest version check to crawler too, cause why not!

### v0.4.2

1. Minor bugfixes cause I've not tested it enough, I'm fixing the bugs as I encounter them, through minor releases.
2. Most of the things done here are self explanatory. I could mention them through verbose commiting but vscode doesn't support it yet and I'm too lazy to use terminal for it.
3. Introduced emotes in readme I don't even know if it will be a good idea. :(

### v0.4.0

1. Added support for user defined configuration file, using `config.toml` for it. The program now has it's own directory where the `.db` file resides, and the `database_name` field of the `config` can be used to specify which `db` should be used.
2. Added a `user` table, which stores information about the database itself, currently this only includes `username` and `name` but later it will be helpful while merging various databases.
3. The output of the `#` commands is now tabulated.
4. Logger now has `t` parameter to quickly debug whether if a point is reachable during execution.
5. Introduced colors for the text with ANSI escape characters, for debug as well as normal output. It is still WIP, but hey.
6. A lot of bugfixes and code refactoring.

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
