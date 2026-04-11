# Benjamin Hamon's author website



## Overview

This is a personal website for Benjamin Hamon, hosted at https://author.benjaminhamon.com.

The project is open source software. See [About](About.md) for more information.



## Development

The project is developed using Python and supports the usual workflows with `pip`, `pylint` and `pytest`. It is highly recommended to use a Python virtual environment. The website can be run through `Sources/website/benjaminhamon_author_website/run.py`.

Additionally, there are commands to automate development related tasks, as can be found under [Automation](Automation). Use the `Automation/Setup/setup.py` script for a quick setup. Following that, the commands will be available through `.venv-automation/scripts/automation`, or `automation` directly after activating the `venv-automation` virtual environment. This executable corresponds to the `Automation/Scripts/automation_scripts/run_command.py` script. Use the `--help` option for information, and the `--simulate` option if you wish to check a command's behavior before actually running it.
