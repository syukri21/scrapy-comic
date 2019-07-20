from scraping.spiders.utility import write_data
import scrapy

import re
import time

import json


t = time.localtime()
current_time = time.strftime("%Y-%m-%d", t)


class Chapter(scrapy.Spider):

    name = "chapter"

    filledComic = []
    comicChapters = {}
    count = 0

    def parse_chapter(self, response):

        name = response.xpath(
            "//div[@class='headpost']//h1[@itemprop='name']/text()").get()
        images = response.xpath("//*[@id='readerarea']//img/@src").extract()

        postedOn = current_time
        postedBy = "uki"

        # make obj chapter
        chapter = {
            "number": response.meta["number"],
            "name": response.meta["chapterName"],
            "postedOn": postedOn,
            "postedBy": postedBy,
            "images": {
                "set": images
            }
        }

        comic = response.meta["comic"]
        # check comic is in filledComic or not
        if comic["title"] not in self.filledComic:
            # if true append new comic
            self.filledComic.append(comic["title"])

            # make new array for comic Chapter
            self.comicChapters[comic["title"]] = []

            # append new Chapter to new ComicChapter
            self.comicChapters[comic["title"]].append(chapter)
        else:
            # append new Chapter to existing comic
            self.comicChapters[comic["title"]].append(chapter)

        # fill create chapter with comic chapter
        comic["chapters"]["create"] = self.comicChapters[comic["title"]]

        yield comic
