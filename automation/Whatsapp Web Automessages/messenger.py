from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from time import sleep
import os

# --- Configuration ---

CHROMIUM_USER_DATA_DIR = os.path.expanduser("~/.config/chromium")
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={CHROMIUM_USER_DATA_DIR}")

# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
chrome_options.add_argument(f"user-agent={custom_user_agent}")

def send_message(contact_name, message):
    """Opens and uses data from default Chromium user and assumes there is an already open Whatsapp Web session.
    contact_name must be exact"""

    try:
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"Selenium is attempting to use user data from: {CHROMIUM_USER_DATA_DIR}")

        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": custom_user_agent})

        driver.get("https://web.whatsapp.com/")
        sleep(5)
        text_box = driver.find_element(
            By.CLASS_NAME,
            "selectable-text"
        )
        text_box.click()
        text_box.send_keys(contact_name)

        driver.find_element(By.XPATH, f'//*[@role="gridcell"]').click()

        chat_box = driver.find_element(By.XPATH, '//*[@aria-label="Type a message"]')

        chat_box.click()
        chat_box.send_keys(message)

        driver.find_element(By.XPATH, '//*[@aria-label="Send"]').click()

        sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:

        if 'driver' in locals() and driver:
            driver.quit()
