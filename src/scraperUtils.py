import csv
import logging
import os
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint
from time import sleep

import undetected_chromedriver as uc
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))


def append_ids(data_object_ids, location):
    location = os.path.join(script_dir, location)
    with open(location, mode="a", newline='', encoding='UTF-8') as file:
        file.write(",".join(data_object_ids))
        file.write(",")
    print(f"{len(data_object_ids)} Ids appended to:", location, "\n")


def clear_file(location):
    location = os.path.join(script_dir, location)
    with open(location, 'w') as file:
        pass
    print(location, "cleared")


# id, maakond, linn, linnaosa, pind, tube, magamistube, korrus, korruseid, ehitusaasta, seisukord, energiamärgis, hind
fieldnames = ["id", "maakond", "linn", "linnaosa", "üldpind", "tube", "magamistube", "korrus", "korruseid",
              "ehitusaasta", "seisukord", "energiamärgis", "hoone materjal", "omandivorm", "hind"]


def write_data(dictionary, location):
    location = os.path.join(script_dir, location)
    with open(location, mode="a", newline='', encoding='UTF-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(dictionary)
    print("1 row of data appended to:", location, "\n")


def get_ids(soup):
    elements = soup.find_all(attrs={"data-object-id": True})
    data_object_ids = [element['data-object-id'] for element in elements]

    return data_object_ids


def read_ids(location):
    location = os.path.join(script_dir, location)
    with open(location, mode="r") as file:
        line = file.readline()
    return line.split(",")


def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    # Disable images, fonts, stylesheets to save bandwith
    prefs = {"profile.managed_default_content_settings.images": 2,
             "profile.managed_default_content_settings.stylesheets": 2,
             "profile.managed_default_content_settings.fonts": 2,
             }
    options.add_experimental_option("prefs", prefs)

    return uc.Chrome(options=options)


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


def get_price(soup):
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


valid_keys = fieldnames


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


def find_listings_amount(soup):
    span = soup.find('span', class_='large stronger')
    amount_elements = span.text.strip().split(" ")
    amount = amount_elements[-1].split('\u00A0')
    return int(''.join(amount))


def sleep_with_countdown():
    sleep_time = randint(6 * 10, 8 * 10)  # TODO CHANGE 10 - 3600
    while sleep_time > 0:
        hours, remainder = divmod(sleep_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"\rTime left: {hours:02d}:{minutes:02d}:{seconds:02d}", flush=True, end='')
        sleep(1)
        sleep_time -= 1
    print("\nDone sleeping!")


def git_commit_and_push(message):
    sleep(10)
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Automated commit \n{message}"], check=True)
        subprocess.run(["git", "push"], check=True)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")


def send_email(subject, body, receiver_email):
    # Gmail credentials
    try:
        load_dotenv("./email_credentials.env")
        sender_email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")  # Use your app password or regular password if less secure access is enabled
    except Exception as e:
        error = f"Failed to read email credentials from .env: {e}"
        logging.error(error)
        print(error)

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
