import scrapy

from scraping.spiders.chapter import Chapter
from scraping.items import ComicItem

import time


from scraping.olddata import old
from scraping.spiders.utility import write_old


t = time.localtime()

current_time = time.strftime("%Y-%m-%d", t)


# Search for an upper case "S" character in the beginning of a word, and print the word:


class Comic(scrapy.Spider):
    name = "comic"

    data = []

    def parse_comic(self, response):

        manga_id = response.xpath("//article/@id").get()
        manga_id = manga_id.replace("-", "")

        postedOn = response.xpath(
            "//time[@itemprop='dateModified']/@datetime").get()

        chapters_url = response.xpath(
            "//div[@class='bixbox bxcl']/ul/li/span[@class='lchx']/a/@href").extract()

        chapters_url = chapters_url
        chaptersName = response.xpath(
            "//div[@class='bixbox bxcl']/ul/li/span[@class='lchx']/a/text()").extract()

        self.comic_create(response)
        # check if old have manga_id
        if old.get(manga_id):
            if old[manga_id].get("postedOn"):
                if(old[manga_id]["postedOn"] != postedOn):
                    # if have save new postedOn
                    old[manga_id]["postedOn"] = postedOn
                    # loop for each urls
                    for i, url in enumerate(chapters_url):
                        # check if chapter  is new chapter
                        if chaptersName[i] not in old[manga_id]["chapters"]:
                            # append new chapter
                            old[manga_id]["chapters"].append(chaptersName[i])
                            url = response.urljoin(url)
                            # make request
                            request = scrapy.Request(
                                url=url, callback=Chapter().parse_chapter)
                            # add meta
                            request.meta["comic"] = self.comic_create(
                                response)
                            request.meta["chapterName"] = chaptersName[i]
                            request.meta["number"] = len(chapters_url) - i
                            request.meta["comic"]["update"] = True
                            request.meta["comic"]["old"] = old
                            yield request

        else:
            # make new old data
            old[manga_id] = {
                "postedOn": postedOn,
                "chapters": chaptersName
            }
            # loop for each urls
            for i, url in enumerate(chapters_url):
                url = response.urljoin(url)
                # make request
                request = scrapy.Request(
                    url=url, callback=Chapter().parse_chapter)
                # add meta
                request.meta["comic"] = self.comic_create(response)
                request.meta["chapterName"] = chaptersName[i]
                request.meta["comic"]["old"] = old
                request.meta["number"] = len(chapters_url) - i

                yield request

    def comic_create(self, response):
        # get data
        title = response.xpath(
            "//div[@class='infox']/h1/text()").get()

        image = response.xpath(
            '//article/div[1]/div[2]/div[1]/img/@src').get()

        japaneseTitle = response.xpath(
            "//div[@class='infox']/span[@class='alter']/text()").get()

        genres = response.xpath(
            "//div[@class='infox']/div[@class='spe']/span/a[@rel='tag']/text()").extract()

        author = response.xpath(
            '//article/div[1]/div[2]/div[2]/div[1]/span[4]/text()').get()

        status = response.xpath(
            '//article/div[1]/div[2]/div[2]/div[1]/span[2]/text()').get()
        status = " OnGoing" if status == "Ongoing" else "Finished"  # enum type match

        tipe = response.xpath(
            '//article/div[1]/div[2]/div[2]/div[1]/span[5]/a/text()').get()

        rating = response.xpath('//article//strong/text()').get()
        rating = rating.replace("Rating ", '')  # remove string 'Rating '
        try:
            rating = float(rating)  # change to FLoat
        except ValueError:
            rating = 0.0

        released = response.xpath(
            '//article/div[1]/div[2]/div[2]/div[1]/span[3]/text()').get()

        synopsis = response.xpath(
            '//article/div[1]/div[2]/div[2]/div[2]/div/span/p/text()').get()

        comicItem = ComicItem(
            title=title,
            image=image,
            japaneseTitle=japaneseTitle,
            author=author,
            status=status,
            tipe=tipe,
            rating=rating,
            released=released,
            synopsis=synopsis,
            genres={
                'create': list(map(lambda x: {"genre": x}, genres))
            },
            postedOn=current_time,
            postedBy="uki",
            updateOn=current_time,
            chapters={
                "create": []
            }

        )

        return comicItem
