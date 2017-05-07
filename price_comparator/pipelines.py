# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from price_comparator.items import Product
from price_comparator.items import Category


class CleanPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Product):
            if None not in item.values():
                print "Product verified!"
                return item
            else:
                raise DropItem("Product droped( missing fields) : %s" % item)
        elif isinstance(item, Category):
                if None in item.values() or "" in item.values():
                    raise DropItem("Category droped(missing fields): %s" % item)
                else:
                    return item
        else:
                pass


class PriceComparatorPipeline(object):
    def process_item(self, item, spider):
        if item['price'] is not None:
            print "Price : %s " % item['price']
        return item
