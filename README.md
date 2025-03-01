# KV.ee Apartment Listings Scraper

## Machine learmong model development
https://github.com/RobinHenrik/RealEstatePricePredicing

## Overview
This project is a Python-based web scraper designed to collect real estate data from [KV.ee](https://kv.ee), focusing on apartments for sale in Estonia. The scraper gathers detailed information about active listings and automates daily data collection for market analysis.

## Features
- **Efficient Data Collection**: Gathers essential apartment details, including:
  - `id`: Listing ID
  - `maakond`: County
  - `linn`: City
  - `linnaosa`: District
  - `pind`: Area (m²)
  - `tube`: Total rooms
  - `magamistube`: Bedrooms
  - `korrus`: Floor
  - `korruseid`: Total floors
  - `ehitusaasta`: Year of construction
  - `seisukord`: Condition
  - `energiamärgis`: Energy label
  - `hoone materjal`: Building material
  - `omandivorm`: Ownership type
  - `hind`: Price

- **Incremental Scraping**: Detects and scrapes only new listings by comparing current active listing IDs with previously scraped data.
- **Automation**: Runs daily at 17:00, automatically committing new data to GitHub and sending email notifications before and after scraping.
- **Bot Detection Handling**: Uses Selenium to bypass bot detection and dynamically load pages.

## Technology Stack
- **Programming Language**: Python
- **Libraries & Tools**: Selenium, BeautifulSoup
- **Data Storage**: CSV file (`data/listings_data.csv`)

## Setup & Usage
1. **Install Google Chrome:**
   - Ensure Google Chrome is installed and up to date on your system.
  
2. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   ```

3. **Navigate to the Project Directory:**
   ```bash
   cd <repository-directory>
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Email Notifications:**
   - Create a file named `email_credentials.env` in the root folder with the following content:
     ```
     EMAIL=<your-email@example.com>
     PASSWORD=<your-email-password>
     ```
   - Update the recipient email in `src/scrapeNewListings.py` or comment out lines 15 and 41 to disable email notifications.

6. **Disable Auto Commit (Optional):**
   - Comment out line 48 in `src/scrapeNewListings.py` to prevent automatic commits and pushes to GitHub.

7. **Run the Scraper:**
   ```bash
   python -u -m src.scrapeNewListings
   ```

## Project Impact
- **Market Insights**: Provides comprehensive data on the Estonian apartment market.
- **Machine Learning Integration**: Used to train models for predicting apartment prices and identifying undervalued properties.
- **Recognition**: Contributed to winning the DeltaX student competition.

## Future Improvements
- Implement database storage for scalability.
- Add data visualization for real-time market trends.
- Enhance filtering options for more targeted data collection.

## License
This project is for educational and research purposes.

---
