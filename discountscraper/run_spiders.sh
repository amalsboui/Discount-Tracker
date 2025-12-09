#!/bin/bash
# Activate the virtual environment
source /mnt/c/rt4/ML/Project/discountscraper/venv/bin/activate

# Navigate to Scrapy project folder
cd /mnt/c/rt4/ML/Project/discountscraper/discountscraper

# Run spiders
scrapy crawl pointmspider
scrapy crawl fatalespider
scrapy crawl beautystorespider

# Optional: deactivate venv
deactivate
