from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

SEARCH_REQUEST = 'Resione m68'

def init_browser():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(1)
    return browser

def input_search_request(search_request:str, browser:webdriver):
    browser.get("https://www.aliexpress.ru")
    search_input = browser.find_element(By.ID, "searchInput")  
    search_input.send_keys(search_request) 
    search_input.send_keys(Keys.ENTER)   

def sort_elements_by_price(elements_list):
    price_list_sorted = []
    elements_list_sorted = []
    for element in elements_list:
        price_list_sorted.append(element.get_attribute("innerHTML"))
    price_list_sorted.sort()
    for price in price_list_sorted:
        for element in elements_list:
            if price == element.get_attribute("innerHTML"):
                elements_list_sorted.append(element)
                break
    return elements_list_sorted

def find_product_on_item_page(browser:webdriver, product_type, product_weight_in_gramms):
    product_title = browser.find_element(By.XPATH, '//*[@id="__aer_root__"]/div/div[7]/div[2]/div/div/div[1]/div/div[1]/div[1]/div/span[2]')
    product_price = browser.find_element(By.XPATH, '//*[@id="__aer_root__"]/div/div[7]/div[2]/div/div/div[3]/div[1]/div/div[2]/div[2]')
    products = browser.find_element(By.XPATH, '//*[@id="__aer_root__"]/div/div[7]/div[2]/div/div/div[1]/div/div[1]/div[2]/div')
    products_list = products.find_elements(By.TAG_NAME, 'div')
    weight_in_kg = product_weight_in_gramms / 1000
    product_index = 1
    while product_index < len(products_list):
        product_title_text = product_title.get_attribute("innerHTML")
        if (str(product_weight_in_gramms) or str(weight_in_kg)) in product_title_text and product_type in product_title_text:
            product_data = {'title' : product_title_text, 'price' : product_price.get_attribute('innerHTML').replace('&nbsp;', ''), 'url' : browser.current_url}
            return product_data
        else:
            products_list[product_index].click()
            product_title = browser.find_element(By.XPATH, '//*[@id="__aer_root__"]/div/div[7]/div[2]/div/div/div[1]/div/div[1]/div[1]/div/span[2]')
            product_index += 1
    return None

def search_product_by_attributes(product_type='M68', product_weight_in_gramms=1000):
    browser = init_browser()
    input_search_request(SEARCH_REQUEST, browser)
    searched_elements_list = browser.find_elements(By.CLASS_NAME, 'snow-price_SnowPrice__mainM__ugww0l')
    products_list = sort_elements_by_price(searched_elements_list)
    window_index = 1
    for product in products_list:
        browser.implicitly_wait(1)     
        product.click()
        browser.switch_to.window(browser.window_handles[window_index])
        product = find_product_on_item_page(browser, product_type=product_type, product_weight_in_gramms=product_weight_in_gramms)
        if product:
            browser.quit()             
            return product
        else:
            window_index += 1
            browser.switch_to.window(browser.window_handles[0])
    else:
        browser.quit()             
        return 'There is no products with such attributes'

if __name__ == '__main__':
    resione = search_product_by_attributes()
    print(resione)