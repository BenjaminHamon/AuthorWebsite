import json
import logging
import os

import benjaminhamon_author_website
from benjaminhamon_author_website import application_factory


logger = logging.getLogger("Main")

logger.info("Instancing application for WSGI (version: %s)", benjaminhamon_author_website.__version__)

configuration_file_path = os.environ["APPLICATION_CONFIGURATION"]
with open(configuration_file_path, mode = "r", encoding = "utf-8") as configuration_file:
    configuration = json.load(configuration_file)

application = application_factory.create_application(
    metrics_token = configuration["metrics_token"],
    server = configuration["server"])
