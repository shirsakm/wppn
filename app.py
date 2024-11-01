from wppn import Scraper
from datetime import datetime

scraper = Scraper('https://publicnotices.washingtonpost.com/')
scraper.search(start_date=datetime(2024, 10, 15), states=['DC'])
scraper.save_all_notices('./data/notices')
scraper.close()
