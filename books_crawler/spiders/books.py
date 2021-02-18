from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
import csv
import glob
from openpyxl import Workbook

class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    # - Extract only books in the home page
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3/a'), callback='parse_page', follow=False),
    )

    def parse_page(self, response):
        title = response.xpath('//article[@class="product_page"]//h1/text()').extract_first()
        price = response.xpath('//p[@class="price_color"]/text()').extract_first()
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()
        yield {'link': response.url,
               'title': title,
               'price': price,
               'description': description
               } 
        
    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        wb = Workbook()
        ws = wb.active
        
        with open(csv_file, 'r',encoding='UTF-8') as f:
            for row in csv.reader(f):
                ws.append(row)
                
        wb.save(csv_file.replace('.csv','.xlsx'))
