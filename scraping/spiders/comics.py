import requests
import scrapy

from scraping.spiders.comic import Comic
from scraping.spiders.utility import write_data

from scrapy import signals, Spider


class Comics(Spider):
    name = "comics"

    def start_requests(self):
        urls = ["https://kiryuu.co/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        comics_url = response.xpath(
            '//div[@class="listupd"]/div[@class="utao"]/div/div[@class="luf"]/a[@class="series"]/@href'
        ).extract()

        new_comics = [comics_url[0], comics_url[1]]

        # loop comics_url and request each of that url
        for i, url in enumerate(new_comics):
            url = response.urljoin(url)
            request = scrapy.Request(
                url=url, callback=Comic().parse_comic,)
            request.meta["index"] = i
            yield request
