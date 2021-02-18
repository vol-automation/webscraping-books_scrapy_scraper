from time import sleep
from scrapy import Spider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from scrapy.selector import Selector
from scrapy.http import Request

class BooksSeleniumSpider(Spider):
    name = 'books_selenium'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome(os.path.join(os.getcwd(),'chromedriver.exe'))
        self.driver.get('http://books.toscrape.com')
        
        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()
        for book in books:
            url = 'http://books.toscrape.com/catalogue/' + book
            yield Request(url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds.')
                next_page.click() 

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)

            except Exception as err:
                self.logger.critical(err)
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break

    def parse_book(self, response):
        title = response.xpath('//article[@class="product_page"]//h1/text()').extract_first()
        price = response.xpath('//p[@class="price_color"]/text()').extract_first()
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()          

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com')

        rating = response.xpath('//*[contains(@class,"star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ','')
        
        upc = product_info(response,'UPC')
        product_type = product_info(response,'Product Type')
        price_without_tax = product_info(response,'Price (excl. tax)')
        price_with_tax = product_info(response,'Price (incl. tax)')
        tax = product_info(response,'Tax')
        availability = product_info(response,'Availability')
        number_of_reviews = product_info(response,'Number of reviews')
        
        yield {
            'title'             : title,
            'price'             : price,
            'description'       : description,
            'image_url'         : image_url,
            'rating'            : rating,
            'upc'               : upc,           
            'product_type'      : product_type,
            'price_without_tax' : price_without_tax,
            'price_with_tax'    : price_with_tax,   
            'tax'               : tax,
            'availability'      : availability, 
            'number_of_reviews' : number_of_reviews            
        }    
    
def product_info(response, value):
    return response.xpath('//th[text()="{0}"]/following-sibling::*[1]/text()'.format(value)).extract_first()
    