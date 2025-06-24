"""
Main script to run all scrapers.
"""
import asyncio
from scrapers.nnols_scrapers import scrape_base_code, scrape_amendments
from scrapers.navajonationcouncil_scrapers import scrape_bills_and_resolutions, scrape_council_member_data
from scrapers.dibb_scrapers import scrape_legislative_metadata
from scrapers.courts_scrapers import scrape_supreme_court_opinions

async def main():
    """
    Main function to run all scrapers.
    """
    await scrape_base_code()
    await scrape_amendments()
    await scrape_bills_and_resolutions()
    await scrape_council_member_data()
    await scrape_legislative_metadata()
    await scrape_supreme_court_opinions()

if __name__ == "__main__":
    asyncio.run(main())