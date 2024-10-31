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
        self.state_options = {
            'All': 'react-select-2-option-0',
            'DC': 'react-select-2-option-1',
            'District of Columbia': 'react-select-2-option-2',
            'Maryland': 'react-select-2-option-3',
            'Virginia': 'react-select-2-option-4',
        }
        self.county_options = {
            'All': 'react-select-3-option-0',
            'Anne Arundel': 'react-select-3-option-1',
            'Arlington': 'react-select-3-option-2',
            'Calvert': 'react-select-3-option-3',
            'Caroll': 'react-select-3-option-4',
            'Charles': 'react-select-3-option-5',
            'City of Alexandria': 'react-select-3-option-6',
            'City of Charlottesville': 'react-select-3-option-7',
            'City of Fredericksburg': 'react-select-3-option-8',
            'Clarke': 'react-select-3-option-9',
            'Culpeper': 'react-select-3-option-10',
            'District of Columbia': 'react-select-3-option-11',
            'Fairfax': 'react-select-3-option-12',
            'Fauquier': 'react-select-3-option-13',
            'Frederick': 'react-select-3-option-14',
            'Howard': 'react-select-3-option-15',
            'Loudoun': 'react-select-3-option-16',
            'Montgomery': 'react-select-3-option-17',
            'Orange': 'react-select-3-option-18',
            'Other': 'react-select-3-option-19',
            'Prince George\'s': 'react-select-3-option-20',
            'Prince William': 'react-select-3-option-21',
            'Rappahannock': 'react-select-3-option-22',
            'Richmond': 'react-select-3-option-23',
            'Spotsylvania': 'react-select-3-option-24',
            'Stafford': 'react-select-3-option-25',
            'Washington': 'react-select-3-option-26',
        }


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
        


    def execute_search(self, search=None, start_date=None, end_date=None, states=None, counties=None):
        """
        search: str
        start_date: datetime
        end_date: datetime
        states: list[str]
        """
        if None not in (search, start_date, end_date):
            return
        
        if search:
            search_input = self.driver.find_element(By.ID, 'searchbtn')
            search_input.send_keys(search)

        if start_date:
            self.set_start_date(start_date)

        if end_date:
            self.set_end_date(end_date)

        if states:
            self.set_states(states)

        if counties:
            self.set_counties(counties)

        search_button = self.driver.find_element(By.ID, 'search')
        search_button.click()
        
        WebDriverWait(self.driver, 30) \
            .until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]')))


    def set_start_date(self, start_date):
        """
        start_date: datetime
        """
        existing_start_date = datetime.strptime(self.driver \
            .find_element(By.XPATH, '//input[@id="dateStart"]') \
            .get_attribute('value'), '%m/%d/%Y')

        if start_date == existing_start_date:
            return

        start_date_input = self.driver.find_element(By.XPATH, '//input[@id="dateStart"]')
        start_date_input.click()
        
        self.reach_target_date(start_date)


    def set_end_date(self, end_date):
        """
        end_date: datetime
        """
        existing_end_date = datetime.strptime(self.driver \
            .find_element(By.XPATH, '//input[@id="dateEnd"]') \
            .get_attribute('value'), '%m/%d/%Y')

        if end_date == existing_end_date:
            return

        end_date_input = self.driver.find_element(By.XPATH, '//input[@id="dateEnd"]')
        end_date_input.click()
        
        self.reach_target_date(end_date)


    def set_states(self, states):
        """
        states: list[str]
        States can be found in state options
        """
        state_dropdown = self.driver.find_element(By.CSS_SELECTOR, 'div#state.css-2b097c-container')
        state_dropdown.click()

        for state in states:
            state_option = self.driver.find_element(By.CSS_SELECTOR, f'div#{self.state_options[state]}')
            state_option.click()

        state_dropdown.click()


    def set_counties(self, counties):
        """
        counties: list[str]
        """
        county_dropdown = self.driver.find_element(By.CSS_SELECTOR, 'div#county.css-2b097c-container')
        county_dropdown.click()

        for county in counties:
            county_option = self.driver.find_element(By.CSS_SELECTOR, f'div#{self.county_options[county]}')
            county_option.click()

        county_dropdown.click()


    def save_notices(self):
        notices = self.driver.find_elements(By.CLASS_NAME, 'public-notice-result')
        id_list = set()
        for notice in notices:
            id_list.add(notice.get_attribute('data-notice-id'))
        pprint(id_list)
        print(len(id_list))


    def close(self):
        self.driver.quit()
