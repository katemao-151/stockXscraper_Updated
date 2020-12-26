import time
import requests
import random
import json

from urllib3.exceptions import MaxRetryError
from selenium import webdriver      
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


for i in range(500):

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.worldbeachguide.com/top-100-beaches-earth.htm")
    driver.quit()
