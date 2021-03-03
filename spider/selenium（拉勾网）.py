from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

'''
# PhantomJS后台浏览器，无弹窗
dirver = webdriver.PhantomJS()
dirver.get('https://www.baidu.com')
print(dirver.page_source)
'''
driver = webdriver.Chrome()
driver.get('https://www.lagou.com')
# 通过xpath查找，找到对应的元素并点击
driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
# 等待
time.sleep(1)
# 找到输入框，输入python
driver.find_element_by_xpath('//*[@id="search_input"]').send_keys('python', Keys.ENTER)
# 关闭二维码弹窗
driver.find_element_by_xpath('/html/body/div[8]/div/div[2]').click()
# 找到所有class为position_link标签
position_links = driver.find_elements_by_class_name('position_link')

path = 'message\\'
n = 1
for position_link in position_links:
    # 找到H3并点击
    position_link.find_element_by_tag_name("h3").click()

    # 窗口转换
    # 跳转到列表倒数第一个
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)

    # 获取招聘信息，提取文本
    text = driver.find_element_by_xpath('//*[@id="job_detail"]/dd[2]').text
    # 把招聘信息保存到文本中
    # 文件夹是否存在
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    f = open( path + '需求%s.txt' % n, 'w', encoding='utf-8')
    f.write(text)
    f.close

    # 关闭窗口
    driver.close()
    # 跳转到第一个窗口
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    n += 1

# 关闭窗口
driver.close()