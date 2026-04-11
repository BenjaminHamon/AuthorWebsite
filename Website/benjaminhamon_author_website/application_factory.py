# cspell:words werkzeug

import logging
from typing import Callable, List

import flask
import jinja2
import werkzeug.exceptions

import benjaminhamon_author_website
from benjaminhamon_author_website.application import Application
from benjaminhamon_author_website.main_controller import MainController


main_logger = logging.getLogger("Website")
request_logger = logging.getLogger("Request")


def create_application() -> Application:
    title = "Benjamin Hamon's author website"
    sources_url = "https://github.com/BenjaminHamon/AuthorWebsite"
    contact_email = "development@benjaminhamon.com"

    flask_application = flask.Flask("benjaminhamon_author_website")
    application = Application(flask_application)
    main_controller = MainController()

    configure(flask_application, title, sources_url, contact_email)
    register_handlers(flask_application, application)
    register_routes(flask_application, main_controller)

    return application


def configure(application: flask.Flask, title: str, sources_url: str, contact_email: str) -> None:
    application.config["WEBSITE_TITLE"] = title
    application.config["WEBSITE_COPYRIGHT"] = benjaminhamon_author_website.__copyright__
    application.config["WEBSITE_VERSION"] = benjaminhamon_author_website.__version__
    application.config["WEBSITE_DATE"] = benjaminhamon_author_website.__date__
    application.config["WEBSITE_SOURCES_URL"] = sources_url
    application.config["WEBSITE_CONTACT_EMAIL"] = contact_email

    application.jinja_env.undefined = jinja2.StrictUndefined
    application.jinja_env.trim_blocks = True
    application.jinja_env.lstrip_blocks = True

    application.context_processor(lambda: { "url_for": versioned_url_for })


def register_handlers(flask_application: flask.Flask, application: Application) -> None:
    flask_application.log_exception = lambda exc_info: None
    flask_application.before_request(application.log_request)
    for exception in werkzeug.exceptions.default_exceptions.values():
        flask_application.register_error_handler(exception, application.handle_error)


def register_routes(flask_application: flask.Flask, main_controller: MainController) -> None:
    add_url_rule(flask_application, "/", [ "GET" ], main_controller.home)
    add_url_rule(flask_application, "/About", [ "GET" ], main_controller.about)
    add_url_rule(flask_application, "/Books", [ "GET" ], main_controller.books)
    add_url_rule(flask_application, "/Contact", [ "GET" ], main_controller.contact)



def add_url_rule(application: flask.Flask, path: str, methods: List[str], handler: Callable, **kwargs) -> None:
    endpoint = ".".join(handler.__module__.split(".")[1:]) + "." + handler.__name__
    application.add_url_rule(path, methods = methods, endpoint = endpoint, view_func = handler, **kwargs)


def versioned_url_for(endpoint: str, **values) -> str:
    if endpoint == "static":
        values["version"] = flask.current_app.config["WEBSITE_VERSION"]
    return flask.url_for(endpoint, **values)
