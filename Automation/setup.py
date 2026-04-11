import sys
from pathlib import Path

import setuptools # pyright: ignore[reportMissingModuleSource] # pylint: disable = import-error

workspace_directory = Path(__file__ ).parent.parent
sys.path.insert(0, str(workspace_directory / "Automation"))

from automation_setup import automation_helpers # pyright: ignore[reportMissingImports] # pylint: disable = import-error, wrong-import-position


def run_setup() -> None:
    project_configuration = automation_helpers.load_project_configuration(str(workspace_directory))

    setuptools.setup(
		name = "automation-scripts",
		description = "Automation scripts for %s" % project_configuration["ProjectDisplayName"],
        version = project_configuration["ProjectVersionFull"],
        author = project_configuration["Author"],
        author_email = project_configuration["AuthorEmail"],
        url = project_configuration["ProjectUrl"],
        packages = setuptools.find_packages(include = [ "automation_scripts", "automation_scripts.*" ]),

        python_requires = "~= 3.11",

		install_requires = [
            "bhamon-development-toolkit ~= 3.1.1",
            "twine ~= 6.2.0",
		],

        extras_require = {
            "dev": [
                "mockito ~= 2.0.3",
                "pylint ~= 4.0.5",
                "pytest ~= 9.0.3",
                "pytest-asyncio ~= 1.3.0",
                "pytest-json ~= 0.4.0",
            ]
        },

        entry_points = {
            "console_scripts": [
                "automation = automation_scripts.run_command:main",
            ]
        },
    )


run_setup()
