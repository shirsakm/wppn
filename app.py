from pn import Scraper

scraper = Scraper('https://publicnotices.washingtonpost.com/')
scraper.load()

scraper.end()