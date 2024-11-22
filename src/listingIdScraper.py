from bs4 import BeautifulSoup

import scraperUtils


def getListingsAmount(driver):
    driver.get(f"https://www.kv.ee/search?deal_type=1")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    amount = scraperUtils.findListingsAmount(soup)
    return amount


def scrapeListingIds(driver):
    scraperUtils.clearFile("../data/flat-ids2.csv")
    start = 0

    try:
        stop = getListingsAmount(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
        stop = 10500

    print(f"found {stop} listings")

    for start in range(start, stop, 50):
        try:
            print("Listing id start:", start)
            # Load the URL
            driver.get(f"https://www.kv.ee/search?deal_type=1&start={start}")
            # Get the page source
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            data_object_ids = scraperUtils.getIds(soup)
            scraperUtils.appendIds(data_object_ids, "../data/flat-ids2.csv")
        except Exception as e:
            print(f"An error occurred while fetching ids (start/stop):({start}/{stop}): {e}")
            continue
