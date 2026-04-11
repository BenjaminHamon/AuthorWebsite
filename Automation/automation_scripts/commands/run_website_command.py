import argparse
import logging
import os
import sys
from typing import List, Optional

from bhamon_development_toolkit.automation.automation_command import AutomationCommand
from bhamon_development_toolkit.processes import process_helpers
from bhamon_development_toolkit.processes.executable_command import ExecutableCommand
from bhamon_development_toolkit.processes.process_options import ProcessOptions
from bhamon_development_toolkit.processes.process_output_handler import ProcessOutputHandler
from bhamon_development_toolkit.processes.process_output_logger import ProcessOutputLogger
from bhamon_development_toolkit.processes.process_runner import ProcessRunner
from bhamon_development_toolkit.processes.process_spawner import ProcessSpawner
from bhamon_development_toolkit.python import python_helpers
from bhamon_development_toolkit.python.python_environment import PythonEnvironment

from automation_scripts.configuration.automation_configuration import AutomationConfiguration


logger = logging.getLogger("Main")


class RunWebsiteCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        parser = subparsers.add_parser("run-website", help = "run the website")
        parser.add_argument("--address", required = True, help = "set the address for the server to listen to")
        parser.add_argument("--port", required = True, type = int, help = "set the port for the server to listen to")
        return parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        raise NotImplementedError("Not supported")


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        address: str = arguments.address
        port: int = arguments.port

        automation_configuration: AutomationConfiguration = kwargs["configuration"]

        venv_directory = automation_configuration.python_development_configuration.venv_directory
        python_system_executable = python_helpers.resolve_system_python_executable()
        python_environment = PythonEnvironment(python_system_executable, venv_directory)
        log_file_path = os.path.join("Artifacts", "RunWebsite.log")

        process_runner = ProcessRunner(ProcessSpawner(is_console = True))

        await self._run_website(
            process_runner = process_runner,
            python_executable = python_environment.get_venv_python_executable(),
            address = address,
            port = port,
            log_file_path = log_file_path,
            simulate = simulate)


    async def _run_website(self, # pylint: disable = too-many-arguments
            process_runner: ProcessRunner, python_executable: str, address: str, port: int, *,
            log_file_path: Optional[str] = None, simulate: bool = False) -> None:

        application_module = "benjaminhamon_author_website.run"

        command = ExecutableCommand(python_executable)
        command.add_arguments([ "-m", application_module ])
        command.add_arguments([ "--address", address ])
        command.add_arguments([ "--port", str(port) ])

        if log_file_path is not None:
            command.add_internal_arguments([ "--log-file", log_file_path ], [])

        process_options = ProcessOptions()
        raw_logger = process_helpers.create_raw_logger(stream = sys.stdout)
        process_output_logger = ProcessOutputLogger(raw_logger.get_actual_logger())
        output_handlers: List[ProcessOutputHandler] = [ process_output_logger ]

        logger.info("Running website)")
        logger.debug("+ %s", process_helpers.format_executable_command(command.get_command_for_logging()))

        try:
            if not simulate:
                try:
                    await process_runner.run(command, process_options, output_handlers)
                finally:
                    logger.debug("Process log file: '%s'", log_file_path)
        finally:
            raw_logger.dispose()
