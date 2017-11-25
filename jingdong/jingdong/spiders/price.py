# -*- coding: utf-8 -*-
import scrapy
import chardet
import json
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup


class PriceSpider(scrapy.Spider):
    name = 'price'
    allowed_domains = ['jd.com']

    def start_requests(self):
        commodity_url = 'https://item.jd.com/15890328841.html'
        commodity_id = re.findall('(\d+)', commodity_url)[0]
        url_end = '&area=1_2901_4135_0&cat=737,794,878&extraParam={"originid":"1"}'
        price_url = 'https://c0.3.cn/stock?skuId={}{}'.format(
            commodity_id, url_end)
        yield scrapy.Request(price_url)

    def parse(self, response):
        print(response.body.decode('cp1251').encode('utf8'))
        data = json.loads(response.text)
