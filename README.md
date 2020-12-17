# Gateoverflow CLI :tada:

open / manage links with the question ids(which are right there, next to question title), create new lists of questions, update them etc.
The codebase is _heavily_ inspired by [this](https://github.com/EnterpriseQualityCoding/FizzBuzzEnterpriseEdition) fizzbuzz implementation.

#### Latest Release v0.5.0 :zap:

Available to install through pip [(pypi)](https://pypi.org/project/gateoverflow).

Read [full changelog](./changelog.md)

# Table of Contents :clipboard:

- [Gateoverflow CLI](#gateoverflow-cli-tada) - [Latest Release v0.4.6](#latest-release-v046-zap)
- [Table of Contents](#table-of-contents-clipboard)
- [Motivation](#motivation)
- [Installation](#installation-rocket)
- [Requirements](#requirements-hammer_and_wrench)
- [Changelog](#changelog-pencil)
  - [v0.5.0](#v050)
  - [v0.4.8](#v048)
  - [v0.3.1](#v031)
  - [v0.2.0](#v020)
- [Usage](#usage-fire)
  - [Parser Commands](#parser-commands)
  - [Commands](#commands)
  - [Usage Examples](#usage-examples)
- [Future](#future)
- [Release Checklist](#release-checklist-pencil2)

# Motivation

Scanning QR codes from the book is really inefficient, so is the `Lists` feature of Gateoverflow Website.
With this tool, one can open / manage those links with the question ids(which are right there, next to question title), create new lists (called as `tags` here cause it's one too many letters shorter than `lists`) of questions.

But this wasn't really the motivation, since it can be just done with a simple script, if I wanted to.
I just wanted to create this project to know how far I can push myself to do a _real_ project, which involves developing AND distributing a python project. Hope I live up to this.

I think I'll write more about this later.

# Installation :rocket:

1. Install [python](https://www.python.org/downloads/). You can skip this step if you already have python installed.

2. Make sure you have `pip` installed by executing

```sh
$ python -m pip --version
```

If it says something like "Module not found: pip", then you should install it.

2. Open Command Prompt / Terminal, and execute

```sh
$ pip install gateoverflow
```

3. Done! Now you can use this tool by opening a Command Prompt / Terminal and running

```sh
$ gateoverflow
```

The supported commands and howto's are in [usage](#usage-fire) section.

### Preview Release

**Note** - Try this only if you know what you're doing.

If you want to install a super early alpha release, which will be on `dev` branch.
You can do,

```sh
$ pip install git+https://github.com/toxdes/gateoverflow-cli.git@dev
```

# Requirements :hammer_and_wrench:

Don't worry about this unless you are going to develop.

- `python >= 3.6`
- `sqlite3`
- `python-dateutil`
- `requests`
- `tabulate`
- `toml`
- `setuptools >= 38.6.0`
- `wheel >= 0.31.0`
- `twine 1.11.0`

# Changelog :pencil:

### v0.5.0

1. Added option to hide the title block (the logo-ish box of text in green color that appears on the top.), by setting `show_title` to either true or false.
2. Added `sample_config.toml` as `package_data`, which means, default config file is no longer read from a string constant. It's read from the `default_config.toml` file which will be included in the package.
3. Refactoring, Polished UI and Bugfixes.

### v0.4.8

1. Added support for user defined configuration file, uses `config.toml` for it.
2. The program now has it's own `project_home` directory.
3. Added a `user` table, which stores meta information about the database.
4. Introduced colors for the text with ANSI escape characters
5. Bugfixes, refactor and gucci.

### v0.3.1

1. listing recents shows title and description of the question now.
2. delete possibly invalid questions
3. Parser barely works, as specified in [link](###parser-commands)
4. Major refactor, queries and debug-outputs.
5. debug mode.
6. Available on PyPI now. Yay!

Read [full changelog](./changelog.md)

# Usage :fire:

### Parser Commands

According to [this](https://github.com/toxdes/opengate/issues/4#issuecomment-612046118) comment, it is just convinient to use the commands as following.

1. If the input command is a list of comma/space separated integers, they are treated as question ids, and will be opened in the browser.
2. If the input command is `#` or `tags`, all created tags are listed.
3. If input command is mix of tags and question ids, then all of the questions are added to respective tags. If some of the mentioned tags do not exist, then the user is interactively prompted to create them.
4. If input command only contains tags, then list of questions with repective tags are shown.

### Commands

| Command        | Description                                                                                                | Status      |
| -------------- | ---------------------------------------------------------------------------------------------------------- | ----------- |
| `#`            | Alias to `tags`. Show list of tags.                                                                        | Implemented |
| `q`            | Alias to `quit`. Exit the program normally.                                                                | Implemented |
| `h`            | Alias to `help`. Shows available commands.                                                                 | Implemented |
| `ls`           | Alias to list.                                                                                             | Implemented |
| `quit`         | Exit the program normally.                                                                                 | Implemented |
| `tags`         | Show list of tags.                                                                                         | Implemented |
| `debug-toggle` | Enable/Disable debug output.(Default is disabled, _unless_ the program is executed with `-d` or `--debug`) | Implemented |
| `crawler`      | Update questions database(title and description).                                                          | Implemented |
| `help`         | Shows available commands.                                                                                  | Implemented |
| `clear`        | Clear output screen.                                                                                       | Implemented |

### Usage Examples

Suppose the link to the question is `https://gateoverflow.in/6969`, then the question ID in this case is `6969`, wherever the word `Question ID` is mentioned in this context.

- `2345,2323,4344, #important` - would add questions `2345,2323,4344` to `#important`.
- `#wrongly-attempted` - would list the questions in `#wrongly-attempted`, sorted with mostly visited.
- `tags` would list all the available tags. `#recent` would be a default tag, which would store all opened `questions`.
- Questions could even be added to multiple tags at the same time by doing something like `2424,23232,3234, #important, #good, #hard` to add those questions to specified tags.
- `create` would create a new tag. E.g. `create #not-so-cool` to create a tag named `not-so-cool`.

# Future

I'm planning to add the following features, assuming I overcome the biggest challenge of not abandoning this.

- usage of arrow keys to select, make UX amazing.
- a "sync" mechanism that will be used to upload the db file to web, and will be shared across somehow.
- create a gui maybe a web app that starts a http browser locally and opens a link in browser, like expo does?
- maybe firebase
- add gifs of usage
- allow users to have a configuration file that allows them to change defaults e.g. shell-prefix-symbol etc.
- A documentation site.
- Travis CI?
- Currently PIP works, but create some standalone OS-specific releases?

# Release Checklist :pencil2:

1. Does it work?
2. Are latest changes fetched from remote?
3. Is `changelog.md` updated with changes?
4. Is `README.md` updated with changes?
5. Is Table Of Contents updated, if it is changed?
6. `make build` succeeds without an error?
7. Cool.
