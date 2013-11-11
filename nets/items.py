# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class NetsItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class DianpingItem(Item):
    id = Field()
    name = Field()
    enname = Field()
