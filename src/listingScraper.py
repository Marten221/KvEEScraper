import time

from bs4 import BeautifulSoup

import scraperUtils, db_utils
from logger import logger

def scrape_listings(driver, cur, ids, deal_type):
    start_time = time.time()

    start = 0
    stop = len(ids)

    for i in range(start, stop):
        try:
            listing_id = ids[i]
            logger.info(f"working on listing({i}/{stop}): {listing_id}")

            driver.get(f"https://www.kv.ee/{listing_id}.html")
            html = driver.page_source

            soup = BeautifulSoup(html, 'lxml')

            dictionary = scraperUtils.get_features(soup)
            dictionary['hind'] = scraperUtils.get_price(soup, deal_type)
            dictionary['id'] = listing_id
            dictionary = scraperUtils.clean_dictionary(dictionary)
            dictionary.update(scraperUtils.get_location(soup))
            dictionary = scraperUtils.add_deal_type_to(dictionary, deal_type)

            db_utils.insert_data(cur, dictionary)
        except Exception as e:
            string = f"An error occurred while fetching listing {ids[i]}: {e}"
            print(string)
            logger.error(string)
            continue

    print(f"{len(ids)} listings scraped in:", time.time() - start_time)

