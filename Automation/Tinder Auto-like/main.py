from random import random, randint
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException, \
    ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from os import environ

def random_response_time():
    """Imitates hesitation from user before licking"""

    upper_bound = 6
    lower_bound = 3

    response_multiplier = random()
    sec = randint(lower_bound, upper_bound)

    final_sec = response_multiplier * sec
    sleep(final_sec)

CHROMEDRIVER = environ.get("chromedriver")
USER_NUMBER = environ.get("user_number")

service = Service(executable_path=CHROMEDRIVER)
options = webdriver.ChromeOptions()
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/90.0.4430.93 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator,"
                      "'webdriver', {get: () => undefined})")

driver.implicitly_wait(10)

driver.get("https://tinder.com")

random_response_time()
driver.find_element(
    By.XPATH,
    "//*[text()='I decline']"
).click()

random_response_time()

# Click login button
driver.find_element(
    By.XPATH,
    "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]/div",
).click()

random_response_time()
# Click loging with phone number
driver.find_element(
    By.XPATH,
    "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/span/div[3]/button/div[2]/div[2]",
).click()

random_response_time()

# Type phone number
driver.find_element(
    By.ID,
    "phone_number"
).send_keys(USER_NUMBER)

random_response_time()

# Hit next
driver.find_element(
    By.XPATH,
    "/html/body/div[2]/div/div/div[1]/div/div[3]/button/div[2]/div[2]/div"
).click()

input("Clear the verification and once inside hit enter\n")

# Accept location access 
driver.find_element(
    By.XPATH,
    "//*[text()='Allow']"
).click()

random_response_time()

# Reject notifications
driver.find_element(
    By.XPATH,
    "//*[text()='I’ll miss out']"
).click()

    # click like
random_response_time()

for i in range(100):
    random_response_time()
    try:
        try:
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[5]/div/div[4]/button"
            ).click()
        except NoSuchElementException:
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[4]/div/div[4]/button"
            ).click()
    except ElementClickInterceptedException:

        try:
            driver.find_element(
                By.XPATH,
                "//*[text()='Not interested']"
            ).click()

        except NoSuchElementException:
            driver.find_element(
                By.CLASS_NAME,
                "Z(1).StretchedBox.CenterAlign"
            )
            input("Some annoying element")




