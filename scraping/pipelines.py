# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from scraping.spiders.utility import write_data, write_old
from scraping.spiders.save_comic import save_comic
from scraping.spiders.update_comic import update_comic


class ScrapingPipeline(object):

    def open_spider(self, spider):
        self.items = {}
        self.updateItems = {}
        self.old = {}

    def close_spider(self, spider):
        for item in self.items:
            res = save_comic(self.items[item])
            write_old(self.old)
            print(res.json())

        for updateItem in self.updateItems:
            res = update_comic(self.updateItems[updateItem])
            write_old(self.old)
            print(res.json())

    def parse_comic(self, item):
        # copy new obj
        data = dict(item)

        # copy olddata to self data
        self.old = data["old"]

        # delete unused property
        if data.get("update"):
            del data["update"]
        if data.get("old"):
            self.old = data["old"]
            del data["old"]

        # change property tipe to type
        # check if there have tipe method
        if item.get("tipe"):
            # if True copy and change method to Type and fill it
            data["type"] = item["tipe"]
            del data["tipe"]
        else:
            # if not make Type property ''
            if "tipe" in item:
                data["type"] = ''
                del data["tipe"]

        # check if title is in self items
        title = data["title"]
        if title not in self.items:
            self.items[title] = data

        return self.items[title]

    def parse_update_comic(self, item):
        data = dict(item)

        if data.get("update"):
            del data["update"]
        if data.get("old"):
            self.old = data["old"]
            del data["old"]

        title = data["title"]

        updateData = {
            "data": {
                "updateOn": data["updateOn"],
                "chapters": data["chapters"]
            },
            "where": {
                "title": title
            }
        }

        if title not in self.updateItems:
            self.updateItems[title] = updateData

        return self.updateItems[title]

    def process_item(self, item, spider):
        # check is update or not
        if item.get("update"):
            if item["update"] == True:
                self.parse_update_comic(item)
            else:
                self.parse_comic(item)
        else:
            self.parse_comic(item)

        return ''

    def create_comic(self, data):
        pass
