"""
Main script to run all scrapers.
"""
import asyncio
from scrapers.nnols_scrapers import scrape_base_code, scrape_amendments
from scrapers.navajonationcouncil_scrapers import scrape_bills_and_resolutions, scrape_council_member_data
from scrapers.dibb_scrapers import scrape_legislative_metadata
from scrapers.courts_scrapers import scrape_supreme_court_opinions
from scrapers.nnc_press_scrapers import scrape_press_releases
from scrapers.opvp_scrapers import scrape_opvp_roster, scrape_opvp_press_releases
from scrapers.nndoj_scrapers import scrape_nndoj_roster
from logger import get_logger

log = get_logger(__name__)

async def async_main():
    """
    Main asynchronous function to run all scrapers.
    """
    await scrape_base_code()
    await scrape_amendments()
    await scrape_bills_and_resolutions()
    await scrape_council_member_data()
    await scrape_legislative_metadata()
    await scrape_supreme_court_opinions()

def run_press_scraper():
    """
    Synchronous entry point for the press scraper.
    """
    try:
        asyncio.run(scrape_press_releases())
    except KeyboardInterrupt:
        log.info("Exiting...")

def run_council_scraper():
    """
    Synchronous entry point for the council scraper.
    """
    try:
        asyncio.run(scrape_council_member_data())
    except KeyboardInterrupt:
        log.info("Exiting...")


def run_opvp_scraper():
    """
    Synchronous entry point for the OPVP scraper.
    """
    async def opvp_main():
        # Run roster and press release scrapers concurrently
        await asyncio.gather(
            scrape_opvp_roster(),
            scrape_opvp_press_releases()
        )

    try:
        asyncio.run(opvp_main())
    except KeyboardInterrupt:
        log.info("Exiting...")


def run_nndoj_scraper():
    """
    Synchronous entry point for the NNDOJ scraper.
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    try:
        asyncio.run(scrape_nndoj_roster(headless=args.headless))
    except KeyboardInterrupt:
        log.info("Exiting...")


def main():
    """
    Synchronous entry point for the main async function.
    """
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        log.info("Exiting...")