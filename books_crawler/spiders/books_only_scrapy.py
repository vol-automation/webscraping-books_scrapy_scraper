import os
import glob
import re
import csv
import mysql.connector
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from books_crawler.items import BooksCrawlerItem

def product_info(response, value):
    return response.xpath('//th[text()="{0}"]/following-sibling::*[1]/text()'.format(value)).extract_first()

class BooksOnlyScrapySpider(Spider):
    name = 'books_only_scrapy'
    allowed_domains = ['books.toscrape.com']
    HOME_PAGE = 'http://books.toscrape.com'
    
    def __init__(self, category=HOME_PAGE):
        # delete previous exported csv
        if os.path.isfile(get_csv_filename(category)):
            os.remove(get_csv_filename(category))

        self.start_urls = [category]
        self.category = category

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # - Process next page
        # next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()    
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield Request(absolute_next_page_url)

    def parse_book(self, response):
        l = ItemLoader(item=BooksCrawlerItem(), response=response)
        title = response.xpath('//article[@class="product_page"]//h1/text()').extract_first()
        l.add_value('title', title) 
        price = response.xpath('//p[@class="price_color"]/text()').extract_first()
        l.add_value('price', price)
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()          
        l.add_value('description', description)

        image_urls = response.xpath('//img/@src').extract_first()
        image_urls = image_urls.replace('../..', 'http://books.toscrape.com')
        l.add_value('image_urls', image_urls)

        rating = response.xpath('//*[contains(@class,"star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ','')
        l.add_value('rating', rating)
        
        upc = product_info(response,'UPC')
        l.add_value('upc', upc)
        product_type = product_info(response,'Product Type')
        l.add_value('product_type', product_type)
        price_without_tax = product_info(response,'Price (excl. tax)')
        l.add_value('price_without_tax', price_without_tax)
        price_with_tax = product_info(response,'Price (incl. tax)')
        l.add_value('price_with_tax', price_with_tax)
        tax = product_info(response,'Tax')
        l.add_value('tax', tax)
        availability = product_info(response,'Availability')
        l.add_value('availability', availability)
        number_of_reviews = product_info(response,'Number of reviews')
        l.add_value('number_of_reviews', number_of_reviews)
        
        # yield {
        #     'title'             : title,
        #     'price'             : price,
        #     'description'       : description,
        #     'image_url'         : image_url,
        #     'rating'            : rating,
        #     'upc'               : upc,           
        #     'product_type'      : product_type,
        #     'price_without_tax' : price_without_tax,
        #     'price_with_tax'    : price_with_tax,   
        #     'tax'               : tax,
        #     'availability'      : availability, 
        #     'number_of_reviews' : number_of_reviews            
        # }
        return l.load_item()
        
    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file, get_csv_filename(self.category))
        
def get_csv_filename(category):
    category_name = ''
    cat_regex_result = re.compile("\/books\/(.+)_\d+\/").search(category)
    if cat_regex_result is not None:
        category_name = cat_regex_result.group(1)

    csv_name = 'books.csv'
    if category_name != '':
        csv_name = 'books-{0}.csv'.format(category_name)   
    return csv_name