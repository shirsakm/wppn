from selenium import webdriver

class Scraper:
    def __init__(self, URL):
        self.driver = webdriver.Firefox()
        self.URL = URL

    def load(self):
        self.driver.get(self.URL)

    def end(self):
        self.driver.quit()