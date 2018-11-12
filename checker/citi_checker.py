"""The dbs bank statement checker"""
import datetime
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common import action_chains, by
from selenium.webdriver.support import expected_conditions, wait
from . import base
LANDING_URL = 'https://www.citibank.com.hk/HKGCB/JSO/signon/DisplayUsernameSignon.do'


class Checker(base.Checker):
    """DBS statement checker"""
    def __init__(self, creds_filename, config):
        """Init"""
        super().__init__(creds_filename)
        self._config = config
        chrome_options = options.Options()
        # chrome_options.add_argument("--headless")
        self._driver = webdriver.Chrome(chrome_options=chrome_options)
        self._driver.maximize_window()
        self._date = None
        self._balance = None

    def _landing(self):
        """Request landing page"""
        self._driver.get(LANDING_URL)

    def _login(self):
        """Login action"""
        username_input = self._driver.find_element_by_id('username')
        username_input.send_keys(self._config['username'])
        password_input = self._driver.find_element_by_id('password')
        password_input.send_keys(self._config['password'])
        login_buttons = self._driver.find_elements_by_class_name('ui-button-text')
        login_btn = None
        for element in login_buttons:
            if element.text == 'SIGN ON':
                login_btn = element
                break
        login_btn.click()

    def _enter_card_detail(self):
        """Enter card detail"""
        element = wait.WebDriverWait(self._driver, 10).until(
            expected_conditions.presence_of_all_elements_located(
                (by.By.ID, 'cmlink_AccountNameLink')
            )
        )
        element[0].click()

    def _get_target(self):
        """Get target"""
        element = wait.WebDriverWait(self._driver, 10).until(
            expected_conditions.presence_of_element_located(
                (by.By.ID, 'rightLabelValueContainer')
            )
        )
        children = element.find_elements_by_tag_name('div')
        balance = None
        date = None
        for child in children:
            item_children = child.find_elements_by_tag_name('div')
            found_balance = False
            found_date = False
            for item in item_children:
                if not found_balance and item.text == 'Last Statement Balance:':
                    found_balance = True
                elif found_balance:
                    balance = item.text
                elif not found_date and item.text == 'Payment Due Date:':
                    found_date = True
                elif found_date:
                    date = item.text
                elif found_date and found_balance:
                    break
        self._balance = 'citi: ' + balance
        splitted_date = date.split('/')
        self._date = datetime.datetime(int(splitted_date[2]), int(splitted_date[0]), int(splitted_date[1]))

    def _logout(self):
        """Log out"""
        logout_btn = self._driver.find_element_by_id('PortalHeaderMenuRight')
        logout_btn.click()

    def get_date(self):
        """Retrieve the date"""
        return self._date

    def get_summary(self):
        """Retrieve the summary"""
        return self._balance

    def do_check(self):
        """The check logic"""
        self._landing()
        self._login()
        self._enter_card_detail()
        self._get_target()
        self._logout()
