import sys
from pathlib import Path

import pytest_asyncio

import benjaminhamon_author_website
from benjaminhamon_author_website_tests.website_runner import WebsiteRunner


@pytest_asyncio.fixture(name = "website", scope = "module", loop_scope = "session")
async def website_fixture():
    python_executable = sys.executable
    script_path = Path(benjaminhamon_author_website.__file__).parent / "run.py"

    address = "localhost"
    port = 4999

    command = [ python_executable, script_path, "--address", address, "--port", str(port) ]

    async with WebsiteRunner(command, address, port) as website:
        yield website.get_url()
