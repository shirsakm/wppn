from datetime import datetime
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


    def get_current_month(self):
        current_month = self.driver.find_element(By.CSS_SELECTOR, 'div.react-datepicker__current-month') \
            .get_attribute('innerHTML')
        current_month = datetime.strptime(current_month, '%B %Y')
        return current_month    


    def reach_target_date(self, target_date):
        """
        target_date: datetime 
        Requires the date picker to be opened beforehand
        """
        current_month = self.get_current_month()
        while target_date.strftime('%B %Y') != current_month.strftime('%B %Y'):
            if target_date < current_month:
                prev_month_button = self.driver.find_element(By.CSS_SELECTOR, 'button.react-datepicker__navigation.react-datepicker__navigation--previous')
                prev_month_button.click()
            else:
                next_month_button = self.driver.find_element(By.CSS_SELECTOR, 'button.react-datepicker__navigation.react-datepicker__navigation--next')
                next_month_button.click()
            current_month = self.get_current_month()
        
        date_button = self.driver.find_element(By.CSS_SELECTOR,
            'div.react-datepicker__day.react-datepicker__day--%03d' \
            % int((target_date).strftime('%d')))
        date_button.click()
        


    def execute_search(self, search=None, start_date=None, end_date=None):
        """
        search: str
        start_date: datetime
        end_date: datetime
        """
        existing_start_date = datetime.strptime(self.driver \
            .find_element(By.XPATH, '//input[@id="dateStart"]') \
            .get_attribute('value'), '%m/%d/%Y')
            
        existing_end_date = datetime.strptime(self.driver \
            .find_element(By.XPATH, '//input[@id="dateEnd"]') \
            .get_attribute('value'), '%m/%d/%Y')

        if None not in (search, start_date, end_date):
            return
        
        if start_date == existing_start_date or end_date == existing_end_date:
            return

        if search:
            search_input = self.driver.find_element(By.ID, 'searchbtn')
            search_input.send_keys(search)

        if start_date:
            start_date_input = self.driver.find_element(By.XPATH, '//input[@id="dateStart"]')
            start_date_input.click()
            
            self.reach_target_date(start_date)

        if end_date:
            end_date_input = self.driver.find_element(By.XPATH, '//input[@id="dateEnd"]')
            end_date_input.click()

            self.reach_target_date(end_date)

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
