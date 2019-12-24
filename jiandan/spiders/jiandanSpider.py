import scrapy
from jiandan.items import JiandanItem
from . import util
import re
import os
import urllib


class jiandanSpider(scrapy.Spider):
    name = 'jiandan'
    allowed_domains = []
    size = 0
    start_urls = ["http://jandan.net/ooxx"]

    def parse(self, response):
        item = JiandanItem()
        hashList = response.css('.img-hash::text').extract()
        print(len(hashList))

        for index, imgHash in enumerate(hashList):
            url = 'http:' + util.parse(imgHash, 'AGs7jEYU8SYmahnebE6Mvg6RCZsFysC9')
            replace = re.match(r'(.*\.sinaimg\.cn\/)(\w+)(\/.+\.gif)', url)
            if replace:
                url = replace.group(1) + 'large' + replace.group(3)
            e = re.match(r'.*(\.\w+)', url)
            extensionName = e.group(1)
            file_path = os.path.join("F:\\jiandan", str(self.size)+'-'+str(index) + extensionName)
            urllib.request.urlretrieve(url, file_path)
            print(url)

        yield item

        new_url = response.xpath('//a[@class="previous-comment-page"]//@href').extract_first()  # 翻页

        if new_url:
            self.size += 1
            if(self.size <20):
                yield scrapy.Request('http:'+new_url, callback=self.parse)

