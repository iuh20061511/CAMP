# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BooksItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    instock = scrapy.Field()
    product_description = scrapy.Field()
    urlBook = scrapy.Field()
    categories = scrapy.Field()
    star_rating = scrapy.Field()
    upc = scrapy.Field()
    price_exc = scrapy.Field()
    price_inc = scrapy.Field()
    tax  = scrapy.Field()
    number_review = scrapy.Field() 
    image_url = scrapy.Field()
