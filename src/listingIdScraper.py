from bs4 import BeautifulSoup
import datetime
from . import scraperUtils
from .logger import logger


def get_listings_amount(driver):
    driver.get(f"https://www.kv.ee/search?deal_type=1")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    amount = scraperUtils.find_listings_amount(soup)
    return amount


def scrape_listing_ids(driver):
    scraperUtils.clear_file("../data/flat-ids2.csv")
    start = 0

    try:
        stop = get_listings_amount(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
        stop = 10500

    print(f"found {stop} listings")

    scrape_start =  datetime.datetime.now()
    for start in range(start, stop, 50):
        try:
            print("Listing id start:", start)
            # Load the URL
            driver.get(f"https://www.kv.ee/search?deal_type=1&start={start}")
            # Get the page source
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            data_object_ids = scraperUtils.get_ids(soup)
            scraperUtils.append_ids(data_object_ids, "../data/flat-ids2.csv")
        except Exception as e:
            string = f"An error occurred while fetching ids (start/stop):({start}/{stop}): {e}"
            print(string)
            logger.error(string)
            continue

    logger.info(f"{stop}, listing Ids scraped and saved in: {datetime.datetime.now() - scrape_start}")