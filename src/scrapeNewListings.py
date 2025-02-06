import datetime
import os

from . import scraperUtils
from .logger import logger
from . import listingIdScraper
from . import listingScraper

recipient = "ojasaarmarten@gmail.com"

#scraperUtils.sleepWithCountdown()

scraperUtils.send_email("Started scraping for new listings", str(datetime.datetime.now()), recipient)

driver = scraperUtils.get_driver()
# Populate flat-ids2.csv
listingIdScraper.scrape_listing_ids(driver)

new_and_old_listings = scraperUtils.read_ids("../data/flat-ids2.csv")
old_listings = scraperUtils.read_ids("../data/flat-ids.csv")
only_new_listings = list(set(new_and_old_listings) - set(old_listings))
print("Amount of new listings found:", len(only_new_listings), "\n")

scrape_start = datetime.datetime.now()
string = f"Started scraping {len(only_new_listings)} listings."
print(scrape_start, string)
logger.info(string)

listingScraper.scrape_listings(driver, only_new_listings)  # Start scraping

scrape_end = datetime.datetime.now()
string = f"Finished scraping {len(only_new_listings)} listings."
print(scrape_end, string)
logger.info(string)

print("Scrape finished in:", scrape_end - scrape_start)
scrape_finish_message = f"Scrape was finished, yielding {len(only_new_listings)} new listings. Taking {scrape_end - scrape_start}\n"
logger.info(scrape_finish_message)
scraperUtils.send_email(scrape_finish_message, str(datetime.datetime.now()), recipient)

scraperUtils.append_ids(only_new_listings,
                       "../data/flat-ids.csv")  # Append freshly scraped listings ids to the scraped listings file

driver.quit()
#Git commit and push
scraperUtils.git_commit_and_push(scrape_finish_message)
# Sleep
#scraperUtils.sleepWithCountdown()
os.system('clear')
