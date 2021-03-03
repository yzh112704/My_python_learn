import requests
from bs4 import BeautifulSoup
import os


# 获取图片信息（名字、链接、当前页数、总页数）
def get_image_message(url):
    response = requests.get(url)
    html = response.text.encode(response.encoding).decode('utf-8')
    page = BeautifulSoup(html, 'lxml')  # BeautifulSoup解析

    a = page.find('div', attrs={'class': 'ImageBody'}).find('img')
    # 找到class为ImageBody的div标签，找到img标签
    image_name = a.get('alt')  # 获取到alt属性内的名字
    image_url = a.get('src')  # 获取到src属性内的链接

    total = page.find('div', attrs={'class': 'ImageBody'}).find('img').find_next('script').text
    # 找到class为ImageBody的div标签，找到下一个script标签并获取文本内容
    total_split = total.split(",")  # 按,切割
    this_num = total_split[0].replace("\"", "").replace("Next(", "")
    total_num = total_split[1].strip('"')

    return image_name, image_url, this_num, total_num


def save_image(path, name, url):
    # 文件夹是否存在
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    if not os.path.exists(path + '\\' + name + '.jpg'):
        response = requests.get(url)
        # 保存图片
        f = open(path + '\\' + name + '.jpg', 'wb')
        f.write(response.content)
        f.close()
        print("download " + name + ' success!!')
    else:
        print(name + ' is downloaded.')


url = 'https://www.umei.cc/p/gaoqing/'
path = 'download\\'  # 保存路径
response = requests.get(url)
html = response.text.encode(response.encoding).decode('utf-8')
page = BeautifulSoup(html, 'lxml')
a_lists = page.find('div', attrs={'class': 'TypeList'}).find_all('a', attrs={'class': 'TypeBigPics'})
# 主页面获取（栏目）
for a in a_lists:
    href = a.get('href')
    name, img_href, this_num, total_num = get_image_message(href)
    save_image(path + name, name + this_num, img_href)
    # 栏目所有页数
    while int(this_num) + 1 <= int(total_num):
        this_num = str(int(this_num) + 1)
        # 重构url
        now_href = href.split('.htm')[0] + '_' + this_num + '.htm'
        name, img_href, this_num, total_num = get_image_message(now_href)
        save_image(path + name, name + this_num, img_href)

