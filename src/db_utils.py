import os
import psycopg2
from dotenv import load_dotenv

load_dotenv("../credentials.env")

INSERT_COMMAND = """
    INSERT INTO listings (
        listing_id, listing_type_enum, building_type_enum,
        county, city, district, area, rooms, bedrooms,
        floor, nr_of_floors, year_built, condition, energy_mark,
        ownership_form, price
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )
    conn.autocommit = True  # Optional: Auto-commit each insert
    return conn

def get_existing_ids(cur):
    cur = get_connection().cursor()
    cur.execute("SELECT listing_id FROM listings")
    return set(row[0] for row in cur.fetchall())

def insert_data(cur, dictionary):
    cur.execute(INSERT_COMMAND, (
        dictionary.get("id"),
        dictionary.get("listing_type_enum"),
        dictionary.get("building_type_enum"),
        dictionary.get("maakond"),
        dictionary.get("linn"),
        dictionary.get("linnaosa"),
        dictionary.get("üldpind"),
        dictionary.get("tube"),
        dictionary.get("magamistube"),
        dictionary.get("korrus"),
        dictionary.get("korruseid"),
        dictionary.get("ehitusaasta"),
        dictionary.get("seisukord"),
        dictionary.get("energiamärgis"),
        dictionary.get("omandivorm"),
        dictionary.get("hind")
    ))

'''
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'listing_type_enum') THEN
        CREATE TYPE listing_type_enum AS ENUM ('sale', 'rent');
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'building_type_enum') THEN
        CREATE TYPE building_type_enum AS ENUM ('flat', 'house');
    END IF;
END
$$;

CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    listing_id TEXT UNIQUE NOT NULL,

	listing_type_enum listing_type_enum,
	building_type building_type_enum,
    county TEXT,
    city TEXT,
    district TEXT,
    area REAL,
    rooms INTEGER,
    bedrooms INTEGER,
    floor INTEGER,
    nr_of_floors INTEGER,
    year_built INTEGER,
    condition TEXT,
    energy_mark TEXT,
    building_material TEXT,
    ownership_form TEXT,
    price INTEGER,

    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''