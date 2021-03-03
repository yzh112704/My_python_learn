# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

class XiaohuaPipeline(object):
    fp = None

    # 重写父类的一个方法：该方法只在开始爬虫时候被调用一次
    def open_spider(self, spider):
        path = './图片下载'
        if not os.path.exists(path):
            os.mkdir(path)
        print('开始爬虫......')

    # 专门用来出来item对像
    # 该方法可以接收到爬虫文件提交的item对象
    # 该方法每接收到一个item就会被调用一次
    def process_item(self, item, spider):
        title = item['title']
        img_name = item['img_name']
        img = item['img']
        path = './图片下载\\' + title

        if not os.path.exists(path):
            os.mkdir(path)
        self.fp = open(path + '\\' + img_name, 'wb')
        self.fp.write(img)
        self.fp.close()
        print('保存' + title + '\\' + img_name + ' 成功！！')

        return item  # 会返回给下一个要执行的管道类

    def close_spider(self, spider):
        print('\n\n------------------------------------------------------\n结束爬虫！！')

