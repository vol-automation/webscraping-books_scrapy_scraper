import os
import glob
import re
import csv
import mysql.connector
from scrapy import Spider
from scrapy.http import Request

def product_info(response, value):
    return response.xpath('//th[text()="{0}"]/following-sibling::*[1]/text()'.format(value)).extract_first()

class BooksOnlyScrapySpider(Spider):
    name = 'books_mysql'
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
        title = response.xpath('//article[@class="product_page"]//h1/text()').extract_first()
        price = response.xpath('//p[@class="price_color"]/text()').extract_first()
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()          
        
        yield {
            'title'             : title,
            'price'             : price,
            'description'       : description,           
        }
        
    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file, get_csv_filename(self.category))
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="scrapy_db"
        )
        cursor = mydb.cursor()
        csv_data = csv.reader(open(get_csv_filename(self.category),encoding='UTF-8'))
        row_count = 0
        for row in csv_data:
            if row_count != 0:
                cursor.execute('''
                    insert into books_table
                    (
                        title,price,description,images
                    ) values (
                        %s,%s,%s,%s
                    )
                ''', row)
                
            row_count += 1
            
        mydb.commit()
        cursor.close()
        
def get_csv_filename(category):
    category_name = ''
    cat_regex_result = re.compile("\/books\/(.+)_\d+\/").search(category)
    if cat_regex_result is not None:
        category_name = cat_regex_result.group(1)

    csv_name = 'books_mysql.csv'
    if category_name != '':
        csv_name = 'books_mysql-{0}.csv'.format(category_name)   
    return csv_name