import pytest
from playwright.async_api import Page
from playwright.async_api import expect

from benjaminhamon_author_website_tests.website_runner import WebsiteRunner



@pytest.mark.asyncio(loop_scope = "session")
async def test_home_page_with_gunicorn(website_using_gunicorn: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_gunicorn.get_url() + "/")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Home - Benjamin Hamon's author website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_home_page(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Home - Benjamin Hamon's author website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_books_page(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/Books")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Books - Benjamin Hamon's author website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_about_page(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/About")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("About - Benjamin Hamon's author website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_contact_page(website_using_flask: WebsiteRunner, page: Page) -> None:
    response = await page.goto(website_using_flask.get_url() + "/Contact")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Contact - Benjamin Hamon's author website")
