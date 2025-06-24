"""
Scrapers for nnols.org.
"""
import os
from pathlib import Path
from playwright.async_api import async_playwright
from logger import get_logger

log = get_logger(__name__)

async def download_file(url: str, download_path: Path):
    """
    Downloads a file from a given URL to a specified path.
    """
    if not download_path.parent.exists():
        download_path.parent.mkdir(parents=True)
        
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            async with page.expect_download() as download_info:
                await page.goto(url)
            download = await download_info.value
            await download.save_as(download_path)
            log.info(f"Successfully downloaded {url} to {download_path}")
        except Exception as e:
            log.error(f"Failed to download {url}: {e}")
        finally:
            await browser.close()

async def scrape_base_code():
    """
    Scrapes the base Navajo Nation Code from nnols.org.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto("http://nnols.org/navajo-nation-code")
            
            pdf_links = await page.locator('a[href$=".pdf"]').all()
            
            for link in pdf_links:
                pdf_url = await link.get_attribute('href')
                if pdf_url:
                    file_name = pdf_url.split("/")[-1]
                    download_path = Path("data/nnols/base_code") / file_name
                    await download_file(pdf_url, download_path)
        except Exception as e:
            log.error(f"Failed to scrape base code: {e}")
        finally:
            await browser.close()

async def scrape_amendments():
    """
    Scrapes the amendments to the Navajo Nation Code from nnols.org.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto("http://nnols.org/navajo-nation-code/amendments/")
            
            pdf_links = await page.locator('a[href$=".pdf"]').all()
            
            for link in pdf_links:
                pdf_url = await link.get_attribute('href')
                if pdf_url:
                    file_name = pdf_url.split("/")[-1]
                    download_path = Path("data/nnols/amendments") / file_name
                    await download_file(pdf_url, download_path)
        except Exception as e:
            log.error(f"Failed to scrape amendments: {e}")
        finally:
            await browser.close()