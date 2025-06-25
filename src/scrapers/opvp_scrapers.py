"""
Scrapers for opvp.navajo-nsn.gov.
"""
import os
from pathlib import Path
import httpx
from playwright.async_api import async_playwright
from logger import get_logger
import json

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
            # Load the local HTML file
            html_file_path = os.path.abspath('nnop_roster.html')
            await page.goto(f'file://{html_file_path}')
            log.debug("OPVP roster page loaded from local file.")

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