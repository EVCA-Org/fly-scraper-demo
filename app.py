#!/usr/bin/env python3
import os
import time
import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import schedule

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sample scraper class
class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.data_dir = 'data'
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def scrape_website(self, url):
        Scrape a website and return the data
        try:
            logger.info(f'Scraping {url}')
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example: scrape all article titles from a news site
            articles = []
            for article in soup.select('article'):
                title_element = article.select_one('h2')
                if title_element:
                    title = title_element.get_text().strip()
                    articles.append({'title': title})
            
            return articles
        
        except Exception as e:
            logger.error(f'Error scraping {url}: {e}')
            return []
    
    def save_data(self, data):
        Save the scraped data to a JSON file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.data_dir, f'scraped_data_{timestamp}.json')
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f'Data saved to {filename}')
    
    def run_scraper(self):
        Run the scraper on a sample news website
        url = 'https://news.ycombinator.com/'  # Hacker News as an example
        data = self.scrape_website(url)
        
        if data:
            self.save_data(data)
            logger.info(f'Successfully scraped {len(data)} items')
        else:
            logger.warning('No data was scraped')

# Main function to run the scraper
def main():
    scraper = WebScraper()
    
    # For testing: Run once immediately
    scraper.run_scraper()
    
    # Schedule to run every hour
    schedule.every(1).hours.do(scraper.run_scraper)
    
    # Keep the script running to execute scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    logger.info('Starting web scraper')
    main()
