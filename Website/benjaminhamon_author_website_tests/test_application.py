import pytest
from playwright.async_api import Page
from playwright.async_api import expect


@pytest.mark.asyncio(loop_scope = "session")
async def test_home_page(website: str, page: Page) -> None:
    response = await page.goto(website + "/")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Home - Benjamin Hamon's author website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_books_page(website: str, page: Page) -> None:
    response = await page.goto(website + "/Books")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Books - Benjamin Hamon's author website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_about_page(website: str, page: Page) -> None:
    response = await page.goto(website + "/About")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("About - Benjamin Hamon's author website")


@pytest.mark.asyncio(loop_scope = "session")
async def test_contact_page(website: str, page: Page) -> None:
    response = await page.goto(website + "/Contact")

    assert response is not None
    assert response.status == 200

    await expect(page).to_have_title("Contact - Benjamin Hamon's author website")
