"""
Scrapers for navajonationcouncil.org.
"""
import os
from pathlib import Path
import httpx
from playwright.async_api import async_playwright
from logger import get_logger
from scrapers.nnols_scrapers import download_file

log = get_logger(__name__)

async def scrape_bills_and_resolutions():
    """
    Scrapes bills and resolutions from navajonationcouncil.org.
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
            log.debug("Navigating to bills and resolutions page...")
            await page.goto("https://www.navajonationcouncil.org/legislation-2025/", wait_until="networkidle", timeout=60000)
            log.debug("Bills and resolutions page loaded.")
            
            accordion_items = await page.locator(".et_pb_accordion_item").all()
            log.debug(f"Found {len(accordion_items)} accordion items.")
            for i, item in enumerate(accordion_items):
                log.debug(f"Processing accordion item {i+1}/{len(accordion_items)}...")
                title = item.locator(".et_pb_toggle_title")
                await title.click(force=True)
                await page.wait_for_timeout(500) # wait for animation
                content = item.locator(".et_pb_toggle_content")
                log.info(f"Title: {await title.inner_text()}")
                log.info(f"Content: {await content.inner_text()}")
                
                pdf_links = await content.locator('a[href$=".pdf"]').all()
                log.debug(f"Found {len(pdf_links)} PDF links.")
                for j, link in enumerate(pdf_links):
                    log.debug(f"Processing link {j+1}/{len(pdf_links)}...")
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
            log.debug("Navigating to council member page...")
            await page.goto("https://www.navajonationcouncil.org/council/", wait_until="networkidle", timeout=60000)
            log.debug("Council member page loaded.")
            
            accordion_items = await page.locator(".et_pb_accordion_item").all()
            log.debug(f"Found {len(accordion_items)} accordion items.")
            
            council_roster = []
            for i, item in enumerate(accordion_items):
                log.debug(f"Processing accordion item {i+1}/{len(accordion_items)}...")
                title_element = item.locator(".et_pb_toggle_title")
                await title_element.click(force=True)
                await page.wait_for_timeout(500) # wait for animation
                
                name = await title_element.inner_text()
                content_element = item.locator(".et_pb_toggle_content")
                content_html = await content_element.inner_html()

                import re
                
                def get_value(pattern, text):
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        # Return the first group, stripping any HTML tags and extra whitespace
                        return re.sub('<[^<]+?>', '', match.group(1)).strip()
                    return ""

                photo_url = get_value(r'<img.*?src="([^"]+)"', content_html)
                representing = get_value(r'is representing:</strong></p>\s*<p>\((.*?)\)</p>', content_html)
                committee = get_value(r"Committee:.*</strong>\s*(.*?)<", content_html)
                email = get_value(r'<em>([^<]+@[^<]+)</em>', content_html)
                maternal_clan = get_value(r"Maternal Clan:\s*</strong>([^<]+)<", content_html)
                paternal_clan = get_value(r"Paternal Clan:\s*</strong>([^<]+)<", content_html)
                maternal_grandfather = get_value(r"Maternal Grandfather:\s*</strong>([^<]+)<", content_html)
                paternal_grandfather = get_value(r"Paternal Grandfather:\s*</strong>([^<]+)<", content_html)
                hometown = get_value(r"Hometown:\s*</strong>([^<]+)<", content_html)

                member_data = {
                    "name": name,
                    "photo_url": photo_url,
                    "representing": representing,
                    "committee": committee,
                    "email": email,
                    "maternal_clan": maternal_clan,
                    "paternal_clan": paternal_clan,
                    "maternal_grandfather": maternal_grandfather,
                    "paternal_grandfather": paternal_grandfather,
                    "hometown": hometown,
                }
                council_roster.append(member_data)
                log.info(f"Scraped data for {name}")

            # Save the roster to a single file
            output_dir = Path("data/navajonationcouncil")
            output_dir.mkdir(exist_ok=True)
            roster_path = output_dir / "council_roster.json"
            
            import json
            with open(roster_path, "w") as f:
                json.dump(council_roster, f, indent=4)
            log.info(f"Council roster saved to {roster_path}")
        except Exception as e:
            log.error(f"Failed to scrape council member data: {e}")
        finally:
            await browser.close()