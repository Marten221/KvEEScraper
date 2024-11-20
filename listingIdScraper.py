import random
from time import sleep
import scraperUtils


driver = scraperUtils.getDriver()

for start in range(0, 10377, 50):
    print(start)
    # Load the URL
    driver.get(f"https://www.kv.ee/search?deal_type=1&start={start}")
    # Get the page source
    html = driver.page_source
    data_object_ids = scraperUtils.getIds(html)
    scraperUtils.writeIds(data_object_ids)

    sleeptime = random.randint(300, 1300) / 1000
    print("sleeping for:", sleeptime)
    sleep(sleeptime)


driver.quit()


