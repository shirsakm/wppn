from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

class Scraper:
    def __init__(self, URL):
        self.driver = webdriver.Firefox()
        self.URL = URL


    def load_url(self):
        self.driver.get(self.URL)
        WebDriverWait(self.driver, 30) \
            .until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[3]/button')))


    def load_all_notices(self):
        WebDriverWait(self.driver, 30) \
            .until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[1]')))
        
        notice_number = int(self.driver \
            .find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[1]') \
            .get_attribute('innerHTML') \
            .split(' ')[1])

        if notice_number < 80:
            return

        iters_required = int(notice_number) // 80 + 1
        for _ in range(iters_required):
            load_more = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[3]/button')
            load_more.click()

            WebDriverWait(self.driver, 30) \
                .until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[3]/button')))


    def execute_search(self, search=None):
        if not search:
            return

        search_input = self.driver.find_element(By.ID, 'searchbtn')
        search_input.send_keys(search)
        search_button = self.driver.find_element(By.ID, 'search')
        search_button.click()
        
        WebDriverWait(self.driver, 30) \
            .until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]')))


    def get_notices(self):
        notices = self.driver.find_elements(By.CLASS_NAME, 'public-notice-result')
        id_list = set()
        for notice in notices:
            id_list.add(notice.get_attribute('data-notice-id'))
        pprint(id_list)
        print(len(id_list))


    def close(self):
        self.driver.quit()
