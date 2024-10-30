from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from pprint import pprint

class Scraper:
    def __init__(self, URL):
        self.driver = webdriver.Firefox()
        self.URL = URL


    def load_url(self):
        self.driver.get(self.URL)
        sleep(20)

    def execute_search(self, search=None):
        pass


    def get_notices(self):
        load_more = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[3]/button')
        load_more.click()
        sleep(20)
        notices = self.driver.find_elements(By.CLASS_NAME, 'public-notice-result')
        id_list = []
        for notice in notices:
            id_list.append(notice.get_attribute('data-notice-id'))
        pprint(id_list)
        print(len(id_list))


    def close(self):
        self.driver.quit()
