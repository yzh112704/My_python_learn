from bs4 import BeautifulSoup
import requests
import os


def get_list(url, headers):
    response = requests.get(url, headers=headers)
    html_text = response.text.encode(response.encoding).decode('utf-8')
    soup = BeautifulSoup(html_text, 'lxml')
    div_book = soup.find('div', attrs={'class': 'book-mulu'})
    lst = div_book.find_all('a')
    return lst


def get_text(url, headers):
    response = requests.get(url, headers=headers)
    html_text = response.text.encode(response.encoding).decode('utf-8')
    soup = BeautifulSoup(html_text, 'lxml')
    div_card = soup.find('div', attrs={'class': 'card bookmark-list'})
    title = div_card.find('h1').text
    text = div_card.find('div', attrs={'class': 'chapter_content'}).text
    return title + '\n\n' + text


def save_text(name, text, path, file_type):
    if not os.path.exists(path + name):
        with open(path + name + file_type, 'w', encoding='utf-8') as f:
            f.write(text)
            f.close()
            print("保存 %s 章节完成" % name)
    else:
        print("%s 章节已经下载过了!!" % name)


def add_text(path, dir_name, total, file_name):
    texts = os.listdir(path + dir_name)
    if len(texts) == total:
        with open(path + file_name, 'w', encoding='utf-8') as f:
            for name in texts:
                with open(path + dir_name + '\\' + name, 'r', encoding='utf-8') as q:
                    text = q.read()
                    f.write(text)
                    q.close()
            f.close()
        print('%s合并完成' % file_name)
    else:
        print('章节下载有缺失！！')


def main():
    domain = 'https://www.shicimingju.com/'
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81'}
    path = os.getcwd() + '\\'
    file_name = '三国演义'
    file_type = '.txt'
    dir_name = file_name + '(分小节)\\'

    lst = get_list(url, headers)
    if not os.path.exists(path + dir_name):
        os.mkdir(path + dir_name)
    num = 1
    for li in lst:
        url = domain + li.get('href')
        name = str(num).zfill(4) + li.text
        if not os.path.exists(path + dir_name + name + file_type):
            text = get_text(url, headers)
            save_text(name, text, path + dir_name, file_type)
        else:
            print("%s had saved!!" % name)
        num += 1
    add_text(path, dir_name, len(lst), file_name + file_type)


if __name__ == '__main__':
    main()
