from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
from logconfig import logger
import chromedriver_binary # need for debug
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlitemanager as sqlm

SEARCH_REQUEST = 'Resione m68'
TIMEZONE = datetime.timezone(datetime.timedelta(hours=3))

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')

class Resin:

    def __init__(self, name:str, search_request:str, product_type:str, amount:int):
        self.name = name
        self.search_request = search_request
        self.product_type = product_type
        self.amount = amount

        try:
            self.browser = webdriver.Chrome(options=options)
            self.browser.implicitly_wait(1)
        except Exception as e:
            logger.error(f'Browser init error: {e}')
            raise
        logger.info('Browser init done!')
        self.get_product_data()
        self.date = self.product_data["date"]
        self.price = self.product_data["price"]
        self.url = self.product_data["url"]
        self.coupon = self.product_data["coupon"]
        if type(self.coupon) is dict:
            self.coupon = f'Купон на: {self.coupon["discount"]} \
                               \n{self.coupon["info"]} \
                               \nСрок купона: {self.coupon["coupon_timer"]}'

    def __str__(self) -> str:
        if type(self.product_data) is dict:
            return f'Смола {self.name}\n{self.product_type}-{self.amount}g \
                    \nЦена: {self.price}\nДанные от {self.date}\n{self.url}\n\n{self.coupon}'
        else:
            return self.product_data


    def input_search_request(self):
        self.browser.get("https://www.aliexpress.ru")
        search_input = self.browser.find_element(By.ID, "searchInput")  
        search_input.send_keys(self.search_request) 
        search_input.send_keys(Keys.ENTER)   
        self.browser.implicitly_wait(1)


    def sort_elements_by_price(self, elements_list):
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


    def find_element_by_xpath(self, xpath:str, web_element:webdriver = None):
        try:
            if web_element:
                element = web_element.find_element(By.XPATH, xpath)
            else:
                element = self.browser.find_element(By.XPATH, xpath)
        except Exception as e:
            logger.error(f'xpath error: {xpath}')
            raise
        return element


    def parse_coupon_data(self, id:str):
        try:
            coupon_block = self.browser.find_element(By.ID, id)
        except Exception as e:
            coupon_block = None
            logger.warning(f'Coupon error: {e}')
        if coupon_block :
            coupon_list = coupon_block.find_elements(By.XPATH, './*')
            if len(coupon_list) > 1:
                coupone_data = f'Проверьте купоны и скидки на: {self.browser.current_url}'
            else:
                coupon_discount = self.find_element_by_xpath('.//div/div/div/div[2]/div/div/div[1]/span', coupon_block)
                coupon_info = self.find_element_by_xpath('.//div/div/div/div[2]/div/div/div[2]/span', coupon_block)
                coupon_timer = self.find_element_by_xpath('.//div/div/div/div[2]/div/div/div[1]/div/span', coupon_block)
                coupone_data = {'discount':coupon_discount.text,
                                'info':coupon_info.text,
                                'coupon_timer':coupon_timer.text}
        else:
            coupone_data = 'Нет купонов для данного товара'
        return coupone_data


    def find_product_on_item_page(self, *args):
        product_title = self.find_element_by_xpath('/html/body/div[1]/div/div[7]/div[2]/div/div/div[1]/div/div[1]/div[1]/div/span[2]')
        product_price = self.find_element_by_xpath('/html/body/div[1]/div/div[7]/div[2]/div/div/div[3]/div[1]/div/div[2]/div[2]')
        product_options = self.find_element_by_xpath('/html/body/div[1]/div/div[7]/div[2]/div/div/div[1]/div/div[1]/div[2]/div')
        product_options_list = product_options.find_elements(By.TAG_NAME, 'div')
        assert(product_options_list, 'No product options')
        weight_in_kg = self.amount / 1000
        product_option_index = 1
        while product_option_index < len(product_options_list):
            if (str(self.amount) or str(weight_in_kg)) in product_title.text and self.product_type in product_title.text:             
                coupon_data = self.parse_coupon_data('coupon_anchor')
                current_date = datetime.datetime.now(TIMEZONE).date().strftime('%d.%m.%Y')
                product_data = {'title' : product_title.text, 
                                'price' : product_price.text, 
                                'url' : self.browser.current_url,
                                'date': current_date,
                                'coupon' : coupon_data}
                return product_data
            else:
                product_options_list[product_option_index].click()
                product_title = self.find_element_by_xpath('/html/body/div[1]/div/div[7]/div[2]/div/div/div[1]/div/div[1]/div[1]/div/span[2]')
                product_price = self.find_element_by_xpath('/html/body/div[1]/div/div[7]/div[2]/div/div/div[3]/div[1]/div/div[2]/div[2]')         
                product_option_index += 1
        return None


    def insert_product_data_in_db(self, table_name:str):
        collums = ('name', 'product_model', 'price', 'date', 'url', 'coupon')
        row = (self.name, 
               f'{self.product_type}-{self.amount}',
               self.price,
               self.date,
               self.url,
               self.coupon)
        sqlm.open_connection()
        sqlm.create_table(table_name, collums)
        sqlm.insert_data(table_name, [row]) 
        sqlm.close_connection()


    def get_product_data(self):
        self.input_search_request()
        first_element_price = self.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div[2]/div[2]/div/div/div[1]/div/div/a/div[3]/div[2]/div[1]')
        searched_elements_list = self.browser.find_elements(By.CLASS_NAME, first_element_price.get_attribute('class'))
        products_list = self.sort_elements_by_price(searched_elements_list)
        window_index = 1
        for product in products_list:
            product.click()
            self.browser.implicitly_wait(1)     
            self.browser.switch_to.window(self.browser.window_handles[window_index])
            product = self.find_product_on_item_page()
            if product:
                self.product_data = product
                self.browser.quit()
                return             
            else:
                window_index += 1
                self.browser.switch_to.window(self.browser.window_handles[0])
        else:
            self.browser.quit()             
            self.product_data = 'There is no products with such attributes'


if __name__ == '__main__':
    # resione = Resin('Resione', SEARCH_REQUEST, 'M68', 1000)
    # print(resione)
    # resione.insert_product_data_in_db('resione')
    sqlm.select_data(f'SELECT * FROM resione DESC LIMIT 1')
    # if type(resione) is dict:
    #     insert_product_data_in_db('resione', resione)