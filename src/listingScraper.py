from bs4 import BeautifulSoup

import scraperUtils
import time
start_time = time.time()

ids = scraperUtils.readIds()
start = 6349
end = len(ids) - 1

driver = scraperUtils.getDriver()
for i in range(start, end):
    listingId = ids[i]
    print(f"working on listing({i}/{end}):", listingId)

    driver.get(f"https://www.kv.ee/{listingId}.html")
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')

    dictionary = scraperUtils.getFeatures(soup)
    dictionary['hind'] = scraperUtils.getPrice(soup)
    dictionary['id'] = listingId
    dictionary = scraperUtils.cleanDictionary(dictionary)
    dictionary.update(scraperUtils.getLocation(soup))

    scraperUtils.writeData(dictionary)


driver.quit()


end_time = time.time()
total_time = end_time - start_time

print("process finished in:", total_time)