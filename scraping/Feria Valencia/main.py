import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from os import environ

DATA_FILE = "demo_data.csv"
company_inf = []


WEBSITE = "https://apps.feriavalencia.com/catalog/iberflora/exhibitors"
CHROMEDRIVER = environ.get("chromedriver")
service = Service(executable_path=CHROMEDRIVER)
options = webdriver.ChromeOptions()
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/90.0.4430.93 Safari/537.36")

driver = webdriver.Chrome(
    service=service,
    options=options,
)

driver.implicitly_wait(3)

driver.get(WEBSITE)

sleep(10)

page = 1

while page <= 10:

    page = int(driver.find_element(
        By.CLASS_NAME,
        "v-select__selections",
    ).find_element(
        By.CSS_SELECTOR,
        "div"
    ).text)

    print(f"Page: {page}")

    table_elements = driver.find_element(
        By.CLASS_NAME,
        "exhibitors-catalog__container"
    ).find_elements(
        By.CSS_SELECTOR,
        "tbody tr"
    )

    page_element = 0
    for element in table_elements:
        page_element += 1
        print(f"Page element: {page_element}")

        children = element.find_elements(
            By.XPATH,
            "./*"
        )

        link = children[1].find_element(
            By.CSS_SELECTOR,
            "a"
        ).get_attribute("href")

        name = children[1].find_element(
            By.CLASS_NAME,
            "exhibitors-catalog__body-row-name-text"
        ).text

        try:
            sector = children[2].find_element(
                By.CSS_SELECTOR,
                "span"
            ).text
        except NoSuchElementException:

            sector = ""

        country = children[3].find_element(
            By.CSS_SELECTOR,
            "span"
        ).text

        driver.execute_script("window.open(arguments[0], '_blank');", link)
        driver.switch_to.window(driver.window_handles[1])

        sleep(3)

        try:
            phone = driver.find_element(
                By.CLASS_NAME,
                "exhibitor-details-info__telefon-description"
            ).text
        except NoSuchElementException:
            phone = "empty"

        try:
            email = driver.find_element(
                By.CSS_SELECTOR,
                "p.exhibitor-details-info__contact-link a"
            ).text
        except NoSuchElementException:
            email = "empty"

        try:
            website = driver.find_element(
                By.CSS_SELECTOR,
                "p.exhibitor-details-info__expositor-link a"
            ).text
        except NoSuchElementException:
            website = "empty"

        try:
            contact_person = driver.find_element(
                By.CLASS_NAME,
                "exhibitor-details-info__contact-description"
            ).text
        except NoSuchElementException:
            contact_person = "empty"

        try:
            address_bits = driver.find_elements(
                By.CLASS_NAME,
                "exhibitor-details-info__direction-description"
            )
        except NoSuchElementException:
            address_bits = "empty"

        final_address = ""
        if final_address != "empty":
            for address_bit in address_bits:

                final_address += address_bit.text + " "

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        inf = {
            "name": name,
            "sector": sector,
            "country": country,
            "email": email,
            "phone": phone,
            "website": website,
            "contact person": contact_person,
            "address": final_address,
            "link": link
        }

        company_inf.append(inf)

    page += 1
    driver.find_element(
        By.CLASS_NAME,
        "far.fa-arrow-right",
    ).click()


data = "local_data.csv"

with open(data, "w", newline="", encoding="utf-8") as write_file:

    writer = csv.DictWriter(write_file, fieldnames=company_inf[0].keys())
    writer.writeheader()
    writer.writerows(company_inf)