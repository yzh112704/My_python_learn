# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class QiushibaikePipeline(object):
    fp = None
    # 重写父类的一个方法：该方法只在开始爬虫时候被调用一次
    def open_spider(self, spider):
        print('开始爬虫......')
        self.fp = open('./qiubai.txt', 'w', encoding='utf-8')
    # 专门用来出来item对像
    # 该方法可以接收到爬虫文件提交的item对象
    # 该方法每接收到一个item就会被调用一次
    def process_item(self, item, spider):
        author = item['author']
        content = item['content']

        self.fp.write(author + ":\n" + content + '\n\n')

        return item     # 会返回给下一个要执行的管道类

    def close_spider(self, spider):
        print('结束爬虫！！')
        self.fp.close()

# 管道文件中一个管道类对应将一组数据存储到一个平台或载体中
class mysqlPipeline(object):
    conn = None
    cursor = None

    def open_spider(self, spider):
        print('链接MySQL数据库......')
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='123456', db='qiushi', charset='utf8')

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute('insert into qiushi values("%s", "%s")' % (item["author"], item["content"]))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item  # 会返回给下一个要执行的管道类

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        print('断开数据库连接！！')
