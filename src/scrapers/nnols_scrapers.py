"""
Scrapers for nnols.org.
"""
import os
import asyncio
from pathlib import Path
import httpx
from playwright.async_api import async_playwright
from logger import get_logger

log = get_logger(__name__)

async def download_file(url: str, download_path: Path, retries=3, delay=5) -> str:
    """
    Downloads a file from a given URL to a specified path with retries.
    Returns a status string: "Success", "Not Found", or "Failed".
    """
    if download_path.exists():
        log.debug(f"File already exists, skipping download: {download_path}")
        return "Success"

    if not download_path.parent.exists():
        download_path.parent.mkdir(parents=True)
        
    for i in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                with open(download_path, "wb") as f:
                    f.write(response.content)
                log.info(f"Successfully downloaded {url} to {download_path}")
                return "Success"
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                log.error(f"File not found on server (404): {url}")
                return "Not Found"
            log.error(f"Failed to download {url} on attempt {i+1}: {e}")
            if i < retries - 1:
                log.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
        except Exception as e:
            log.error(f"Failed to download {url} on attempt {i+1}: {e}")
            if i < retries - 1:
                log.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
    
    log.error(f"Failed to download {url} after {retries} attempts.")
    return "Failed"

async def scrape_base_code():
    """
    Scrapes the base Navajo Nation Code from nnols.org.
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
            log.debug("Navigating to base code page...")
            await page.goto("http://nnols.org/navajo-nation-code", wait_until="networkidle", timeout=60000)
            log.debug("Base code page loaded.")
            
            pdf_links = await page.locator('a[href$=".pdf"]').all()
            log.debug(f"Found {len(pdf_links)} PDF links.")
            
            for i, link in enumerate(pdf_links):
                log.debug(f"Processing link {i+1}/{len(pdf_links)}...")
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
            log.debug("Navigating to amendments page...")
            await page.goto("http://nnols.org/navajo-nation-code/amendments/", wait_until="networkidle", timeout=60000)
            log.debug("Amendments page loaded.")
            
            pdf_links = await page.locator('a[href$=".pdf"]').all()
            log.debug(f"Found {len(pdf_links)} PDF links.")
            
            for i, link in enumerate(pdf_links):
                log.debug(f"Processing link {i+1}/{len(pdf_links)}...")
                pdf_url = await link.get_attribute('href')
                if pdf_url:
                    file_name = pdf_url.split("/")[-1]
                    download_path = Path("data/nnols/amendments") / file_name
                    await download_file(pdf_url, download_path)
        except Exception as e:
            log.error(f"Failed to scrape amendments: {e}")
        finally:
            await browser.close()