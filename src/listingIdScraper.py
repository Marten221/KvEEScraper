from bs4 import BeautifulSoup
import datetime
import scraperUtils
from logger import logger


def get_listings_amount(driver, deal_type):
    driver.get(f"https://www.kv.ee/search?deal_type={deal_type}")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    amount = scraperUtils.find_listings_amount(soup)
    return amount


def scrape_listing_ids(driver, deal_type):
    scraped_ids = set()
    start = 0

    try:
        stop = get_listings_amount(driver, deal_type)
    except Exception as e:
        print(f"An error occurred getting listings amount: {e}")
        stop = 10500

    print(f"found {stop} listings")

    scrape_start =  datetime.datetime.now()
    for start in range(start, stop, 50):
        try:
            print("Listing id start:", start)
            # Load the URL
            driver.get(f"https://www.kv.ee/search?deal_type={deal_type}&start={start}")
            # Get the page source
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            data_object_ids = scraperUtils.get_ids(soup)
            scraped_ids.update(data_object_ids)
        except Exception as e:
            string = f"An error occurred while fetching ids (start/stop):({start}/{stop}): {e}"
            print(string)
            logger.error(string)
            continue

    logger.info(f"{stop}, listing Ids scraped: {datetime.datetime.now() - scrape_start}")
    return scraped_ids