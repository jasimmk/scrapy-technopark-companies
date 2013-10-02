# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class CompanyProp(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    desc = Field()
    link = Field()
    email = Field()
    address = Field()
    phone = Field()