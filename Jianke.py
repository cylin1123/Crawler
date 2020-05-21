import requests
import chardet
from bs4 import BeautifulSoup
import time

import urllib.request
from selenium import webdriver
from selenium.webdriver.support import ui as UI
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as BY

options = webdriver.ChromeOptions()
browser = webdriver.Chrome()
browser.get('https://www.jianke.com/product/28.html')
browser.find_element_by_id('b_4').click()

time.sleep(15)
content = browser.find_element_by_class_name('con_det')

print(content.text.encode('utf8'))



browser.quit()