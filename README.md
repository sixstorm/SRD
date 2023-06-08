# SRD
Simple Reddit Digest

This is a personal, small project, using Python, PRAW, and Jinja, producing a small, self-hostable image only site, powered by Reddit content.  Media is downloaded locally for offline usage.

## Quick Stats

- Docker Container based on 'nginx:alpine'.
- JSON file for simple settings.
- By default, updates run every hour.

**Upcoming Reddit API changes could break this project entirely**

## What Works

- Docker container building, creation, and usage works!
- Built-in Python scripts for scraping content; by default, top of the day.
  - JPG, JPEG, PNG, and GIF
- Cleanup task
  - Keeps media from the last 24 hours

## Coming Soon

- GIFV/MP4 support
- Settings Page (maybe, JSON is easy enough)
- Options
  - Time range of Reddit search (day, week, month, etc)
  - Limit of how many items are downloaded
- Get this container into the Docker Registry

## Setup (WIP, Always Changing)

Log into your Reddit account and create a new application.  Take note of the Client ID and Secret.

Build the Docker container locally:

```
docker build -t sixstorm/srd .
```

You can run the container with this command:

```
docker run --name SRD -p 80:80 -v ./localsettings:/bin/SRD/settings -d sixstorm/srd
```

Copy 'settings/settings_example.json' to 'settings/settings.json':

```sh
cp settings/settings_example.json settings/settings.json
```

Edit 'settings.json' in your text editor of choice and fill in the Client ID and Secret from your Reddit Application.  Make sure to put something like your username, in the "User Agent" variable.

Once all settings are in 'settings.json', run the main Python script.

```sh
python3 /bin/SRD/Scrape.py

-OR-

docker exec -d SRD python3 /bin/SRD/Scrape.py
```