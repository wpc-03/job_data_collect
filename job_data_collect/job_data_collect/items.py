# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobDataCollectItem(scrapy.Item): # 本质是一个字典  键值对的形式
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name=scrapy.Field()
    company_name =scrapy.Field()
    base_message =scrapy.Field()
    company_address =scrapy.Field()
    company_details_message =scrapy.Field()
    job_message =scrapy.Field()
    salary =scrapy.Field()

