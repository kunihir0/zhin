"""
Scrapers for dibb.nnols.org.
"""
import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from logger import get_logger
from scrapers.nnols_scrapers import download_file
from queue_system import QueueManager

log = get_logger(__name__)


async def scrape_legislative_metadata():
    """
    Scrapes legislative metadata from dibb.nnols.org.
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
        
        async def process_bill_page_worker(bill_url):
            """Worker coroutine that processes a single bill page."""
            await process_bill_page(context, bill_url)

        bill_processor_queue = QueueManager(
            worker_coro=process_bill_page_worker,
            num_workers=10,
            name="BillProcessor"
        )

        try:
            page = await context.new_page()
            log.debug("Navigating to public reporting page...")
            await page.goto("http://dibb.nnols.org/publicreporting.aspx", wait_until="networkidle", timeout=60000)
            log.debug("Public reporting page loaded.")

            # Set the number of entries to 100
            log.debug("Setting number of entries to 100.")
            await page.select_option("select[name='LegislationInfoTable_length']", "100")
            await page.wait_for_timeout(1000) # wait for table to reload

            # Start the queue manager
            await bill_processor_queue.start()

            # Collect all bill URLs
            bill_urls = []
            page_num = 1
            while True:
                log.debug(f"Scraping page {page_num} for bill URLs...")
                rows = await page.locator("#LegislationInfoTable tbody tr").all()
                log.debug(f"Found {len(rows)} rows on page {page_num}.")
                for row in rows:
                    view_link = row.locator("a:has-text('View')")
                    href = await view_link.get_attribute("href")
                    if href:
                        bill_urls.append(f"http://dibb.nnols.org/{href}")

                next_button = page.locator("#LegislationInfoTable_next")
                if "disabled" in await next_button.get_attribute("class"):
                    log.debug("Next button is disabled. Exiting URL collection loop.")
                    break
                
                log.debug("Clicking next button.")
                await next_button.click(force=True)
                await page.wait_for_timeout(1000) # wait for table to load
                page_num += 1
            
            await page.close()
            
            log.info(f"Found a total of {len(bill_urls)} bill URLs. Adding to queue...")
            for bill_url in bill_urls:
                await bill_processor_queue.add_task(bill_url)

            log.info("All bill URLs added to the queue. Waiting for workers to finish.")
            await bill_processor_queue.join()

            await verify_and_redownload_files()
 
        except Exception as e:
            log.exception(f"Failed to scrape legislative metadata: {e}")
        finally:
            log.info("Closing browser and stopping queue manager.")
            await bill_processor_queue.stop()
            await browser.close()


async def process_bill_page(context, bill_url):
    log.debug(f"Processing bill URL: {bill_url}")
    page = await context.new_page()
    try:
        await page.goto(bill_url, wait_until="networkidle", timeout=60000)
        log.debug(f"Bill page loaded: {bill_url}")

        # Scrape metadata
        legislation_number = await page.locator("#ContentPlaceHolder1_divLegislationNumber").inner_text()
        legislation_title = await page.locator("#ContentPlaceHolder1_divLegislationTitle").inner_text()
        legislation_description = await page.locator("#ContentPlaceHolder1_divLegislationDescription").inner_text()
        sponsor = await page.locator("#ContentPlaceHolder1_divSponsor").inner_text()
        co_sponsors = await page.locator("#ContentPlaceHolder1_divCoSponsor").inner_text()
        status = await page.locator("#ContentPlaceHolder1_divStatus").inner_text()

        metadata = {
            "url": bill_url,
            "legislation_number": legislation_number,
            "title": legislation_title,
            "description": legislation_description,
            "sponsor": sponsor,
            "co_sponsors": co_sponsors,
            "status": status,
            "documents": []
        }

        # Set the number of entries to 100 for the documents table
        try:
            log.debug("Attempting to set number of entries to 100 for documents table.")
            await page.select_option("select[name='DataTables_Table_0_length']", "100", timeout=5000)
            await page.wait_for_timeout(1000) # wait for table to reload
        except Exception:
            log.warning(f"Could not set 'DataTables_Table_0_length' on {bill_url}. The table may not exist or already show all entries.")

        pdf_links = await page.locator("td.TableLnks a[href*='/api/FileInfo/GetUri/']").all()
        log.debug(f"Found {len(pdf_links)} PDF links on bill page.")
        for j, pdf_link in enumerate(pdf_links):
            log.debug(f"Processing link {j+1}/{len(pdf_links)} on bill page...")
            href = await pdf_link.get_attribute("href")
            if href:
                full_pdf_url = f"http://dibb.nnols.org{href}"
                file_name = full_pdf_url.split("=")[-1] + ".pdf"
                download_path = Path("data/dibb/bills") / file_name
                
                download_status = await download_file(full_pdf_url, download_path)
                
                document_title = await pdf_link.inner_text()
                
                metadata["documents"].append({
                    "title": document_title,
                    "url": full_pdf_url,
                    "local_path": str(download_path),
                    "download_status": download_status
                })
        
        # Save metadata
        metadata_filename = legislation_number.replace("/", "-") + ".json"
        metadata_path = Path("data/dibb/bills") / metadata_filename
        with open(metadata_path, "w") as f:
            import json
            json.dump(metadata, f, indent=4)
        log.info(f"Saved metadata for {legislation_number} to {metadata_path}")

    except Exception:
        log.exception(f"Failed to process bill page: {bill_url}")
    finally:
        await page.close()


async def verify_and_redownload_files():
   """
   Verifies that all files listed in the metadata exist, and retries downloading any that are missing.
   """
   log.info("Starting verification and re-download process...")
   metadata_dir = Path("data/dibb/bills")
   json_files = list(metadata_dir.glob("*.json"))
   
   if not json_files:
       log.warning("No metadata files found to verify.")
       return

   failed_downloads = []
   for json_file in json_files:
       with open(json_file, "r") as f:
           import json
           try:
               metadata = json.load(f)
               for doc in metadata.get("documents", []):
                   # Check for "Failed" status and also if the file doesn't exist, just in case.
                   if doc.get("download_status") == "Failed" or not Path(doc.get("local_path", "")).exists():
                       # But don't try to re-download files that were not found.
                       if doc.get("download_status") != "Not Found":
                           failed_downloads.append(doc)
           except json.JSONDecodeError:
               log.error(f"Could not decode JSON from {json_file}")

   if failed_downloads:
       log.info(f"Found {len(failed_downloads)} failed or missing downloads. Retrying...")
       for doc in failed_downloads:
           url = doc.get("url")
           path_str = doc.get("local_path")
           if url and path_str:
               path = Path(path_str)
               log.info(f"Retrying download for {url}")
               await download_file(url, path)
           else:
               log.warning(f"Skipping retry for document due to missing URL or path in metadata: {doc.get('title')}")

   else:
       log.info("No failed downloads to retry.")

   # Final verification
   log.info("Performing final verification of all documents...")
   missing_files_after_retry = []
   for json_file in json_files:
       with open(json_file, "r") as f:
           import json
           try:
               metadata = json.load(f)
               for doc in metadata.get("documents", []):
                   path_str = doc.get("local_path")
                   if not path_str or not Path(path_str).exists():
                       missing_files_after_retry.append(doc)
           except json.JSONDecodeError:
               log.error(f"Could not decode JSON from {json_file}")

   if missing_files_after_retry:
       log.warning(f"Found {len(missing_files_after_retry)} missing files after final verification:")
       for doc in missing_files_after_retry:
           log.warning(f"  - {doc.get('local_path')} (from {doc.get('url')})")
   else:
       log.info("All files verified successfully.")