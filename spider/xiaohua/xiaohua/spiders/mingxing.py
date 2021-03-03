# -*- coding: utf-8 -*-
import scrapy
from xiaohua.items import XiaohuaItem

class MingxingSpider(scrapy.Spider):
    name = 'mingxing'
    # allowed_domains = ['www.521609.com/']
    start_urls = ['http://www.521609.com/tuku/mxxz/']

    # 生成一个通用url模板
    url = 'http://www.521609.com/tuku/mxxz/index_%d.html'
    page_num = 2


    def parse_detail(self, response):
        title = response.meta['title']
        div_list = response.xpath('//*[@id="swiper1"]/div/div')
        num = 1
        for div in div_list:
            img_url = 'http://www.521609.com' + div.xpath('.//img/@src').extract_first().strip()
            # print('img_url:', img_url)
            item = XiaohuaItem()
            item['title'] = title
            item['img_name'] = str(num).zfill(2) + '.jpg'
            yield scrapy.Request(url=img_url, callback=self.prase_img, meta={'item': item})
            num += 1


    def prase_img(self, response):
        item = response.meta['item']
        item['img'] = response.body
        yield item


    def parse(self, response):
        li_list = response.xpath('/html/body/div[4]/div[3]/ul/li')
        for li in li_list:
            detail_url = 'http://www.521609.com' + li.xpath('./a/@href').extract_first().strip()
            detail_title = li.xpath('./a/@title').extract_first().strip()
            # print('detail_title:', detail_title)
            # 请求传参
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'title': detail_title})

        if self.page_num <= 2:
            new_url = format(self.url % self.page_num)
            self.page_num += 1
            # 手动请求发送：callback回调函数是专门用于数据解析
            yield scrapy.Request(url=new_url, callback=self.parse)
