from collections import namedtuple
import sys
import signal
import time
import yaml
import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *

Color = namedtuple('color', 'BOLD SOLDOUT_BLUE EXIST_GREEN ENDC')
color = Color('\033[1m', '\033[94m', '\033[92m', '\033[0m')

# GET IT BY YOUR HANDS
class switch_cercatore(object):
    """ Switch 'Cercatore' """
    def __init__(self):
        # Load shop list from your '.shops.yaml.'
        self.shops_yaml = ".shops.yaml"
        with open(self.shops_yaml, 'r+') as stream:
            self.shops = yaml.load(stream)
            # if __debug__:
            #     print(self.shops)

        # specify a path to Chrome Canary App.
        self.path_to_chrome = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        self.browser = self._run_chrome_with_headless()

    def start_check(self):
        self.checkers = {'nintendo': self._nintendo_checker,
                         'amazon': self._amazon_checker,
                         'yodobashi_gray': self._yodobashi_checker,
                         'yodobashi_color': self._yodobashi_checker,
                         'yodobashi_splatoon': self._yodobashi_checker}
        result = dict()
        for shop, items in self.shops.items():
            checker = self.checkers[shop]
            result[shop] = checker(items)

        signal.signal(signal.SIGINT, self.Ctrl_C_handler)

        return result

    def end_check(self):
        self.browser.quit()

    def _run_chrome_with_headless(self):
        options = Options()
        # select Chrome Chanary
        options.binary_location = self.path_to_chrome
        # Enable headless mode
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        # Create Web Driver instance of Chrome
        browser = webdriver.Chrome(chrome_options=options)
        return browser

    def _run_chrome(self):
        options = Options()
        # select Chrome Chanary
        options.binary_location = self.path_to_chrome
        browser = webdriver.Chrome(chrome_options=options)
        return browser

    def _nintendo_checker(self, items):
        url = items['url']
        title = items['title']

        # Connect specific page.
        msg = color.BOLD + "Checker - Try connecting My Nintendo Store." + color.ENDC
        logging.info(msg)
        self.browser.get(url)
        if not title in self.browser.title:
            cnt = 0
            while True:
                cnt += 1
                msg = color.BOLD + \
                      "Checker - Try connecting My Nintendo Store. ({} times)" + \
                      color.ENDC
                logging.info(msg.format(cnt))
                # Retry connecting specific web page.
                self.browser.get(url)
                if title in self.browser.title:
                    cnt = 0
                    break
        msg = color.BOLD + "Checker - connected My Nintendo Store." + color.ENDC
        logging.info(msg)

        xpath = "//div[@id='HAC_S_KAYAA']/p[@class='stock']"
        element = self.browser.find_element_by_xpath(xpath)

        if element.text == "SOLD OUT":
            msg = color.SOLDOUT_BLUE + "Checker - Nintendo Switch is SOLD OUT." + color.ENDC
            logging.info(msg)
            return False
        else:
            logging.info(
                color.EXIST_GREEN + \
                "Checker - It is time to get Nintendo Switch!!" + \
                color.ENDC
            )
            return True

    def _amazon_checker(self, items):
        url = items['url']
        title = items['title']

        msg = color.BOLD + \
              "Checker - Try connecting Amazon's Nintendo Switch page." + \
              color.ENDC
        logging.info(msg)
        # Connect specific page.
        self.browser.get(url)
        if not title in self.browser.title:
            cnt = 0
            while True:
                cnt += 1
                msg = color.BOLD + \
                      "Checker - Try connecting Amazon's Nintendo Switch page. ({} times)" + \
                      color.ENDC
                logging.info(msg.format(cnt))
                # Retry connecting specific web page.
                self.browser.get(url)
                if title in self.browser.title:
                    cnt = 0
                    break
        msg = color.BOLD + "Checker - connected Amazon's Nintendo Switch page." + color.ENDC
        logging.info(msg)

        xpath = "//span[@id='priceblock_ourprice']"
        element = self.browser.find_element_by_xpath(xpath)
        str_price = element.text
        price = int(str_price.split(' ')[1].replace(',', ''))
        if price < 35000:
            msg = color.EXIST_GREEN + \
                  "Checker - It is time to get Nintendo Switch!!" + \
                  color.ENDC
            logging.info(msg)
            return True
        else:
            msg = color.SOLDOUT_BLUE + "Checker - This Switch is not proper." + color.ENDC
            logging.info(msg)
            return False

    def _yodobashi_checker(self, items):
        url = items['url']
        titles = items['title']
        is_soldout = True

        # Connect specific page.
        msg = color.BOLD + "Checker - Try Yodobashi's Nintendo Switch page." + color.ENDC
        logging.info(msg)
        self.browser.get(url)
        for title in titles:
            assert title in self.browser.title
            if not title in self.browser.title:
                cnt = 0
                while True:
                    cnt += 1
                    msg = color.BOLD + \
                          "Checker - Try Yodobashi's Nintendo Switch page." + \
                          color.ENDC
                    logging.info(msg)
                    self.browser.get(url)
                    if title in self.browser.title:
                        cnt = 0
                        break
        msg = color.BOLD + "Checker - Connected Yodobashi's Nintendo Switch page." + color.ENDC
        logging.info(msg)
        logging.info("Checker - Product name: {}".format(items['product']))

        xpath = "//div[@class='salesInfo']/p"
        if self._element_exist_by_xpath(xpath):
            msg = color.SOLDOUT_BLUE + "Checker - Nintendo Switch is SOLD OUT" + color.ENDC
            logging.info(msg)
            return False
        else:
            logging.info(
                    color.EXIST_GREEN + \
                    "Checker - It is time to get Nintendo Switch!!" + \
                    color.ENDC
            )
            return True
            """
            # Create visible browser instance.
            visible_browser = self._run_chrome()
            visible_browser.get(url)

            # Select how many items to buy
            select_xpath = "//select[@class='uiSlct']"
            dropdown = WebDriverWait(visible_browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, select_xpath))
            )
            dropdown = Select(dropdown)
            all_selected_options = dropdown.all_selected_options
            if not all_selected_options[0].text == 1:
                dropdown.select_by_visible_text('1')
            buyBtn_xpath = "//div[@class='buyBtn']"

            buyBtn = visible_browser.find_element_by_xpath(buyBtn_xpath)
            buyBtn.click()
            """

    def _element_exist_by_xpath(self, xpath):
        try:
            element = self.browser.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False

    def Ctrl_C_handler(self, signal, frame):
        self.end_check()
        sys.exit(0)
