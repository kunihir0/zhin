"""
Scrapers for opvp.navajo-nsn.gov.
"""
import os
import re
from pathlib import Path
import httpx
from playwright.async_api import async_playwright
from logger import get_logger
import json
from urllib.parse import urljoin
from queue_system import QueueManager
from progress import ProgressBar
from scrapers.nnols_scrapers import download_file

log = get_logger(__name__)

async def scrape_opvp_roster():
    """
    Scrapes the administration roster from opvp.navajo-nsn.gov.
    """
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            # Navigate to the live administration page
            roster_url = "https://opvp.navajo-nsn.gov/administration/"
            await page.goto(roster_url, wait_until="networkidle", timeout=60000)
            log.debug("OPVP roster page loaded from live URL.")

            roster = []
            
            sections = await page.locator('.et_pb_section.et_section_regular').all()
            log.debug(f"Found {len(sections)} sections.")

            current_group = None
            for section in sections:
                # Check for a heading that defines the group
                heading_element = section.locator('h1.et_pb_module_heading').first
                if await heading_element.count() > 0:
                    current_group = await heading_element.inner_text()
                    log.info(f"Processing group: {current_group}")

                team_members = await section.locator('.et_pb_team_member').all()
                if not team_members:
                    continue

                log.debug(f"Found {len(team_members)} team members in this section.")
                for member in team_members:
                    name_element = member.locator('h4.et_pb_module_header')
                    name = await name_element.inner_text() if await name_element.count() > 0 else "N/A"

                    position_element = member.locator('p.et_pb_member_position')
                    position = await position_element.inner_text() if await position_element.count() > 0 else "N/A"
                    
                    image_element = member.locator('.et_pb_team_member_image img')
                    photo_url = await image_element.get_attribute('src') if await image_element.count() > 0 else None

                    email_element = member.locator('.et_pb_team_member_description a[href^="mailto:"]')
                    email = await email_element.inner_text() if await email_element.count() > 0 else None
                    if email:
                        email = email.strip()

                    org_link_element = member.locator('.et_pb_team_member_description a:not([href^="mailto:"])')
                    org_url = await org_link_element.get_attribute('href') if await org_link_element.count() > 0 else None

                    member_data = {
                        "name": name,
                        "title": position,
                        "photo_url": photo_url,
                        "email": email,
                        "group": current_group,
                        "org_url": org_url
                    }
                    roster.append(member_data)
                    log.info(f"Scraped data for {name}")

            # Save the roster to a single file
            output_dir = Path("data/opvp")
            output_dir.mkdir(exist_ok=True)
            roster_path = output_dir / "roster.json"
            
            with open(roster_path, "w") as f:
                json.dump(roster, f, indent=4)
            log.info(f"OPVP roster saved to {roster_path}")

        except Exception as e:
            log.error(f"Failed to scrape OPVP roster: {e}")
        finally:
            await browser.close()

async def process_opvp_press_release(context, url):
    """
    Processes a single press release page and saves it as a Markdown file.
    """
    page = await context.new_page()
    try:
        log.info(f"Processing press release: {url}")
        await page.goto(url, wait_until="networkidle", timeout=60000)

        title = await page.locator('h1.entry-title').inner_text()
        date = await page.locator('p.post-meta').inner_text()
        
        # Optionally get the main image URL
        image_locator = page.locator('.et_post_meta_wrapper > img')
        image_url = None
        if await image_locator.count() > 0:
            image_url = await image_locator.get_attribute('src')
        
        # Get all paragraphs from the entry-content
        paragraphs = await page.locator('div.entry-content p').all_inner_texts()
        
        # Sanitize title to create a valid filename
        sanitized_title = re.sub(r'[^\w\-_\. ]', '_', title).strip().lower().replace(' ', '-')
        
        output_dir = Path("data/opvp/press_releases")
        output_dir.mkdir(exist_ok=True)
        
        # Construct Markdown content
        markdown_content = f"# {title}\n\n"
        markdown_content += f"**{date}**\n\n"
        if image_url:
            # Embed image using Markdown syntax with the direct URL
            markdown_content += f"![{title}]({image_url})\n\n"
        
        for p in paragraphs:
            # Filter out any unwanted share text or empty paragraphs
            if p.strip() and "Share" not in p:
                markdown_content += f"{p.strip()}\n\n"
        
        # Save as a Markdown file
        output_path = output_dir / f"{sanitized_title}.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        log.info(f"Saved press release as Markdown: {output_path}")

    except Exception as e:
        log.error(f"Failed to process press release {url}: {e}")
    finally:
        await page.close()

async def scrape_opvp_press_releases(headless=True):
    """
    Scrapes press releases from the OPVP website using the "Scrape, Then Paginate" strategy.
    """
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=headless)
        context = await browser.new_context()
        
        async def worker_coro(url):
            await process_opvp_press_release(context, url)

        press_release_queue = QueueManager(
            worker_coro=worker_coro,
            num_workers=5,
            name="OpvpPressReleaseProcessor"
        )
        await press_release_queue.start()

        page = await context.new_page()
        try:
            await page.goto("https://opvp.navajo-nsn.gov/press-room/")
            log.info("Navigated to OPVP press release page.")

            master_urls = set()

            while True:
                # Scrape all URLs on the current page
                articles = await page.locator('article.et_pb_post').all()
                log.info(f"Found {len(articles)} articles on the current page.")
                for article in articles:
                    url = await article.locator('h2.entry-title a').get_attribute('href')
                    if url:
                        master_urls.add(url)

                # Check for and click the "Older Entries" button
                older_entries_button = page.locator('a:has-text("« Older Entries")')
                if await older_entries_button.count() > 0:
                    log.info("Clicking 'Older Entries' to load more posts...")
                    if not headless:
                        await older_entries_button.evaluate("element => element.style.border = '2px solid red'")
                    await older_entries_button.click()
                    await page.wait_for_timeout(2000) # Wait for content to load
                else:
                    log.info("No more 'Older Entries' button found. All pages scraped.")
                    break
            
            urls_to_process = list(master_urls)
            log.info(f"Found {len(urls_to_process)} unique press release URLs. Adding to queue.")
            
            progress_bar = ProgressBar(len(urls_to_process), text="Scraping OPVP Press Releases")

            async def worker_with_progress(url):
                await process_opvp_press_release(context, url)
                progress_bar.update()

            press_release_queue.worker_coro = worker_with_progress

            for url in urls_to_process:
                await press_release_queue.add_task(url)

            await press_release_queue.join()
            progress_bar.finish()

        except Exception as e:
            log.error(f"An error occurred during the OPVP press release scraping process: {e}")
        finally:
            await press_release_queue.stop()
            await page.close()
            await browser.close()