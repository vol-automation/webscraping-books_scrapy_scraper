# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksCrawlerItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_without_tax = scrapy.Field()
    price_with_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
    
    image_urls = scrapy.Field()
    images = scrapy.Field()
