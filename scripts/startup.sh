#! /bin/sh

# Run CRON
crond -f -l 8 &

# First run of SRD
python3 /bin/SRD/Scrape.py