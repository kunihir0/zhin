"""
Tests for the nnols.org scrapers.
"""
import pytest
from playwright.async_api import Page, expect

@pytest.mark.asyncio
async def test_scrape_base_code(page: Page):
    """
    Tests that the base code page is accessible.
    """
    await page.goto("http://nnols.org/navajo-nation-code")
    print(await page.content())
    await expect(page).to_have_title("Navajo Nation Code | Navajo Nation Office of Legislative Services")

@pytest.mark.asyncio
async def test_scrape_amendments(page: Page):
    """
    Tests that the amendments page is accessible.
    """
    await page.goto("http://nnols.org/navajo-nation-code/amendments/")
    print(await page.content())
    await expect(page).to_have_title("Amendments | Navajo Nation Office of Legislative Services")