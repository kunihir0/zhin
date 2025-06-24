"""
Tests for the navajonationcouncil.org scrapers.
"""
import pytest
from playwright.async_api import Page, expect

@pytest.mark.asyncio
async def test_scrape_bills_and_resolutions(page: Page):
    """
    Tests that the legislation page is accessible.
    """
    await page.goto("https://www.navajonationcouncil.org/legislation-2025/")
    print(await page.content())
    await expect(page).to_have_title("Legislation 2025 - 25th Navajo Nation Council")

@pytest.mark.asyncio
async def test_scrape_council_member_data(page: Page):
    """
    Tests that the council members page is accessible.
    """
    await page.goto("https://www.navajonationcouncil.org/council/")
    print(await page.content())
    await expect(page).to_have_title("Navajo Nation Council | Legislative Body of the Navajo Nation")