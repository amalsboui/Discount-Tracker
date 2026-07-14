# Discount Monitoring Platform - Beauty Products Tunisia

This project is a **discount monitoring platform** with a focus on **web scraping**. It tracks promotions and discounts on beauty products in Tunisia by collecting and processing data from multiple e-commerce websites in real time, helping users stay informed about the best offers.

The workflow follows an **ETL (Extract, Transform, Load) process**, with automated updates triggered daily via a cron job and a shell script. The collected data can be visualized through a Streamlit dashboard for easy exploration and analysis.

---

## Features

- Scraping product data from multiple online stores:
  - `PointM`
  - `Fatale`
  - `BeautyStore`
- Extracted information includes:
  - Product name
  - Brand
  - Current price
  - Old price
  - Discount percentage
  - Date of promotion
  - Link to product page
  - Product image
- Automatic data cleaning and normalization
- Dashboard visualization with **Streamlit**
- Daily automated scraping using **cron jobs** and a **shell script**

---

## Architecture

- **Scrapy**: spiders for each store
- **Pipelines**: clean and transform scraped data
- **PostgreSQL**: database storage using `psycopg2`
- **Streamlit + Pandas**: interactive dashboard
- **Cron job + Shell script**: automated daily scraping

---

## Data Preparation

- Conversion of prices to `float` (removing currency symbols and unnecessary characters like `TND`, `DT`, `À partir de…`)
- Extraction of discount percentages
- Normalization of brand and product names:
  - `.upper()` for brands
  - `.title()` for product names
- Handling incomplete product names by fetching from the **product detail page**
- Handling lazy-loaded images by visiting **product detail pages**
- Validation and cleaning of scraped data

---

## Usage

### Setup

1. Clone the repository:

```bash
git clone https://github.com/amalsboui/Discount-Tracker.git
cd discountscraper
```

2. Create and activate the virtual environment

**Linux / WSL:**

```bash
python -m venv venv2
source venv2/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your database connection in `.env`:

```env
POSTGRES_HOST=<your_host>
POSTGRES_DB=<your_db>
POSTGRES_USER=<your_user>
POSTGRES_PASSWORD=<your_password>
POSTGRES_PORT=<your_port>
```

### Run Scrapers Manually

```bash
cd /path/to/discountscraper/discountscraper
scrapy crawl pointmspider
scrapy crawl fatalespider
scrapy crawl beautystorespider
```

### Run Dashboard

```bash
streamlit run streamlit_app/app.py
```

---

## Automation

The `run_spiders.sh` script executes all spiders sequentially with the virtual environment activated:

```bash
#!/bin/bash
# Activate the virtual environment
source /path/to/venv2/bin/activate
# Navigate to Scrapy project folder
cd /path/to/discountscraper/discountscraper
# Run spiders
scrapy crawl pointmspider
scrapy crawl fatalespider
scrapy crawl beautystorespider
# Optional: deactivate venv
deactivate
```

### Automation (Cron Job)

On Linux / WSL, you can schedule daily scraping with cron:

```bash
crontab -e
```

Add the line:

```bash
0 2 * * * /path/to/discountscraper/run_spiders.sh >> /path/to/discountscraper/spiders.log 2>&1
```

A cron job can trigger this script daily to automatically update the promotions database.

This runs the spiders every day at 2 AM and logs output to `spiders.log`.  
Each time the spiders run, they **update the PostgreSQL database** with the latest promotions from all stores.  
Thanks to this daily update, the **Streamlit dashboard always displays the newest data**, allowing users to visualize the promotions for that day in real time.

---

## Project Workflow

- **Scraping** → Collect promotions data from multiple stores
- **Transformation** → Clean prices, normalize brands/names, calculate discount percentage
- **Stockage** → Store data in PostgreSQL
- **Visualization** → Explore data via Streamlit
- **Automation** → Trigger scraping daily via cron + shell script

---

## Conclusion

- The project successfully collects and centralizes discount information for beauty products in Tunisia.
- Current coverage includes 3 stores and approximately 666 products.
- The workflow ensures that the database is updated daily and the latest promotions can be visualized in real time on the Streamlit dashboard.
