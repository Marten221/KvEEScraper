import datetime
from logger import logger
import scraperUtils, listingIdScraper, listingScraper
from db_utils import get_connection, get_existing_ids

recipient = "ojasaarmarten@gmail.com"
scraperUtils.send_email("Started scraping for new listings", str(datetime.datetime.now()), recipient)
driver = scraperUtils.get_driver()

listing_types = {"flat_sale": 1, "flat_rent": 2, "house_sale": 3, "house_rent": 4}

conn = get_connection()
cur = conn.cursor()
for listing_type in listing_types:
    # Find new ids
    new_listing_ids = listingIdScraper.scrape_listing_ids(driver, listing_types[listing_type])
    old_listings = get_existing_ids(cur)
    only_new_listings = list(set(new_listing_ids) - set(old_listings))
    #print("Amount of new listings found:", len(only_new_listings), "\n")

    scrape_start = datetime.datetime.now()
    string = f"Started scraping {len(only_new_listings)} listings."
    print(scrape_start, string)
    logger.info(string)

    listingScraper.scrape_listings(driver, cur, only_new_listings, listing_types[listing_type])  # Start scraping

    scrape_end = datetime.datetime.now()
    string = f"Finished scraping {len(only_new_listings)} listings."
    print(scrape_end, string)
    logger.info(string)

    print("Scrape finished in:", scrape_end - scrape_start)
    scrape_finish_message = f"{listing_type} Scrape was finished, yielding {len(only_new_listings)} new listings. Taking {scrape_end - scrape_start}\n"
    logger.info(scrape_finish_message)
    scraperUtils.send_email(scrape_finish_message, str(datetime.datetime.now()), recipient)


driver.quit()
cur.close()
conn.close()