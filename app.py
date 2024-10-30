from pn import Scraper

scraper = Scraper('https://publicnotices.washingtonpost.com/')

scraper.load_url()
scraper.get_notices()

scraper.close()