# cspell:words multiproc

import json
import os
import platform
import sys
from pathlib import Path

import pytest
import pytest_asyncio

import benjaminhamon_author_website
from benjaminhamon_author_website_tests.website_runner import WebsiteRunner


@pytest_asyncio.fixture(name = "website_using_flask", scope = "module", loop_scope = "session")
async def website_fixture():
    python_executable = sys.executable
    application_module = "benjaminhamon_author_website.run"
    address = "localhost"
    port = 4999

    command = [ python_executable, "-m", application_module, "--address", address, "--port", str(port) ]

    async with WebsiteRunner(command, address, port) as website_runner:
        yield website_runner


@pytest_asyncio.fixture(name = "website_using_gunicorn", scope = "module", loop_scope = "session")
async def gunicorn_fixture(tmp_path_factory: pytest.TempPathFactory):
    if platform.system() != "Linux":
        pytest.skip("gunicorn requires Linux")

    gunicorn_executable = Path(sys.executable).parent / "gunicorn"
    gunicorn_configuration_path = Path(benjaminhamon_author_website.__file__).parent / "gunicorn_configuration.py"

    address = "localhost"
    port = 4999

    application_configuration = {
        "metrics_token": "metrics",
        "server": "gunicorn",
    }

    runtime_directory = tmp_path_factory.mktemp("gunicorn", numbered = True)
    application_configuration_file_path = runtime_directory / "application.json"
    with open(application_configuration_file_path, mode = "w", encoding = "utf-8") as application_configuration_file:
        json.dump(application_configuration, application_configuration_file)

    prometheus_multiprocess_directory = runtime_directory / "prometheus"
    os.makedirs(str(prometheus_multiprocess_directory))

    command = [ str(gunicorn_executable), "--bind", address + ":" + str(port), "--config", str(gunicorn_configuration_path) ]

    environment = {
        "APPLICATION_CONFIGURATION": str(application_configuration_file_path),
        "PROMETHEUS_MULTIPROC_DIR": str(prometheus_multiprocess_directory),
    }

    async with WebsiteRunner(command, address, port, environment) as website_runner:
        yield website_runner
