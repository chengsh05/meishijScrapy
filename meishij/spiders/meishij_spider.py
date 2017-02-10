import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from meishij.items import MeishijItem
import urllib

class MeiShiJSpider(scrapy.Spider):
    name = "meishij"
    allowed_domains = ["meishij.net"]
    start_urls = [
        "http://www.meishij.net/chufang/diy/"
    ]

    def parse(self, response):
        item = MeishijItem()

        selector = Selector(response)
        Dishes   = selector.xpath('//div [@class="listtyle1"]')
        i = 0
        for Dish in Dishes:
            item['name'] = Dish.xpath('a/@title').extract()
            item['url'] = Dish.xpath('a/@href').extract()
            item['dis']  = int(Dish.xpath('//div \
                    [@class="c1"]/span/text()').extract()[i].split()[0])
            item['pnum'] = int(Dish.xpath('//div \
                    [@class="c1"]/span/text()').extract()[i].split()[2])
            i = i+1
            yield item

        next_link = selector.xpath('//div [@class="listtyle1_page_w"]/a \
        [@class="next"]/@href').extract()[0]

        print type(next_link)
        print next_link

        yield Request(next_link,callback=self.parse)
