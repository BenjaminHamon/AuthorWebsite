# cspell:words werkzeug

import logging
from typing import Any, Callable, Optional, Tuple

import flask
import werkzeug.exceptions

from benjaminhamon_author_website import web_helpers


main_logger = logging.getLogger("Application")
request_logger = logging.getLogger("Request")


class Application:


    def __init__(self, flask_application: flask.Flask) -> None:
        self._flask_application = flask_application


    def __call__(self, environ: dict, start_response: Callable) -> Any:
        return self._flask_application(environ, start_response)


    def run(self, address: Optional[str] = None, port: Optional[int] = None, debug: Optional[bool] = None) -> None:
        self._flask_application.run(host = address, port = port, debug = debug)


    def log_request(self) -> None:
        request_logger.info("(%s) %s %s", flask.request.environ["REMOTE_ADDR"], flask.request.method, flask.request.base_url)


    def handle_error(self, exception: Any) -> Tuple[str, int]:
        status_code = exception.code if isinstance(exception, werkzeug.exceptions.HTTPException) and exception.code is not None else 500
        status_message = web_helpers.get_http_error_message(status_code)

        request_logger.error("(%s) %s %s (StatusCode: %s)",
            flask.request.environ["REMOTE_ADDR"], flask.request.method, flask.request.base_url, status_code, exc_info = True)

        return flask.render_template("error.html", title = "Error", message = status_message, status_code = status_code), status_code
