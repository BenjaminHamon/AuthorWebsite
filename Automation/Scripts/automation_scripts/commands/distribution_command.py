import argparse
import logging
import os
import sys

from bhamon_development_toolkit.automation.automation_command import AutomationCommand
from bhamon_development_toolkit.automation.automation_command_group import AutomationCommandGroup
from bhamon_development_toolkit.processes.process_runner import ProcessRunner
from bhamon_development_toolkit.processes.process_spawner import ProcessSpawner
from bhamon_development_toolkit.python.python_package_builder import PythonPackageBuilder
from bhamon_development_toolkit.python.python_twine_distribution_manager import PythonTwineDistributionManager
from bhamon_development_toolkit.security.interactive_credentials_provider import InteractiveCredentialsProvider

from automation_scripts.configuration.automation_configuration import AutomationConfiguration


logger = logging.getLogger("Main")


class DistributionCommand(AutomationCommandGroup):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        local_parser: argparse.ArgumentParser = subparsers.add_parser("distribution", help = "execute commands related to distribution")

        command_collection = [
            _SetupCommand,
            _PackageCommand,
            _UploadCommand,
            _UploadForReleaseCommand,
        ]

        self.add_commands(local_parser, command_collection)

        return local_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


class _SetupCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        return subparsers.add_parser("setup", help = "setup the local packages for distribution")


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        python_executable = sys.executable
        automation_configuration: AutomationConfiguration = kwargs["configuration"]

        process_runner = ProcessRunner(ProcessSpawner(is_console = True))
        python_package_builder = PythonPackageBuilder(python_executable, process_runner)

        logger.info("Generating python package metadata")
        python_package_metadata = automation_configuration.python_development_configuration.get_package_metadata(automation_configuration.project_metadata)
        for python_package in automation_configuration.python_development_configuration.package_collection:
            python_package_builder.generate_package_metadata(python_package, python_package_metadata, simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)


class _PackageCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        return subparsers.add_parser("package", help = "create the distribution packages")


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        raise NotImplementedError("Not supported")


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        python_executable = sys.executable
        automation_configuration: AutomationConfiguration = kwargs["configuration"]

        process_runner = ProcessRunner(ProcessSpawner(is_console = True))
        python_package_builder = PythonPackageBuilder(python_executable, process_runner)

        logger.info("Building python distribution packages")
        for python_package in automation_configuration.python_development_configuration.package_collection:
            output_directory = os.path.join("Artifacts", "Distributions", python_package.identifier)
            custom_settings = { "version": automation_configuration.project_metadata.version.full_identifier }
            log_file_path = os.path.join("Artifacts", "Logs", "BuildDistributionPackage_%s.log" % python_package.identifier)

            await python_package_builder.build_distribution_package_with_custom_settings(
                python_package, output_directory, custom_settings, log_file_path = log_file_path, simulate = simulate)


class _UploadCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        return subparsers.add_parser("upload", help = "upload the distribution packages")


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        python_executable = sys.executable
        automation_configuration: AutomationConfiguration = kwargs["configuration"]
        target_environment: str = "Development"

        version = automation_configuration.project_metadata.version.full_identifier
        distribution_directory = os.path.join("Artifacts", "Distributions")
        package_repository_url = automation_configuration.workspace_environment.get_python_package_repository_url(target_environment)

        python_distribution_manager = _create_distribution_manager(python_executable, package_repository_url)

        logger.info("Uploading python distribution packages")
        for python_package in automation_configuration.python_development_configuration.package_collection:
            archive_name = python_package.name_for_file_system + "-" + version
            package_path = os.path.join(distribution_directory, python_package.identifier, archive_name + "-py3-none-any.whl")
            python_distribution_manager.upload_package(package_path, simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)


class _UploadForReleaseCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        return subparsers.add_parser("upload-for-release", help = "upload the distribution packages for release")


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None: # pylint: disable = too-many-locals
        python_executable = sys.executable
        automation_configuration: AutomationConfiguration = kwargs["configuration"]
        target_environment: str = "Production"

        version = automation_configuration.project_metadata.version.full_identifier
        version_for_release = automation_configuration.project_metadata.version.identifier
        distribution_directory = os.path.join("Artifacts", "Distributions")
        package_repository_url = automation_configuration.workspace_environment.get_python_package_repository_url(target_environment)

        process_runner = ProcessRunner(ProcessSpawner(is_console = True))
        python_package_builder = PythonPackageBuilder(python_executable, process_runner)
        python_distribution_manager = _create_distribution_manager(python_executable, package_repository_url)

        logger.info("Uploading python distribution packages")
        for python_package in automation_configuration.python_development_configuration.package_collection:
            python_package_builder.copy_distribution_package_for_release(
                python_package, version, version_for_release, os.path.join(distribution_directory, python_package.identifier), simulate = simulate)

            archive_name = python_package.name_for_file_system + "-" + version_for_release
            package_path = os.path.join(distribution_directory, python_package.identifier, archive_name + "-py3-none-any.whl")
            python_distribution_manager.upload_package(package_path, simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)


def _create_distribution_manager(python_executable: str, repository_url: str) -> PythonTwineDistributionManager:
    credentials_provider = InteractiveCredentialsProvider()
    credentials = credentials_provider.get_credentials(repository_url)

    python_distribution_manager = PythonTwineDistributionManager(python_executable)
    python_distribution_manager.repository_url = repository_url + "/"
    python_distribution_manager.username = credentials.username
    python_distribution_manager.password = credentials.secret

    return python_distribution_manager
