import csv
import logging
import os
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint
from time import sleep
import re

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def get_ids(soup):
    elements = soup.find_all(attrs={"data-object-id": True})
    data_object_ids = set(element['data-object-id'] for element in elements)

    return data_object_ids

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.set_preference("general.useragent.override",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )
    options.set_preference("permissions.default.image", 2)
    options.set_preference("permissions.default.stylesheet", 2)
    options.set_preference("permissions.default.font", 2)

    return webdriver.Firefox(options=options)


def get_features(soup):
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


def get_price(soup, deal_type):
    if deal_type % 2 == 0: #types 2 and 4 are for rent
        # Find the price-outer div
        price_outer = soup.find('div', class_='price-outer')

        # Get the first div inside it (which contains the price)
        price_div = price_outer.find('div')

        # Get the text from the div, excluding the <small> part
        price_text = price_div.find(text=True, recursive=False)
        price = re.sub(r'\D', '', price_text)
    else:
        price_div = soup.find('div', class_='label campaign')
        price = price_div.get('data-price') if price_div else None

    return price


def get_location(soup):
    heading_el = soup.find('h1')
    heading = heading_el.text if heading_el else None
    address_parts = [part.strip().lower() for part in heading.split(',')]
    dictionary = dict()
    dictionary['maakond'] = address_parts[-1] if len(address_parts) >= 1 else None
    dictionary['linn'] = address_parts[-2] if len(address_parts) >= 2 else None
    dictionary['linnaosa'] = address_parts[-3] if len(address_parts) >= 3 else None
    return dictionary



valid_keys = ["id", "maakond", "linn", "linnaosa", "üldpind", "tube", "magamistube", "korrus", "korruseid",
              "ehitusaasta", "seisukord", "energiamärgis", "hoone materjal", "omandivorm", "hind"]

def clean_dictionary(dictionary):
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

def add_deal_type_to(dictionary, deal_type):
    if deal_type == 1:
        dictionary["listing_type_enum"] = "sale"
        dictionary["building_type_enum"] = "flat"
    elif deal_type == 2:
        dictionary["listing_type_enum"] = "rent"
        dictionary["building_type_enum"] = "flat"
    elif deal_type == 3:
        dictionary["listing_type_enum"] = "sale"
        dictionary["building_type_enum"] = "house"
    elif deal_type == 4:
        dictionary["listing_type_enum"] = "rent"
        dictionary["building_type_enum"] = "house"
    return dictionary


def find_listings_amount(soup):
    span = soup.find('span', class_='large stronger')
    amount_elements = span.text.strip().split(" ")
    amount = amount_elements[-1].split('\u00A0')
    return int(''.join(amount))



def send_email(subject, body, receiver_email):
    # Gmail credentials
    try:
        load_dotenv("./credentials.env")
        sender_email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")  # Use your app password or regular password if less secure access is enabled
    except Exception as e:
        error = f"Failed to read email credentials from .env: {e}"
        logging.error(error)

    # Create email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Encrypt connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        print(f"Failed to send email: {e}")
