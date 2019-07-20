# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    japaneseTitle = scrapy.Field()
    status = scrapy.Field()
    image = scrapy.Field()
    tipe = scrapy.Field()
    rating = scrapy.Field()
    synopsis = scrapy.Field()
    released = scrapy.Field()
    postedOn = scrapy.Field()
    postedBy = scrapy.Field()
    updateOn = scrapy.Field()
    userRating = scrapy.Field()
    userVote = scrapy.Field()
    genres = scrapy.Field()
    chapters = scrapy.Field()
    update = scrapy.Field()
    old = scrapy.Field()
