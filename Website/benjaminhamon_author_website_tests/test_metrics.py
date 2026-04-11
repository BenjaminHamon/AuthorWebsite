from typing import Dict, Iterable, Optional

import requests

import prometheus_client.parser
from prometheus_client.metrics_core import Metric
from prometheus_client.samples import Sample

from benjaminhamon_author_website_tests.website_runner import WebsiteRunner


def test_metrics_with_authorization(website_using_flask: WebsiteRunner) -> None:
    response = requests.request("GET", website_using_flask.get_url() + "/metrics", headers = { "Authorization": "Bearer metrics" }, timeout = 1)

    assert response.status_code == 200
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text != ""


def test_metrics_with_bad_authorization(website_using_flask: WebsiteRunner) -> None:
    response = requests.request("GET", website_using_flask.get_url() + "/metrics", headers = { "Authorization": "Bearer wrong" }, timeout = 1)

    assert response.status_code == 403
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text == ""


def test_metrics_without_authorization(website_using_flask: WebsiteRunner) -> None:
    response = requests.request("GET", website_using_flask.get_url() + "/metrics", timeout = 1)

    assert response.status_code == 401
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text == ""


def test_metrics_with_multiprocess(website_using_gunicorn: WebsiteRunner) -> None:
    for _ in range(0, 100):
        requests.request("GET", website_using_gunicorn.get_url() + "/", timeout = 30)

    response = requests.request("GET", website_using_gunicorn.get_url() + "/metrics", headers = { "Authorization": "Bearer metrics" }, timeout = 1)

    assert response.status_code == 200
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text != ""

    metrics = prometheus_client.parser.text_string_to_metric_families(response.text)
    sample = _get_sample(metrics, "flask_http_request_total", { "method": "GET", "status": "200" })

    assert sample is not None
    assert sample.value == 100


def _get_sample(metrics: Iterable[Metric], name: str, labels: Dict[str,str]) -> Optional[Sample]:
    for family in metrics:
        for sample in family.samples:
            if name == sample.name and labels == sample.labels:
                return sample

    return None
