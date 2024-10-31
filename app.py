from pn import Scraper

scraper = Scraper('https://publicnotices.washingtonpost.com/')

scraper.load_url()
scraper.execute_search('Palace')
scraper.load_all_notices()
scraper.get_notices()

scraper.close()