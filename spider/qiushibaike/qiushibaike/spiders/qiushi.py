# -*- coding: utf-8 -*-
import scrapy
from qiushibaike.items import QiushibaikeItem


class QiushiSpider(scrapy.Spider):
    name = 'qiushi'
    #allowed_domains = ['www.qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/text/']

    # 命令持久化
    # def parse(self, response):
    #     # 解析： 作者名称，段子内容
    #     div_list = response.xpath('//*[@id="content"]/div/div[2]/div')
    #     # 存储所有解析到的数据
    #     all_data = []
    #     for div in div_list:
    #         # xpath返回的是列表，但是列表的元素一定是Selector类型对象
    #         # extract可以将Selector对象中的data参数存储的字符串提取出来,list存储
    #         # author = div.xpath('.//h2/text()').extract()[0]
    #         author = div.xpath('.//h2/text()').extract_first()
    #         # 列表调用了extract之后，则表示将列表中每一个Selector对象中data对应的字符串提取出来，存储到列表当中
    #         content = div.xpath('./a/div/span/text()')[0].extract()
    #         content = ''.join(content)
    #         print(author, content)
    #         dic = {
    #             'author': author,
    #             'content': content
    #         }
    #         all_data.append(dic)
    #     return all_data

    # 管道持久化
    def parse(self, response):
        # 解析： 作者名称，段子内容
        div_list = response.xpath('//*[@id="content"]/div/div[2]/div')
        # 存储所有解析到的数据
        all_data = []
        for div in div_list:
            # xpath返回的是列表，但是列表的元素一定是Selector类型对象
            # extract可以将Selector对象中的data参数存储的字符串提取出来,list存储
            # author = div.xpath('.//h2/text()').extract()[0]
            author = div.xpath('.//h2/text()').extract_first().strip()
            # 列表调用了extract之后，则表示将列表中每一个Selector对象中data对应的字符串提取出来，存储到列表当中
            content = div.xpath('./a/div/span/text()')[0].extract().strip()
            content = ''.join(content)
            # print(author, content)

            item = QiushibaikeItem()
            item['author'] = author
            item['content'] = content

            # 提交item到管道
            yield item