import csv

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

class Scraper:
    def __init__(self, URL, initialize=True):
        """
        URL: str
        initialize: bool
        It is highly recommended to initialize by default, unless you have a very good reason to manually call _load_url()
        """
        self.driver_options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=self.driver_options)
        self.URL = URL
        self.STATE_OPTIONS = {
            'All': 'react-select-2-option-0',
            'DC': 'react-select-2-option-1',
            'District of Columbia': 'react-select-2-option-2',
            'Maryland': 'react-select-2-option-3',
            'Virginia': 'react-select-2-option-4',
        }
        self.COUNTY_OPTIONS = {
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
        self.NOTICE_TYPES = {
            
            'All': 'react-select-4-option-0',
            'Bids & Proposals': 'react-select-4-option-1',
            'City of Alexandria': 'react-select-4-option-2',
            'City of Charlottesville': 'react-select-4-option-3',
            'City of Fredericksburg': 'react-select-4-option-4',
            'Frederick County': 'react-select-4-option-5',
            'Legal Notices': 'react-select-4-option-6',
            'Notice of Hearing': 'react-select-4-option-7',
            'Official Notices': 'react-select-4-option-8',
            'Orange County': 'react-select-4-option-9',
            'Public Sale Notices': 'react-select-4-option-10',
            'Rappahannock County': 'react-select-4-option-11',
            'Special Notices': 'react-select-4-option-12',
            'Spotsylvania County': 'react-select-4-option-13',
            'Trustee Sales': 'react-select-4-option-14',
        }

        if initialize:
            self._load_url()


    def _get_current_month(self):
        current_month = self.driver.find_element(By.CSS_SELECTOR, 'div.react-datepicker__current-month') \
            .get_attribute('innerHTML')
        current_month = datetime.strptime(current_month, '%B %Y')
        return current_month 


    def _reach_target_date(self, target_date):
        """
        target_date: datetime 
        Requires the date picker to be opened beforehand
        """
        current_month = self._get_current_month()
        while target_date.strftime('%B %Y') != current_month.strftime('%B %Y'):
            if target_date < current_month:
                prev_month_button = self.driver.find_element(By.CSS_SELECTOR, 'button.react-datepicker__navigation.react-datepicker__navigation--previous')
                prev_month_button.click()
            else:
                next_month_button = self.driver.find_element(By.CSS_SELECTOR, 'button.react-datepicker__navigation.react-datepicker__navigation--next')
                next_month_button.click()
            current_month = self._get_current_month()
        
        date_button = self.driver.find_element(By.CSS_SELECTOR,
            'div.react-datepicker__day.react-datepicker__day--%03d' \
            % int((target_date).strftime('%d')))
        date_button.click()


    def _load_all_notices(self):
        WebDriverWait(self.driver, 30) \
            .until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[1]')))
        
        notice_number = int(self.driver \
            .find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[1]') \
            .get_attribute('innerHTML') \
            .split(' ')[1])

        if notice_number < 80:
            return

        iters_required = int(notice_number) // 80
        for _ in range(iters_required):
            load_more = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[3]/button')
            load_more.click()

            WebDriverWait(self.driver, 30) \
                .until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[3]/button')))


    def _load_url(self):
        self.driver.get(self.URL)
        WebDriverWait(self.driver, 30) \
            .until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[5]/div[3]/button')))


    def _set_start_date(self, start_date):
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
        
        self._reach_target_date(start_date)


    def _set_end_date(self, end_date):
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
        
        self._reach_target_date(end_date)


    def _set_states(self, states):
        """
        states: list[str]
        """
        state_dropdown = self.driver.find_element(By.CSS_SELECTOR, 'div#state.css-2b097c-container')
        state_dropdown.click()

        for state in states:
            state_option = self.driver.find_element(By.CSS_SELECTOR, f'div#{self.STATE_OPTIONS[state]}')
            state_option.click()

        state_dropdown.click()


    def _set_counties(self, counties):
        """
        counties: list[str]
        """
        county_dropdown = self.driver.find_element(By.CSS_SELECTOR, 'div#county.css-2b097c-container')
        county_dropdown.click()

        for county in counties:
            county_option = self.driver.find_element(By.CSS_SELECTOR, f'div#{self.COUNTY_OPTIONS[county]}')
            county_option.click()

        county_dropdown.click()

    def _set_notice_types(self, notice_types):
        """
        notice_types: list[str]
        """
        notice_type_dropdown = self.driver.find_element(By.CSS_SELECTOR, 'div#noticetype.css-2b097c-container')
        notice_type_dropdown.click()

        for notice_type in notice_types:
            notice_type_option = self.driver.find_element(By.CSS_SELECTOR, f'div#{self.NOTICE_TYPES[notice_type]}')
            notice_type_option.click()

        notice_type_dropdown.click()


    def search(self, search_phrase=None, start_date=None, end_date=None, states=None, counties=None, notice_types=None):
        """
        search: str
        start_date: datetime
        end_date: datetime
        states: list[str]
        counties: list[str]
        notice_types: list[str]
        """
        if search_phrase:
            search_input = self.driver.find_element(By.ID, 'searchbtn')
            search_input.send_keys(search_phrase)

        if start_date:
            self._set_start_date(start_date)

        if end_date:
            self._set_end_date(end_date)

        if states:
            self._set_states(states)

        if counties:
            self._set_counties(counties)

        if notice_types:
            self._set_notice_types(notice_types)

        search_button = self.driver.find_element(By.ID, 'search')
        search_button.click()
        
        WebDriverWait(self.driver, 30) \
            .until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]')))


    def save_all_notices(self, filename, format='csv'):
        """
        filename: str
        format: str
        format can be 'csv'
        """
        self._load_all_notices()
        with open(f'{filename}.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Data', 'Location', 'Type', 'Text'])

        scraped_id = []
        notices = self.driver.find_elements(By.CSS_SELECTOR, 'div.public-notice-result')
        for notice in notices:
            notice_id = notice.get_attribute('data-notice-id')
            if notice_id in scraped_id:
                continue

            dl_driver = webdriver.Firefox(options=self.driver_options)
            dl_driver.get(f'{self.URL}?activeNotice={notice_id}')

            WebDriverWait(dl_driver, 30) \
                .until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'header')))
            
            header = dl_driver.find_element(By.CSS_SELECTOR, 'header')
            notice_date = datetime.strptime(' '.join(header.find_element(By.CSS_SELECTOR, 'p') \
                .get_attribute('innerHTML') \
                .split(' ')[-3:]), '%B %d, %Y')
            notice_type = header.find_element(By.CSS_SELECTOR, 'h2').get_attribute('innerHTML')
            location = header.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div[2]') \
                .get_attribute('innerHTML')
            
            dd_list = dl_driver.find_element(By.CSS_SELECTOR, 'dd')
            paragraphs = dd_list.find_elements(By.CSS_SELECTOR, 'p')
            text = '\n'.join([p.text for p in paragraphs])

            dl_driver.quit()

            with open(f'{filename}.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([notice_id, notice_date.strftime('%Y-%m-%d'), location, notice_type, text])

            scraped_id.append(notice_id)

    def close(self):
        self.driver.quit()
