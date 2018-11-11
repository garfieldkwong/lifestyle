"""The dbs bank statement checker"""
import time
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common import action_chains, by
from selenium.webdriver.support import expected_conditions, wait
from . import base
LANDING_URL = 'https://internet-banking.hk.dbs.com/IB/Welcome?' \
              'pid=hk-personal-topnav-ib-login'


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

    def _landing(self):
        """Request landing page"""
        self._driver.get(LANDING_URL)

    def _login(self):
        """Login action"""
        print(self._driver.window_handles)
        username_input = self._driver.find_element_by_id('uname')
        username_input.send_keys(self._config['username'])
        password_input = self._driver.find_element_by_id('pwd')
        password_input.send_keys(self._config['password'])
        login_button = self._driver.find_element_by_name('logon')
        login_button.click()

    def _enter_card_detail(self):
        """Enter card detail"""
        time.sleep(2)
        elements = self._driver.find_elements_by_partial_link_text('')
        print(elements)
        for e in elements:
            print(e.text)


    def do_check(self):
        """The check logic"""
        self._landing()
        self._login()
        self._enter_card_detail()


