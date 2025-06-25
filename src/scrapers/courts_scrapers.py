"""
Scrapers for courts.navajo-nsn.gov.
"""
import os
from pathlib import Path
from playwright.async_api import async_playwright
from logger import get_logger
from scrapers.nnols_scrapers import download_file

log = get_logger(__name__)

async def scrape_supreme_court_opinions():
    """
    Scrapes Supreme Court opinions from courts.navajo-nsn.gov.
    """
    async with async_playwright() as p:
        browser = await p.firefox.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
        )
        page = await context.new_page()
        try:
            log.debug("Navigating to supreme court opinions page...")
            await page.goto("http://courts.navajo-nsn.gov/supreme-court-opinions/", wait_until="networkidle", timeout=60000)
            log.debug("Supreme court opinions page loaded.")
            
            accordion_items = await page.locator(".card").all()
            log.info(f"Found {len(accordion_items)} accordion items.")
            for i, item in enumerate(accordion_items):
                log.debug(f"Processing accordion item {i+1}/{len(accordion_items)}...")
                title_element = item.locator("h5.title .text")
                title = await title_element.inner_text()
                
                # Click the title to expand the content
                log.debug(f"Clicking title: {title}")
                await title_element.click(force=True)
                await page.wait_for_timeout(500)  # wait for animation

                content = item.locator(".card-body")
                log.info(f"Title: {title}")
                
                # also get the pdf links
                pdf_links = await content.locator('a[href$=".pdf"]').all()
                log.debug(f"Found {len(pdf_links)} PDF links.")
                for j, link in enumerate(pdf_links):
                    log.debug(f"Processing link {j+1}/{len(pdf_links)}...")
                    pdf_url = await link.get_attribute('href')
                    if pdf_url:
                        file_name = pdf_url.split("/")[-1]
                        download_path = Path("data/courts/supreme_court") / file_name
                        await download_file(pdf_url, download_path)

                log.info(f"Content: {await content.inner_text()}")
                log.info("-" * 20)
        except Exception as e:
            log.error(f"Failed to scrape supreme court opinions: {e}")
        finally:
            await browser.close()