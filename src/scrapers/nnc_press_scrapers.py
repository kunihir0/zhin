"""
Scrapers for Navajo Nation Council press releases.
"""
import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright, Page
from logger import get_logger
from scrapers.nnols_scrapers import download_file
from queue_system import QueueManager
from progress import ProgressBar

log = get_logger(__name__)

async def scrape_press_releases(start_year=2016):
    """
    Scrapes press releases from the Navajo Nation Council website.
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
            log.info("Navigating to press releases archive page...")
            await page.goto("https://www.navajonationcouncil.org/press-releases-archive/", wait_until="networkidle", timeout=60000)
            log.info("Press releases archive page loaded.")

            press_release_queue = QueueManager(
                worker_coro=process_press_release,
                num_workers=10,
                name="PressReleaseProcessor"
            )
            await press_release_queue.start()

            all_press_releases = []
            
            log.info("Extracting all press releases in a single batch...")
            all_press_releases = await page.evaluate("""
                (start_year) => {
                    const releases = [];
                    const tabControls = document.querySelectorAll('ul.et_pb_tabs_controls > li > a');
                    const tabPanels = document.querySelectorAll('div.et_pb_tab');

                    tabControls.forEach((control, index) => {
                        const controlText = control.innerText;
                        const yearMatch = controlText.match(/\\b(20\\d{2})\\b/);
                        if (!yearMatch) {
                            return;
                        }

                        const year = parseInt(yearMatch[1], 10);
                        if (year < start_year) {
                            return;
                        }

                        const panel = tabPanels[index];
                        if (!panel) return;

                        const listItems = panel.querySelectorAll('li');
                        listItems.forEach(item => {
                            const fullText = item.innerText;
                            const dateMatch = fullText.match(/(\\d{1,2}\\/\\d{1,2}\\/\\d{4})/);
                            if (!dateMatch) {
                                return;
                            }
                            const date = dateMatch[1];
                            const title = fullText.replace(date, '').replace('–', '').trim();
                            const link = item.querySelector('a');
                            if (link) {
                                const url = link.href;
                                releases.push({ url, title, date });
                            }
                        });
                    });
                    return releases;
                }
            """, start_year)

            
            log.info(f"Found a total of {len(all_press_releases)} press releases. Adding to queue...")
            
            progress_bar = ProgressBar(len(all_press_releases), text="Downloading Press Releases")
            
            async def worker_with_progress(task_data):
                await process_press_release(task_data)
                progress_bar.update()

            press_release_queue.worker_coro = worker_with_progress

            for release_data in all_press_releases:
                await press_release_queue.add_task(release_data)

            await press_release_queue.join()
            progress_bar.finish()

        except Exception as e:
            log.exception(f"Failed to scrape press releases: {e}")
        finally:
            log.info("Closing browser.")
            await press_release_queue.stop()
            await browser.close()

async def process_press_release(data):
    """
    Processes a single press release.
    """
    try:
        url = data["url"]
        title = data["title"]
        date_text = data["date"]
        
        download_dir = Path("data/nnc_press_releases")
        download_dir.mkdir(exist_ok=True)
        
        file_name = url.split("/")[-1]
        download_path = download_dir / file_name

        download_status = await download_file(url, download_path)

        metadata = {
            "title": title,
            "date": date_text.replace("–", "").strip(),
            "url": url,
            "local_path": str(download_path),
            "download_status": download_status
        }

        metadata_filename = file_name.replace(".pdf", ".json")
        metadata_path = download_dir / metadata_filename
        with open(metadata_path, "w") as f:
            import json
            json.dump(metadata, f, indent=4)
        
        if download_status == "Success":
            log.info(f"Saved metadata for {title} to {metadata_path}")
        else:
            log.warning(f"Saved metadata for {title} to {metadata_path} with status {download_status}")

    except Exception:
        log.exception(f"Failed to process press release: {data.get('url')}")

if __name__ == "__main__":
    asyncio.run(scrape_press_releases())