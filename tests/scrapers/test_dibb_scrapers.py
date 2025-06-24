"""
Tests for the dibb.nnols.org scrapers.
"""
import pytest
from playwright.async_api import Page, expect

@pytest.mark.asyncio
async def test_scrape_legislative_metadata(page: Page):
    """
    Tests that the DIBB website is accessible.
    """
    await page.goto("http://dibb.nnols.org/publicreporting.aspx")
    print(await page.content())
    await expect(page).to_have_title("NNOLS Legislative Tracking System")