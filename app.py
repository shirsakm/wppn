from pn import Scraper
from datetime import datetime

scraper = Scraper('https://publicnotices.washingtonpost.com/')
scraper.search(search_phrase='Palace')
scraper.save_all_notices('./data/notices')
scraper.close()
