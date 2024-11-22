import scraperUtils
import datetime

from src import listingIdScraper

from src import listingScraper

# Logimine
# try catch, et kõik kokku ei jookseks ühe postituse pärast #Done
# Vb proovi andmebaasiga ühendada


driver = scraperUtils.getDriver()
listingIdScraper.scrapeListingIds(driver)

new_and_old_listings = scraperUtils.readIds("../data/flat-ids2.csv")
old_listings = scraperUtils.readIds("../data/flat-ids.csv")
only_new_listings = list(set(new_and_old_listings) - set(old_listings))
print("Amount of new listings found:", len(only_new_listings), "\n")

scrape_start = datetime.datetime.now()
print(scrape_start, f"Started scraping {len(only_new_listings)} listings.\n")
listingScraper.scrapeListings(driver, only_new_listings)
scrape_end = datetime.datetime.now()
print(scrape_end, f"Finished scraping {len(only_new_listings)} listings.\n")
print("Scrape finished in:", scrape_end - scrape_start)

scraperUtils.appendIds(only_new_listings, "../data/flat-ids.csv")
driver.quit()
