import datetime

import scraperUtils
from logger import logger
from src import listingIdScraper
from src import listingScraper

scrape_nr = 1
# Logimine
# try catch, et kõik kokku ei jookseks ühe postituse pärast #Done
# Vb proovi andmebaasiga ühendada
#commitib ainult stc kausta. ja loggeri viimased read eu tule kaasa. Ide crashib kui telost sulgen arvutu.Mingi jama connectioni vahetamisega? peale ugat tsüklit võib driveri sulgeda
scraperUtils.sleepWithCountdown()

while True:
    driver = scraperUtils.getDriver()
    # Populate flat-ids2.csv
    listingIdScraper.scrapeListingIds(driver)

    new_and_old_listings = scraperUtils.readIds("../data/flat-ids2.csv")
    old_listings = scraperUtils.readIds("../data/flat-ids.csv")
    only_new_listings = list(set(new_and_old_listings) - set(old_listings))
    print("Amount of new listings found:", len(only_new_listings), "\n")

    scrape_start = datetime.datetime.now()
    string = f"Started scraping {len(only_new_listings)} listings."
    print(scrape_start, string)
    logger.info(string)

    listingScraper.scrapeListings(driver, only_new_listings)  # Start scraping

    scrape_end = datetime.datetime.now()
    string = f"Finished scraping {len(only_new_listings)} listings."
    print(scrape_end, string)
    logger.info(string)

    print("Scrape finished in:", scrape_end - scrape_start)
    scrape_finish_message = f"Scrape nr: {scrape_nr} was finished, yielding {len(only_new_listings)} new listings. Taking {scrape_end - scrape_start}\n"
    logger.info(scrape_finish_message)

    scraperUtils.appendIds(only_new_listings,
                           "../data/flat-ids.csv")  # Append freshly scraped listings ids to the scraped listings file

    driver.quit()
    #Git commit and push
    scraperUtils.git_commit_and_push(scrape_finish_message)
    # Sleep
    scraperUtils.sleepWithCountdown()

