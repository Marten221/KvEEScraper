import scraperUtils
import listingIdScraper
import listingScraper
driver = scraperUtils.get_driver()
listingScraper.scrape_listings(driver, ["3175599"])

driver.quit()