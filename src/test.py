import scraperUtils
import listingIdScraper
import listingScraper
import psycopg2
'''
driver = scraperUtils.get_driver()
listingScraper.scrape_listings(driver, ["3175599"])

driver.quit()

conn = psycopg2.connect(
    dbname="kv_db",
    user="postgres",
    password="nqajX5mdaz",
    host="localhost",  # or your remote host
    port="5432"
)


with conn.cursor() as curs:
    curs.execute("CREATE TABLE apartment_sale (apartmentID int, location varchar(255));")
conn.commit()
conn.close()
#db_version = cur.fetchone()
#print(db_version)
'''

