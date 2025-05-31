import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from os import environ

CHROMEDRIVER = environ.get("chromedriver")

service = Service(executable_path=CHROMEDRIVER)
options = webdriver.ChromeOptions()
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/90.0.4430.93 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator,"
                      "'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 10)

driver.get("https://cookieclicker.gg/")

input("")

bigCookie = driver.find_element(By.ID, "bigCookie")

products = [driver.find_element(By.ID, f"product{i}") for i in range(20)]
upgrades_box = driver.find_element(By.ID, "upgrades")

while True:

    for product in products:
        if product.get_attribute("Class") == "product unlocked enabled":
            product.click()

    upgrades = upgrades_box.find_elements(By.XPATH, ".//*")
    for upgrade in upgrades:
        try:
            if upgrade.get_attribute("Class") == "crate upgrade enabled":
                upgrade.click()
                break
        except StaleElementReferenceException:
            break

    bigCookie.click()