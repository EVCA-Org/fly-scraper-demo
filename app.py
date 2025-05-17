#!/usr/bin/env python3
import os
import time
import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import schedule
import threading
import http.server
import socketserver
from supabase import create_client

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Supabase client
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
SUPABASE_TABLE = os.environ.get('SUPABASE_TABLE', 'scraped_data')

# Validate Supabase configuration
if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning('SUPABASE_URL or SUPABASE_KEY not set. Data will only be saved locally.')
    supabase = None
else:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info('Successfully connected to Supabase')
    except Exception as e:
        logger.error(f'Failed to connect to Supabase: {e}')
        supabase = None

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
        """Scrape a website and return the data"""
        try:
            logger.info(f'Scraping {url}')
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example: scrape all article titles from Hacker News
            articles = []
            for article in soup.select('.title .titleline'):  # HN-specific selector
                if article and article.a:
                    title = article.a.get_text().strip()
                    link = article.a.get('href', '')
                    articles.append({
                        'title': title,
                        'url': link,
                        'source': url,
                        'scraped_at': datetime.now().isoformat()
                    })
            
            return articles
        
        except Exception as e:
            logger.error(f'Error scraping {url}: {e}')
            return []
    
    def save_to_supabase(self, data):
        Save the scraped data to Supabase
        if not supabase:
            logger.warning('Supabase client not available. Data not saved to Supabase.')
            return False
        
        try:
            for item in data:
                result = supabase.table(SUPABASE_TABLE).insert(item).execute()
                # Check if the insert was successful
                if hasattr(result, 'error') and result.error:
                    logger.error(f'Error saving to Supabase: {result.error}')
                    return False
            
            logger.info(f'Successfully saved {len(data)} items to Supabase')
            return True
        except Exception as e:
            logger.error(f'Error saving to Supabase: {e}')
            return False
    
    def save_data_locally(self, data):
        Save the scraped data to a local JSON file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.data_dir, f'scraped_data_{timestamp}.json')
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f'Data saved locally to {filename}')
    
    def run_scraper(self):
        Run the scraper on a sample news website
        url = 'https://news.ycombinator.com/'  # Hacker News as an example
        data = self.scrape_website(url)
        
        if data:
            # Try to save to Supabase first
            if not self.save_to_supabase(data):
                # Fall back to local storage if Supabase save fails
                self.save_data_locally(data)
                
            logger.info(f'Successfully scraped {len(data)} items')
        else:
            logger.warning('No data was scraped')

# Health check server for Fly.io
class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Include basic stats
            stats = {
                'status': 'ok',
                'service': 'fly-scraper-demo',
                'timestamp': datetime.now().isoformat(),
                'environment': os.environ.get('FLY_APP_NAME', 'development')
            }
            
            self.wfile.write(json.dumps(stats).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        logger.info(f'Health check: {args[0]} {args[1]} {args[2]}')

def start_health_server():
    port = int(os.environ.get('PORT', 8080))
    handler = HealthCheckHandler
    httpd = socketserver.TCPServer(('', port), handler)
    logger.info(f'Starting health check server on port {port}')
    httpd.serve_forever()

# Main function to run the scraper
def main():
    # Start the health check server in a separate thread
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    scraper = WebScraper()
    
    # For testing: Run once immediately
    scraper.run_scraper()
    
    # Schedule to run every hour
    schedule_interval = int(os.environ.get('SCRAPER_INTERVAL_HOURS', 1))
    logger.info(f'Scheduling scraper to run every {schedule_interval} hour(s)')
    schedule.every(schedule_interval).hours.do(scraper.run_scraper)
    
    # Keep the script running to execute scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    logger.info('Starting web scraper with Supabase integration')
    main()
