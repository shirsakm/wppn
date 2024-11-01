from wppn import Scraper
from datetime import datetime

scraper = Scraper('https://publicnotices.washingtonpost.com/')

"""
Find below, sample search queries, uncomment to run
"""
scraper.search(search_phrase='Palace')
# scraper.search(start_date=datetime(2024, 10, 15), states=['DC'])
# scraper.search(counties=['Prince George\'s'], notice_types=['Trustee Sales'])

scraper.save_all_notices('./data/notices')
scraper.close()
