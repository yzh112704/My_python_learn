import selenium.webdriver
from bs4 import BeautifulSoup
import requests
import re
import threading
import os
import easygui as t
from PIL import Image

requests.packages.urllib3.disable_warnings()
lock = threading.Lock()  # 只是定义一个锁
threads = []  # 多线程存放进程
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81'}


# 漫画列表
urls = {'https://www.manhuaniu.com/manhua/14782/': '神武帝尊'
        }


# 创建漫画列表
def create_list():
    global urls
    choice = t.choicebox(msg='选择漫画', title='', choices=urls.items())
    if choice is None:
        return
    choice = re.search('(https.*?\d+/)', choice)
    url = choice.group(1)
    num = re.search('(\d+)', url)
    num = num.group(1)
    response = requests.get(url, verify=False)
    text = response.text
    text = re.search('<h3>《(.*?)》 - 章节全集</h3>.*?<ul id="chapter-list-1" data-sort="asc">(.*?)</ul>', text, re.S)
    txts = re.findall('li(.*?)</li>', text.group(2), re.S)
    f = open('list.txt', 'w', encoding='utf-8')
    count = 0
    for txt in txts:
        count += 1
        message = re.search('<a href="(.*?)".*?<span>(.*?)</span>', txt, re.S)
        url = 'https://www.manhuaniu.com' + message.group(1)
        name = message.group(2)
        txt = name + ' ' + url + '\n'
        f.write(txt)
    f.close()
    return text.group(1)


# 创建漫画最新话列表
def create_new_list():
    names_urls = {}
    global urls
    for url, n in urls.items():
        response = requests.get(url, verify=False)
        text = response.text
        text = re.search('<h3>《(.*?)》 - 章节全集</h3>.*?<ul id="chapter-list-1" data-sort="asc">(.*?)</ul>', text, re.S)
        txts = re.findall('li(.*?)</li>', text.group(2), re.S)
        f = open('list.txt', 'w', encoding='utf-8')
        for txt in txts:
            message = re.search('<a href="(.*?)".*?<span>(.*?)</span>', txt, re.S)
            url = 'https://www.manhuaniu.com' + message.group(1)
            name = message.group(2)
            txt = name + ' ' + url + '\n'
            f.write(txt)
        f.close()
        names_urls.update({n + name + '\n': url})
    return names_urls


# 获取漫画本话的页数
def get_url_page_num(url):
    response = requests.get(url)
    text = response.text
    txt = re.search('<h2>(.*?)</h2>.*?class="curPage"></span>/(.*?)\)</', text, re.S)
    num = int(txt.group(2))
    print('共' + str(num) + '页')
    return num


# 获取到每一页的url
def get_url_lists(url, num):
    url_lists = ''
    for i in range(1, num + 1):
        url_lists += url + '?p=' + str(i) + '\n'
    return url_lists


# 找到想要下载漫画话数的url
def search_url():
    f = open('list.txt', 'r', encoding='utf-8')
    txt = []
    line = f.readline()
    while line:
        string = re.search('(.*?)https', line)
        txt.insert(0, string.group(1) + '\n')
        line = f.readline()
    f.close()
    choices = t.multchoicebox(msg='选择需要下载的话', title='', choices=txt)
    if choices is None:
        return
    f = open('list.txt', 'r', encoding='utf-8')
    lst = f.read()
    names_urls = {}
    for choice in choices:
        string = re.search(choice.replace("\n", "") + '.*?(ht.*?html)', lst)
        names_urls.update({choice: string.group(1)})
    f.close()
    return names_urls


def get_page(url, path):  # 判断该页是否已下载，并得到网页信息
    num = re.search('html\?p=(\d+)', url)
    if num is None:
        return
    name = path + '\\' + num.group(1) + '.png'
    if os.path.exists(name):
        print('第' + num.group(1) + '页已下载！')
    else:
        driver = selenium.webdriver.PhantomJS()
        driver.get(url)
        text = driver.page_source
        driver.close()
        return text


# 获取到漫画该页的图片内容并下载
def get_message(text, path):
    soup = BeautifulSoup(text, 'xml')
    img_url = soup.find_all('img')
    img = img_url[0].get('src')
    txt = re.search('<h2>(.*?)</h2>.*?curPage">(.*?)</span>', text, re.S)
    name = path + '\\' + txt.group(2) + '.png'
    response = requests.get(img, verify=False)
    with open(name, 'wb') as f:
        f.write(response.content)
        f.close()
        print('第' + txt.group(2) + '页下载完成！')


# 下载图片
def create_img(url, path):
    text = get_page(url, path)
    if text is not None:
        get_message(text, path)


# 合并成长图
def create_result_img(path, name, num):
    file = os.getcwd() + '\\长图\\' + name + '.png'
    # 长图是否已经合成
    if os.path.exists(file):
        print('已合成长图。')
    else:
        path += '\\'
        name += '.png'
        i = 1
        try:
            # 保存图片列表
            ims = []
            # 最大宽度、总高度
            max_width, total_height = 0, 0
            for i in range(1, num):
                img = Image.open(path + str(i) + '.png')
                ims.append(img)
                # 按照所有图片最大的宽度
                if max_width < img.size[0]:
                    max_width = img.size[0]
                # 所有图片高度相加
                total_height += img.size[1]
            result = Image.new(ims[0].mode, (max_width, total_height))  # 新建空白图片（可以存放所有图片）
            # 长图粘贴图片位置的高度
            height = 0
            for i, im in enumerate(ims):
                # 粘贴图片
                # 横坐标居中(最大宽度减去当前图片宽度之后除以二)，纵坐标上一个图片高度的结尾
                result.paste(im, box=(int((max_width - im.size[0]) / 2), height))
                # 高度增加上一个图片的高度
                height += im.size[1]
            # 保存图片
            result.save(path + name)
            print('合成成功！')
            isExists = os.path.exists(os.getcwd() + '\\长图\\')
            if not isExists:
                os.makedirs(os.getcwd() + '\\长图\\')
            result.save(os.getcwd() + '\\长图\\' + name)
            print('长图文件夹合成成功！\n\n')
        except(OSError, NameError):
            print('图片 ', str(i) + '.png OS错误！！')


# 多线程下载
def threads_download(name, url):
    num = get_url_page_num(url)
    url_lists = get_url_lists(url, num)
    name = re.sub(':', '：', name)
    path = os.getcwd() + '\\' + name
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    for url_list in url_lists.split('\n'):
        t = threading.Thread(target=create_img, args=(url_list, path))  # 添加线程到线程列表
        threads.append(t)
        t.start()  # 启动线程
    for t in threads:
        t.join()
    create_result_img(path, name, num)


def main():
    import easygui as t
    choice = t.buttonbox('选择功能', '下载漫画', ('选择漫画', '最新话列表'))
    if choice is None:
        return
    elif choice == '选择漫画':
        while True:
            main_name = create_list()
            if main_name is None:
                return
            while True:
                names_urls = search_url()
                if names_urls is None:
                    break
                for file_name, url in names_urls.items():
                    name = main_name + file_name.replace('\n', '')
                    name = name[:-1]
                    threads_download(name, url)
    else:
        new_list = create_new_list()
        while True:
            import easygui as t
            choice = t.choicebox(msg='选择漫画', title='最新话', choices=new_list.items())
            if choice is None:
                return
            name = re.search("\('(.*?)\',", choice).group(0)
            name = name[2:-4]
            url = re.search('(https.*?html)', choice).group(0)
            threads_download(name, url)


if __name__ == '__main__':
    main()
