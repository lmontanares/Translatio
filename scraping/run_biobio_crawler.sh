#!/usr/bin/env bash

# Navigate to the project directory
# Change this to the path of the project on your machine
cd /home/somebody/dev/Translatio/scraping/biobio || exit

# Truncate the log file
truncate -s 0 /var/log/scrapy/scrapy.log

# Start the crawler with logging enabled
nohup poetry run python -m scrapy crawl biobio_crawler -L DEBUG -s LOG_FILE=/var/log/translatio-scrapy/scrapy.log >/dev/null 2>&1 &

# Navigate back to the original directory
cd - || exit
