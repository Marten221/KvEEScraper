import csv

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def writeIds(data_object_ids):
    with open("flat-ids.csv", mode="a", newline='', encoding='UTF-8') as file:
        file.write(",".join(data_object_ids))
        file.write(",")
    print("Data saved to flat-ids.csv")

# id, maakond, linn, linnaosa, pind, tube, magamistube, korrus, korruseid, ehitusaasta, seisukord, energiamärgis, hind
fieldnames = ["id", "maakond", "linn", "linnaosa", "üldpind", "tube", "magamistube", "korrus", "korruseid", "ehitusaasta", "seisukord", "energiamärgis", "hoone materjal", "omandivorm", "hind"]
def writeData(dictionary):
    with open("listings_data.csv", mode="a", newline='', encoding='UTF-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(dictionary)


def getIds(html):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all(attrs={"data-object-id": True})
    data_object_ids = [element['data-object-id'] for element in elements]

    return data_object_ids


def readIds():
    with open("flat-ids.csv", mode="r") as file:
        line = file.readline()
    return line.split(",")


def getDriver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    return uc.Chrome(options=options)


def getFeatures(soup):
    dictionary = dict()
    table_div = soup.find('div', class_="meta-table")
    table = table_div.find('table', class_='table-lined')
    # Extract all rows from the table
    rows = table.find_all('tr')
    for row in rows:
        table_headers = row.find_all('th')
        header_values = [header.text for header in table_headers]
        cells = row.find_all('td')
        cell_values = [cell.text for cell in cells]
        if len(header_values) < 1 or len(cell_values) < 1:
            continue
        dictionary[header_values.pop(0).strip().lower()] = cell_values.pop(0).strip().lower()
    return dictionary


def getPrice(soup):
    price_div = soup.find('div', class_='label campaign')
    price = price_div.get('data-price') if price_div else None
    return price


def getLocation(soup):
    heading_el = soup.find('h1')
    heading = heading_el.text if heading_el else None
    address_parts = [part.strip().lower() for part in heading.split(',')]
    dictionary = dict()
    dictionary['maakond'] = address_parts[-1] if len(address_parts) >= 1 else None
    dictionary['linn'] = address_parts[-2] if len(address_parts) >= 2 else None
    dictionary['linnaosa'] = address_parts[-3] if len(address_parts) >= 3 else None
    return dictionary


valid_keys = fieldnames
def cleanDictionary(dictionary):
    # ÜLDPIND
    pind = dictionary.get('üldpind')  # non-breaking space
    dictionary['üldpind'] = pind.split('\u00A0')[0] if pind else None

    if "katastrinumber" in dictionary.keys():
        dictionary.pop("katastrinumber")

    if "korrus/korruseid" in dictionary.keys():
        korrused = dictionary.pop("korrus/korruseid")
        dictionary['korrus'] = korrused.split("/")[0] if korrused else None
        dictionary['korruseid'] = korrused.split("/")[1] if korrused else None

    filtered_dictionary = {k: v for k, v in dictionary.items() if k in valid_keys}

    return filtered_dictionary

