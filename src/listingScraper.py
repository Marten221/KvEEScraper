import time

from bs4 import BeautifulSoup

import scraperUtils


def scrapeListings(driver, ids):
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

            dictionary = scraperUtils.getFeatures(soup)
            dictionary['hind'] = scraperUtils.getPrice(soup)
            dictionary['id'] = listingId
            dictionary = scraperUtils.cleanDictionary(dictionary)
            dictionary.update(scraperUtils.getLocation(soup))

            scraperUtils.writeData(dictionary, "../data/listings_data.csv")
        except Exception as e:
            print(f"An error occurred while fetching listing {ids[i]}: {e}")
            continue

    print(f"{len(ids)} listings scraped in:", start_time - time.time())
