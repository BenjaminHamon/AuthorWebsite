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
    flask_application = flask.Flask("benjaminhamon_author_website")
    application = Application(flask_application)
    main_controller = MainController()

    configure(flask_application)
    register_handlers(flask_application, application)
    register_routes(flask_application, main_controller)

    return application


def configure(application: flask.Flask) -> None:
    application.config["METADATA"] = {
        "title": "Benjamin Hamon's author website",
        "product": benjaminhamon_author_website.__product__,
        "copyright": benjaminhamon_author_website.__copyright__,
        "version": benjaminhamon_author_website.__version__,
        "date": benjaminhamon_author_website.__date__,
        "sources_url": "https://github.com/BenjaminHamon/AuthorWebsite",
        "contact_email": "development@benjaminhamon.com",
    }

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
        values["version"] = flask.current_app.config["METADATA"]["version"]
    return flask.url_for(endpoint, **values)
