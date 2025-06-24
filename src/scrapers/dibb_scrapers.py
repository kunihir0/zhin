"""
Scrapers for dibb.nnols.org.
"""
import os
from pathlib import Path
from playwright.async_api import async_playwright
from logger import get_logger
from scrapers.nnols_scrapers import download_file

log = get_logger(__name__)

async def scrape_legislative_metadata():
    """
    Scrapes legislative metadata from dibb.nnols.org.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto("http://dibb.nnols.org/publicreporting.aspx")

            # Set the number of entries to 100
            await page.select_option("select[name='LegislationInfoTable_length']", "100")

            while True:
                # Scrape the data from the current page
                rows = await page.locator("#LegislationInfoTable tbody tr").all()
                for i in range(len(rows)):
                    row = page.locator("#LegislationInfoTable tbody tr").nth(i)
                    view_link = row.locator("a:has-text('View')")
                    
                    href = await view_link.get_attribute("href")
                    if href:
                        bill_url = f"http://dibb.nnols.org/{href}"
                        await page.goto(bill_url)
                        await page.wait_for_load_state()
                        
                        pdf_links = await page.locator("td.TableLnks a[href*='/api/FileInfo/GetUri/']").all()
                        for pdf_link in pdf_links:
                            href = await pdf_link.get_attribute("href")
                            if href:
                                full_pdf_url = f"http://dibb.nnols.org{href}"
                                file_name = full_pdf_url.split("=")[-1] + ".pdf"
                                download_path = Path("data/dibb/bills") / file_name
                                await download_file(full_pdf_url, download_path)
                        
                        await page.go_back()
                        await page.wait_for_load_state()


                # Check if there is a next page
                next_button = page.locator("#LegislationInfoTable_next")
                if "disabled" in await next_button.get_attribute("class"):
                    break
                
                await next_button.click()
                await page.wait_for_timeout(1000) # wait for table to load
        except Exception as e:
            log.error(f"Failed to scrape legislative metadata: {e}")
        finally:
            await browser.close()