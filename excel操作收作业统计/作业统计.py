import xlrd
import xlsxwriter
import os
import re

def main(name, path, count, cishu):                     # count为1时创建新列
    wk = xlrd.open_workbook(path + '\\' + name)         # 读取Excel
    workbook = xlsxwriter.Workbook(path + '\\' + name)  # 新建Excel并编辑
    ws = wk.sheet_by_index(0)       # 获取Excel中第一个sheet（即sheet0）
    nrows = ws.nrows                # 获取总行数
    data_nums = ws.col_values(0)    # 获取第一列（学号）
    data_names = ws.col_values(1)   # 获取第二列（姓名）
    datas_one = ws.row_values(0)    # 获取第一行（表头）
    data_flags = []                 # 前几次实验的对号存储
    worksheet = workbook.add_worksheet()    # 操作Excel表
    num = 0                 # 统计总共多少列
    person = 0              # 统计未交人数
    repeat = []
    for data in datas_one :
        worksheet.write(0, num, data)   # 写入表头（每一列第一行）
        num += 1
    for i in range(2 , num) :           # 获取对号信息
        data_flags.append(ws.col_values(i))
    if count:                           # 是否添加新的表头
        worksheet.write(0, num, cishu)
    else :
        num -= 1
    for i in range(1, nrows) :          # 从第二行开始遍历
        for j in range(0, num - 2):     # 把前几次实验的对号信息写入新Excel表
            worksheet.write(i, j + 2, data_flags[j][i])
        flag = open_file(data_names[i], data_nums[i], path)   # 标记是否已交
        worksheet.write(i, 0, data_nums[i])     # 写入学号
        worksheet.write(i, 1, data_names[i])    # 写入姓名
        if flag :
            worksheet.write(i, num , '√')      # 已交打上对号
            if flag != 1 :
                repeat.append(data_names[i] + '交了' + str(flag) + '次')
        else :
            print(data_names[i] + '未交')       # 输出谁没交
            person += 1
    workbook.close()                            # 保存新表（更新信息）
    print('\n共' + str(nrows - 1 ) + '人\n' +str(person) + '人未交')     # 输出总人数与未交人数
    if repeat:
        print('\n重复提交：')
        for string in repeat :                  
            print(string)                       #输出重复提交的人的名字
    input('\npress Eneter to exit')             # 输入回车退出
def open_file(file_name, file_num, path) :      #file_name 文件名（姓名）      file_num 学号     path 路径
    flag = 0                                    #统计交的次数
    for root, dirs, files in os.walk(path):     # 获取当前文件夹下的所有文件名
        for file in files:
            if re.search(file_name, file) != None:          # 判断文件名与Excel中的名字是否相同
                flag += 1                                   #统计交的次数，每扫描到一个+1
                file_type = re.search('.*?(\.\D+)',file)    #获取文件类型后缀
                try :
                    os.renames(file, str(int(file_num)) + file_name + file_type.group(1))
                except :
                    if flag == 1 :
                        os.renames(file, str(int(file_num)) + file_name + '(' + str(flag) + ')' + file_type.group(1))
                    else :
                        os.renames(file,str(int(file_num)) + file_name + '(' + str(flag - 1) + ')' + file_type.group(1))    #重命名为学号+姓名+（flag -1）
    return flag
if __name__ == "__main__":
    name = '统计.xlsx'        # 表名
    path = os.getcwd()                    # 获取当前目录
    cishu = '第一次'                      # 创建新列的名称
    main(name,path,1,cishu)
