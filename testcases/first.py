from prompt_toolkit.keys import Key
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
import os
import time
import unittest
import keyboard

class FirstTest(unittest.TestCase):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    dir_path=os.path.dirname(os.path.realpath(__file__))
    chromedriver=dir_path+"../../resources/chromedriver"
    os.environ["webdriver.chrome.driver"]=chromedriver
    driver=webdriver.Chrome(chrome_options=options, executable_path=chromedriver)

    def setUp(self):
        driver=self.driver
        driver.get("https://www.google.com/flights")
        WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_xpath("//*[@aria-label='Main menu']"))
        driver.maximize_window()
        driver.set_page_load_timeout(20)

    def test_FlightSearch(self):
        driver=self.driver
        assert "Flights" in driver.title
        fromSearch="//div[@data-flt-ve='origin_airport']/div[3]"
        fromSearchInput="//input[@placeholder='Where from?']"
        toSearch="//div[@data-flt-ve='destination_airport']/div[3]"
        toSearchInput="//input[@placeholder='Where to?']"
        searchBtn="//floating-action-button[@data-flt-ve='search_button']"
        tripSummaryHdr="//ol[@aria-label='Trip summary']"
        flightSearchResultList="//ol[@class='gws-flights-results__result-list']/li"

        fromSearchElement=WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(fromSearch))
        toSearchElement=WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(toSearch))
        searchBtnElement=WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(searchBtn))

        fromSearchElement.click()
        fromSearchInputElement=WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(fromSearchInput))
        fromSearchInputElement.clear()
        time.sleep(1)
        fromSearchInputElement.send_keys("ORD")
        keyboard.press_and_release('enter')
        time.sleep(1)
        toSearchElement.click()
        toSearchInputElement=WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(toSearchInput))
        toSearchInputElement.clear()
        time.sleep(1)
        toSearchInputElement.send_keys("BOM")
        keyboard.press_and_release('enter')
        time.sleep(1)
        searchBtnElement.click()
        tripSummaryHdrElement=WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_xpath(tripSummaryHdr))
        assert len(tripSummaryHdrElement) >= 1
        time.sleep(1)
        assert len(driver.find_elements_by_xpath(flightSearchResultList)) >= 1
        #time.sleep(5)

    def tearDown(self):
        self.driver.quit()

if __name__=='__main__':
    unittest.main()