import time

from bs4 import BeautifulSoup

from . import scraperUtils
from .logger import logger


def scrape_listings(driver, ids):
    start_time = time.time()

    start = 0
    stop = len(ids)

    for i in range(start, stop):
        try:
            listingId = ids[i]
            print(f"working on listing({i}/{stop}):", listingId)

            driver.get(f"https://www.kv.ee/{listingId}.html")
            html = driver.page_source

            soup = BeautifulSoup(html, 'lxml')

            dictionary = scraperUtils.get_features(soup)
            dictionary['hind'] = scraperUtils.get_price(soup)
            dictionary['id'] = listingId
            dictionary = scraperUtils.clean_dictionary(dictionary)
            dictionary.update(scraperUtils.get_location(soup))

            scraperUtils.write_data(dictionary, "../data/listings_data.csv")
        except Exception as e:
            string = f"An error occurred while fetching listing {ids[i]}: {e}"
            print(string)
            logger.error(string)
            continue

    print(f"{len(ids)} listings scraped in:", start_time - time.time())

