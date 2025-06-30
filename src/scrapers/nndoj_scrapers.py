"""
Scrapers for nndoj.navajo-nsn.gov.
"""
import os
from pathlib import Path
import httpx
from playwright.async_api import async_playwright
from logger import get_logger
import json
from urllib.parse import urljoin, quote
from queue_system import QueueManager
from progress import ProgressBar
from scrapers.nnols_scrapers import download_file

log = get_logger(__name__)

async def scrape_nndoj_roster(headless=True):
    """
    Scrapes the staff roster from the NNDOJ website.
    """
    department_urls = [
        "https://nndoj.navajo-nsn.gov/Directory/Chapter-Unit",
        "https://nndoj.navajo-nsn.gov/Directory/Economic-Community-Development",
        "https://nndoj.navajo-nsn.gov/Directory/Human-Services-Government",
        "https://nndoj.navajo-nsn.gov/Directory/Litigation-Unit",
        "https://nndoj.navajo-nsn.gov/Directory/Natural-Resources",
        "https://nndoj.navajo-nsn.gov/Directory/Office-of-Attorney-General",
        "https://nndoj.navajo-nsn.gov/Directory/Tax-and-Finance",
        "https://nndoj.navajo-nsn.gov/Directory/Water-Rights"
    ]

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()

        all_staff = []
        for url in department_urls:
            try:
                department = url.split("/")[-1]
                log.info(f"Scraping roster for {department}...")
                await page.goto(url, timeout=60000)
                staff = await process_roster_page(page)
                for person in staff:
                    person["department"] = department
                all_staff.extend(staff)
            except Exception as e:
                log.error(f"Failed to scrape {url}: {e}")

        output_dir = Path("data/nndoj")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "roster.json"

        with open(output_path, "w") as f:
            json.dump(all_staff, f, indent=4)
        
        log.info(f"NNDOJ roster saved to {output_path}")

        await browser.close()

async def process_roster_page(page):
    """
    Processes a single roster page.
    """
    staff = []
    rows = await page.locator('.row.mt-3').all()
    for row in rows:
        name_element = row.locator('h2')
        name = await name_element.inner_text() if await name_element.count() > 0 else "N/A"

        title_element = row.locator('h3')
        title = await title_element.inner_text() if await title_element.count() > 0 else "N/A"

        img_element = row.locator('img')
        photo_url = await img_element.get_attribute('src') if await img_element.count() > 0 else None
        if photo_url:
            photo_url = urljoin(page.url, photo_url)

        bio_elements = await row.locator('div.col-md-8 p').all()
        bio = "\n".join([await p.inner_text() for p in bio_elements]) if bio_elements else "N/A"

        staff.append({
            "name": name,
            "title": title,
            "photo_url": photo_url,
            "bio": bio
        })
    return staff