import requests


def test_metrics_with_authorization(website: str) -> None:
    response = requests.request("GET", website + "/metrics", headers = { "Authorization": "Bearer metrics" }, timeout = 1)

    assert response.status_code == 200
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text != ""


def test_metrics_with_bad_authorization(website: str) -> None:
    response = requests.request("GET", website + "/metrics", headers = { "Authorization": "Bearer wrong" }, timeout = 1)

    assert response.status_code == 403
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text == ""


def test_metrics_without_authorization(website: str) -> None:
    response = requests.request("GET", website + "/metrics", timeout = 1)

    assert response.status_code == 401
    assert response.headers["Content-Type"].split(";")[0] == "text/plain"
    assert response.text == ""
