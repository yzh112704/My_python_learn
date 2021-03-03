from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd    # 数据处理和分析，清洗

url = 'https://datachart.500.com/dlt/history/history.shtml'
driver = webdriver.Chrome()
driver.get(url)
driver.find_element_by_xpath('//*[@id="link183"]').click()
t_data = driver.find_element_by_xpath('//*[@id="tdata"]').text
driver.close()
#      |前区号码 |后 区|        |  一等奖 |  二等奖 |        |
# 期号|1 2 3 4 5|1   2|奖池奖金|注数 奖金|注数 奖金|总投注额|开奖日期
# f = open('t_data.txt', 'w', encoding = 'utf-8')
# f.write(t_data)
# f.close
total_data = []
for line in t_data.split('\n'):
    line_data = []
    for field in line.split(' '):
        line_data.append(field.replace(',', ''))
    total_data.append(line_data)
# 保存为csv格式（没有表头、索引）
pd.DataFrame(columns = None, data = total_data).to_csv('500.csv', header=False, index=False)