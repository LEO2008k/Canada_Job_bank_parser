from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

# Запускаємо веб-драйвер
driver = webdriver.Chrome()

# Початкова сторінка зі списком посилань
initial_url = 'https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=Computer+technician&locationstring=Maple+ridge%2C+BC'

# Отримуємо сторінку зі списком посилань
driver.get(initial_url)

# Даємо трошки часу на завантаження (можете зменшити або збільшити затримку)
time.sleep(2)

# Знаходимо всі посилання на поточній сторінці
links = driver.find_elements(By.CSS_SELECTOR, 'a')

# Отримуємо посилання тільки на оголошення про роботу
job_links = [link.get_attribute('href') for link in links if link.get_attribute('href') and link.get_attribute('href').startswith('https://www.jobbank.gc.ca/jobsearch/jobposting/')]

# Проходимося по кожному оголошенню
for job_link in job_links:
    # Отримуємо сторінку оголошення
    driver.get(job_link)

    # Даємо трошки часу на завантаження (можете зменшити або збільшити затримку)
    time.sleep(5)

    # Отримуємо ім'я компанії
    try:
        # Знаходимо всі елементи з назвою компанії (strong або a)
        company_name_elements = driver.find_elements(By.XPATH, "//span[@property='hiringOrganization']//span[@property='name']//*[(self::strong or self::a)]")
        
        # Перевіряємо наявність елементів
        if company_name_elements:
            # Виводимо ім'я компанії
            company_name = company_name_elements[0].text.strip()
            print(f"Company Name: {company_name}")
    except:
        print("Company name not found.")

    # Знаходимо кнопку за ID
    apply_button = driver.find_element(By.ID, 'applynowbutton')

    # Клікаємо по кнопці
    apply_button.click()

    # Даємо трошки часу на завантаження (можете зменшити або збільшити затримку)
    time.sleep(2)

    # Отримуємо всі посилання на сторінці
    email_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'mailto')]")

    # Виводимо тільки рядки з електронними адресами
    for email_link in email_links:
        email_address_match = re.search(r'mailto:(.*?)(&|\?|$)', email_link.get_attribute('href'))
        if email_address_match:
            email_address = email_address_match.group(1)
            if email_address:
                print(f"Found Email Address: {email_address}")

    print("-----------------")
# Закриваємо веб-драйвер
driver.quit()

