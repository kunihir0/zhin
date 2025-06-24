"""
Scrapers for navajonationcouncil.org.
"""
import os
from pathlib import Path
from playwright.async_api import async_playwright
from logger import get_logger
from scrapers.nnols_scrapers import download_file

log = get_logger(__name__)

async def scrape_bills_and_resolutions():
    """
    Scrapes bills and resolutions from navajonationcouncil.org.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto("https://www.navajonationcouncil.org/legislation-2025/")
            
            accordion_items = await page.locator(".et_pb_accordion_item").all()
            for item in accordion_items:
                title = item.locator(".et_pb_toggle_title")
                await title.click()
                await page.wait_for_timeout(500) # wait for animation
                content = item.locator(".et_pb_toggle_content")
                log.info(f"Title: {await title.inner_text()}")
                log.info(f"Content: {await content.inner_text()}")
                
                pdf_links = await content.locator('a[href$=".pdf"]').all()
                for link in pdf_links:
                    pdf_url = await link.get_attribute('href')
                    if pdf_url:
                        file_name = pdf_url.split("/")[-1]
                        download_path = Path("data/navajonationcouncil/bills_and_resolutions") / file_name
                        await download_file(pdf_url, download_path)

                log.info("-" * 20)
        except Exception as e:
            log.error(f"Failed to scrape bills and resolutions: {e}")
        finally:
            await browser.close()

async def scrape_council_member_data():
    """
    Scrapes council member data from navajonationcouncil.org.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto("https://www.navajonationcouncil.org/council/")
            
            accordion_items = await page.locator(".et_pb_accordion_item").all()
            for item in accordion_items:
                title = item.locator(".et_pb_toggle_title")
                await title.click()
                await page.wait_for_timeout(500) # wait for animation
                content = item.locator(".et_pb_toggle_content")
                log.info(f"Title: {await title.inner_text()}")
                log.info(f"Content: {await content.inner_text()}")
                log.info("-" * 20)
        except Exception as e:
            log.error(f"Failed to scrape council member data: {e}")
        finally:
            await browser.close()