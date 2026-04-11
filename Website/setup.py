# cspell:words cmdclass

import sys
from pathlib import Path

import distutils.command.build # pyright: ignore[reportMissingModuleSource] # pylint: disable = deprecated-module, import-error
import setuptools # pyright: ignore[reportMissingModuleSource] # pylint: disable = import-error

workspace_directory = Path(__file__ ).parent.parent
sys.path.insert(0, str(workspace_directory / "Automation"))

from automation_setup import automation_helpers # pyright: ignore[reportMissingImports] # pylint: disable = import-error, wrong-import-position


class BuildCommand(distutils.command.build.build):

    def initialize_options(self):
        super().initialize_options()

        artifact_directory = workspace_directory / "Artifacts" / "Distributions-Intermediate" / "benjaminhamon_author_website"
        self.build_base = str(artifact_directory) # pylint: disable = attribute-defined-outside-init


def run_setup() -> None:
    project_configuration = automation_helpers.load_project_configuration(str(workspace_directory))

    setuptools.setup(
        cmdclass = { "build": BuildCommand },

		name = "benjaminhamon-author-website",
		description = "Author website for Benjamin Hamon",
        version = project_configuration["ProjectVersionFull"],
        author = project_configuration["Author"],
        author_email = project_configuration["AuthorEmail"],
        url = project_configuration["ProjectUrl"],
        license_files = [ "../About.md", "../License.txt" ],
        packages = setuptools.find_packages(include = [ "benjaminhamon_author_website", "benjaminhamon_author_website.*" ]),

        python_requires = "~= 3.11",

        install_requires = [
            "benjaminhamon-standard-extensions ~= 1.0.1",
            "Flask ~= 3.1.3",
        ],

        extras_require = {
            "dev": [
                "mockito ~= 2.0.3",
                "pylint ~= 4.0.5",
                "pytest ~= 9.0.3",
                "pytest-asyncio ~= 1.3.0",
                "pytest-json ~= 0.4.0",
            ],
        },

        package_data = {
            "benjaminhamon_author_website": [
                "static/**/*.css",
                "static/**/*.jpeg",
                "static/**/*.pdf",
                "static/**/*.png",
                "templates/**/*.html",
            ],
        },
    )


run_setup()
