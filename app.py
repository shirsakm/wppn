from pn import Scraper
from datetime import datetime

scraper = Scraper('https://publicnotices.washingtonpost.com/')

scraper.load_url()
# scraper.execute_search(start_date=datetime(2024, 10, 20))
# scraper.load_all_notices()
# scraper.get_notices()

scraper.close()