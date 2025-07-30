import os
import psycopg2
from dotenv import load_dotenv

load_dotenv("../credentials.env")

INSERT_COMMAND = """
    INSERT INTO listings (
        listing_id, listing_type_enum, building_type,
        county, city, district, area, rooms, bedrooms,
        floor, nr_of_floors, year_built, condition, energy_mark,
        building_material, ownership_form, price
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def get_cursor():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )
    conn.autocommit = True  # Optional: Auto-commit each insert
    return conn.cursor()

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