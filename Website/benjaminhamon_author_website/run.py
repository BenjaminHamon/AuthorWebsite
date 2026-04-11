# cspell:words levelname werkzeug

import argparse
import logging
import sys
from typing import Optional

from benjaminhamon_author_website import application_factory
from benjaminhamon_author_website import logging_helpers


logger = logging.getLogger("Main")


def main():
    argument_parser = create_argument_parser()
    arguments = argument_parser.parse_args()

    configure_logging(arguments)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    application = application_factory.create_application()
    website_url = "http://%s:%s/" % (arguments.address, arguments.port)

    logger.info("Website available at '%s'", website_url)
    application.run(address = arguments.address, port = arguments.port, debug = True)


def create_argument_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument("--address", required = True,
        help = "set the address for the server to listen to")
    argument_parser.add_argument("--port", required = True, type = int,
        help = "set the port for the server to listen to")

    argument_parser.add_argument("--verbosity", choices = logging_helpers.all_log_levels,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(logging_helpers.all_log_levels))
    argument_parser.add_argument("--log-file",
        metavar = "<file_path>", help = "set the log file path")
    argument_parser.add_argument("--log-file-verbosity", choices = logging_helpers.all_log_levels,
        metavar = "<level>", help = "set the logging level for the log file (%s)" % ", ".join(logging_helpers.all_log_levels))

    return argument_parser


def configure_logging(arguments: argparse.Namespace):
    message_format = "{asctime} [{levelname}][{name}] {message}"
    date_format = "%Y-%m-%dT%H:%M:%S"

    log_stream_verbosity: str = "info"
    log_file_path: Optional[str] = None
    log_file_verbosity: str = "debug"

    if arguments is not None and getattr(arguments, "verbosity", None) is not None:
        log_stream_verbosity = arguments.verbosity
    if arguments is not None and getattr(arguments, "log_file", None) is not None:
        log_file_path = arguments.log_file
    if arguments is not None and getattr(arguments, "log_file_verbosity", None) is not None:
        log_file_verbosity = arguments.log_file_verbosity

    logging.root.setLevel(logging.DEBUG)

    logging.addLevelName(logging.DEBUG, "Debug")
    logging.addLevelName(logging.INFO, "Info")
    logging.addLevelName(logging.WARNING, "Warning")
    logging.addLevelName(logging.ERROR, "Error")
    logging.addLevelName(logging.CRITICAL, "Critical")

    logging_helpers.configure_log_stream(logging.root, sys.stdout, log_stream_verbosity, message_format, date_format)
    if log_file_path is not None:
        logging_helpers.configure_log_file(logging.root, log_file_path, log_file_verbosity, message_format, date_format, mode = "w", encoding = "utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception: # pylint: disable = broad-except
        logger.error("Script failed", exc_info = True)
        sys.exit(1)
