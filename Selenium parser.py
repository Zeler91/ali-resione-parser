from selenium import webdriver
import chromedriver_binary
import time
import re  # Regular Expressions = Регулярные выражения

from selenium.webdriver.common.by import By

browser = webdriver.Chrome()   # Запускаем браузер
browser.get("http://hh.ru")    # Открываем hh.ru

search_input = browser.find_element(By.ID, "a11y-search-input")  # Находим поле поискового запроса
search_input.send_keys("Junior Python")  # Вводим текст


search_button = browser.find_element(By.CSS_SELECTOR, '[data-qa="search-button"]') # Находим кнопку
search_button.click()  # Кликаем


job_count = browser.find_element(By.CSS_SELECTOR, '[data-qa="vacancies-search-header"] h1')  # Заголовок с кол-вом вакансий

# re.sub - сделать замену
# \D символы, не являющиеся цифрой
# Удаляем \D из строки:
count = re.sub(r"\D", "", job_count.text)
print(f"Found exactly {count} jobs")


browser.close()                # Закрываем браузер





# head_hunter.py

# from selenium import webdriver
# import chromedriver_binary
# from selenium.webdriver.common.by import By
# import re


# def parse_hh(job_title):
#     browser = webdriver.Chrome()  # Запускаем браузер
#     browser.get("http://hh.ru")  # Открываем hh.ru

#     search_input = browser.find_element(By.ID, "a11y-search-input")  # Находим поле поискового запроса
#     search_input.send_keys(job_title)  # Вводим текст

#     search_button = browser.find_element(By.CSS_SELECTOR, '[data-qa="search-button"]')  # Находим кнопку
#     search_button.click()  # Кликаем

#     job_count = browser.find_element(By.CSS_SELECTOR,
#                                      '[data-qa="vacancies-search-header"] h1')  # Заголовок с кол-вом вакансий

#     # Regular Expressions = Регулярные выражения
#     # re.sub - сделать замену
#     # \D символы, не являющиеся цифрой
#     # Удаляем \D из строки:
#     count = re.sub(r"\D", "", job_count.text)

#     browser.close()  # Закрываем браузер
#     return count