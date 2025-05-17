# Fly Scraper Demo

A simple web scraper demonstration project set up for deployment on Fly.io.

## Features

- Basic web scraping using BeautifulSoup
- Scheduled scraping jobs
- Data storage in JSON files
- Dockerized deployment
- Ready for Fly.io deployment

## Local Development

1. Install dependencies:
   

2. Run the scraper:
   

## Deployment

Deploy to Fly.io:

Scanning source code
[32mCould not find a Dockerfile, nor detect a runtime or framework from source code. Continuing with a blank app.[0m
Creating app in /
We're about to launch your app on Fly.io. Here's what you're getting:

Organization: adam@evca.org          (fly launch defaults to the personal org)
Name:         bitter-wave-3478       (generated)
Region:       Singapore, Singapore   (this is the fastest region for you)
App Machines: shared-cpu-1x, 1GB RAM (most apps need about 1GB of RAM)
Postgres:     <none>                 (not requested)
Redis:        <none>                 (not requested)
Tigris:       <none>                 (not requested)

Created app 'bitter-wave-3478' in organization 'personal'
Admin URL: https://fly.io/apps/bitter-wave-3478
Hostname: bitter-wave-3478.fly.dev
Wrote config file fly.toml

## Configuration

- Update the scraper URLs and parsing logic in 
- Modify the scraping schedule as needed
- Add environment variables for any API keys or configuration

## License

MIT
