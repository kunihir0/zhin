"""
Tests for the courts.navajo-nsn.gov scrapers.
"""
import pytest
from playwright.async_api import Page, expect

@pytest.mark.asyncio
async def test_scrape_supreme_court_opinions(page: Page):
    """
    Tests that the Supreme Court opinions page is accessible.
    """
    await page.goto("http://courts.navajo-nsn.gov/supreme-court-opinions/")
    print(await page.content())
    await expect(page).to_have_title("Supreme Court Opinions - NN Judicial Branch")