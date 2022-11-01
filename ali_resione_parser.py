from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
# import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

SEARCH_REQUEST = 'Resione m68'


options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(1)


def input_search_request(search_request:str):
    global browser
    browser.get("https://www.aliexpress.ru")
    search_input = browser.find_element(By.ID, "searchInput")  
    search_input.send_keys(search_request) 
    search_input.send_keys(Keys.ENTER)   
    browser.implicitly_wait(1)

def sort_elements_by_price(elements_list):
    price_list_sorted = []
    elements_list_sorted = []
    for element in elements_list:
        price_list_sorted.append(element.text)
    price_list_sorted.sort()
    for price in price_list_sorted:
        for element in elements_list:
            if price == element.text:
                elements_list_sorted.append(element)
                break
    return elements_list_sorted

def find_product_on_item_page(*args):
    global browser
    product_title = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[8]/div[2]/div/div/div[1]/div/div[1]/div[1]/div/span[2]')
    product_price = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[8]/div[2]/div/div/div[3]/div[1]/div/div[2]/div[2]')
    product_options = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[8]/div[2]/div/div/div[1]/div/div[1]/div[2]/div')
    product_options_list = product_options.find_elements(By.TAG_NAME, 'div')
    assert(product_options_list, f'No product options')
    weight_in_kg = args[1] / 1000
    product_option_index = 1
    while product_option_index < len(product_options_list):
        if (str(args[1]) or str(weight_in_kg)) in product_title.text and args[0] in product_title.text:
            product_data = {'title' : product_title.text, 'price' : product_price.text, 'url' : browser.current_url}
            return product_data
        else:
            product_options_list[product_option_index].click()
            product_title = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[8]/div[2]/div/div/div[1]/div/div[1]/div[1]/div/span[2]')
            product_price = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[8]/div[2]/div/div/div[3]/div[1]/div/div[2]/div[2]')         
            product_option_index += 1
    return None

def search_product_by_attributes(product_type='M68', product_weight_in_gramms=1000):
    global browser
    input_search_request(SEARCH_REQUEST)
    first_element_price = browser.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[2]/div[2]/div[2]/div/div/div[1]/div/div/a/div[3]/div[2]/div[1]')
    searched_elements_list = browser.find_elements(By.CLASS_NAME, first_element_price.get_attribute('class'))
    products_list = sort_elements_by_price(searched_elements_list)
    window_index = 1
    for product in products_list:
        product.click()
        browser.implicitly_wait(1)     
        browser.switch_to.window(browser.window_handles[window_index])
        product = find_product_on_item_page(product_type, product_weight_in_gramms)
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