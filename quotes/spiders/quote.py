# -*- coding: utf-8 -*-
import scrapy

from quotes.items import QuotesItem


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def start_requests(self):
        # 当实现该方法时，start_urls将被忽略(测试结论，非官方资料)
        # 测试请求出错的情况，禁止重试，下载超时为3秒
        yield scrapy.Request('https://www.google.com/',
                             meta={'dont_retry': False, 'download_timeout': 3.0})

    def parse(self, response):
        # print(response.text)

        # 抽取列表数据
        for quote in response.css('div.col-md-8 > div.quote'):
            item = QuotesItem()
            # 抽取名言
            item['text'] = quote.css('span.text::text').extract_first()
            # 抽取作者
            item['author'] = quote.css('small.author::text').extract_first()
            # 抽取标签
            item['tags'] = quote.css('div.tags > a::text').extract()

            yield item

        # 抽取下一页链接
        next_href = response.css('li.next > a::attr(href)').extract_first()
        if next_href:
            next_url = response.urljoin(next_href)
            yield scrapy.Request(url=next_url, callback=self.parse)
