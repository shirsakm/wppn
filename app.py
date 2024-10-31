from pn import Scraper
from datetime import datetime

scraper = Scraper('https://publicnotices.washingtonpost.com/')

# scraper.search(start_date=datetime(2024, 10, 15), end_date=datetime(2024, 11, 1), states=['DC'])
scraper.search(search_phrase='Palace')
scraper.save_all_notices()
scraper.close()