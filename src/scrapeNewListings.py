import datetime

import scraperUtils
from logger import logger
from src import listingIdScraper
from src import listingScraper

scrape_nr = 1
# Logimine
# try catch, et kõik kokku ei jookseks ühe postituse pärast #Done
# Vb proovi andmebaasiga ühendada

driver = scraperUtils.getDriver()
while True:
    # Populate flat-ids2.csv
    listingIdScraper.scrapeListingIds(driver)

    new_and_old_listings = scraperUtils.readIds("../data/flat-ids2.csv")
    old_listings = scraperUtils.readIds("../data/flat-ids.csv")
    only_new_listings = list(set(new_and_old_listings) - set(old_listings))
    print("Amount of new listings found:", len(only_new_listings), "\n")

    scrape_start = datetime.datetime.now()
    string = f"Started scraping {len(only_new_listings)} listings.\n"
    print(scrape_start, string)
    logger.info(string)

    listingScraper.scrapeListings(driver, only_new_listings)  # Start scraping

    scrape_end = datetime.datetime.now()
    string = f"Finished scraping {len(only_new_listings)} listings.\n"
    print(scrape_end, string)
    logger.info(string)

    print("Scrape finished in:", scrape_end - scrape_start)
    logger.info(
        f"Scrape nr: {scrape_nr} was finished, yielding {len(only_new_listings)} new listings. Taking {scrape_end - scrape_start}\n")

    scraperUtils.appendIds(only_new_listings,
                           "../data/flat-ids.csv")  # Append freshly scraped listings ids to teh scraped listings file

    # Sleep
    scraperUtils.sleep15_24hWithCountdown()
    i += 1

driver.quit()
