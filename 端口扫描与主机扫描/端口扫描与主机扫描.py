#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *        #套接字
import threading            #多线程
import easygui as easy      #可视化界面
import os                   #文件处理模块
import datetime             #获取当前时间
import re                   #正则匹配

lock = threading.Lock()     #只是定义一个锁
threads = []                #多线程存放进程
strs1 = ''                  #存放端口扫描到的结果
strs2 = ''                  #存放主机扫描到的结果
openNum = 0                 #统计开启端口的数量
hostNum = 0                 #统计主机的数量

def show(easy) :            #界面模块
    flag = 1
    while flag == 1 :       #判断是否结束
        way = easy.ccbox('选择功能模式', '端口扫描与主机扫描', ('端口扫描', '主机扫描'))
        if way :
            flag = port()
        else :
            flag = host()
def get_host_IP() :         #获得电脑主机IP
    strs = ''
    ip = ''
    outputs = os.popen('ipconfig')      #执行ipconfig命令
    for output in outputs:
        output = output.strip()
        strs += output + '\n'           #获取ipconfig所有信息
    IPs = re.findall('IPv4 地址.*?(\d+.\d+.\d+.\d+)',strs)        #正则表达是筛选IP
    for IP in IPs :
        ip += str(IP) + '\n'
    return ip
def useful_ip() :       #获得存在网关的ip信息
    strs = ''           #存储得到的信息
    ip_Gateway = ''     #存储IPv4与网关
    n = 0               #统计网卡个数
    outputs = os.popen('ipconfig')      #cmd执行ipconfig
    for output in outputs :             #获得的信息按网卡筛选分块
        output = output.strip()
        out = re.search('适配器 (.*?):', output)
        if out != None:
            n += 1
            strs += str(n) + '.适配器 :' + out.group(1) + '\n'
        out = re.search('IPv4.*?(\d+.\d+.\d+.\d+)',output)
        if out != None :
            strs += str(n) + '.IPv4 :' + out.group(1) + '\n'
        out = re.search('默认网关.*?(\d+.\d+.\d+.\d+)', output)
        if out != None :
            strs += str(n) + '.默认网关 :' + out.group(1) + '\n'
    for i in range(n+2) :       #筛选存在网关的网卡
        out = re.findall(str(i) + '\.(\D.*?)\n',strs)
        if len(out) == 3 :
            ip_Gateway += out[1] + '\n' + out[2] + '\n'
    return ip_Gateway       #返回IPv4与网关信息
def show_strs() :       #界面显示的信息
    strs = '扫描得到的主机IP :\n'
    strs += get_host_IP()
    strs += '\n建议使用的IP(ip配有网关)：\n'
    strs += useful_ip()
    return strs
def get_useful_ip() :       #获得存在网关的IPv4地址
    ip = re.search('IPv4 :(\d+.\d+.\d+.\d+)',useful_ip())
    return ip.group(1)
def port() :            #扫描端口模块
    global openNum
    global strs1
    strs1 = ''
    openNum = 0
    IP = easy.enterbox(show_strs() + '\n请输入IP:', '端口扫描', get_useful_ip())  # 界面获取输入的IP
    if IP == None:  # 判断是否点击cancle
        return
    ranges = easy.multenterbox('请输入端口范围：', '端口扫描', ['起始端口号', '结束端口号'], [1, 1024])
    # 获取输入的范围
    if ranges == None:  # 判断是否点击cancle
        return
    range_begin = int(ranges[0])    # 获得初始端口号
    range_end = int(ranges[1])      # 获得结束端口号
    strs1 += '扫描IP ：' + str(IP) + '\n起始端口号：' + str(range_begin) + '\n结束端口号：' + str(range_end)
    start_time = datetime.datetime.now()       #获取当前时间
    strs1 += '\n[开始时间] ' + str(start_time) + 's\n'
    strs1 = thread_port(IP, range_begin, range_end)
    end_time = datetime.datetime.now()  # 获取当前时间
    run_time = end_time - start_time
    strs1 += '[运行时间] ' + str(run_time) + 's\n' + '[结束时间] ' + str(end_time) + 's'
    creat_log(strs1,1)
    flag = easy.ccbox(strs1, '端口扫描', ('继续', '结束'))
    return flag
def thread_port(IP,range_begin,range_end) :     #多线程扫描端口
    global strs1
    for p in range(range_begin, range_end):  # 遍历初始端口号~结束端口号
        t = threading.Thread(target=portScanner, args=(IP, p))  # 创建线程TCP
        threads.append(t)  # 添加线程到线程列表
        t.start()  # 启动线程
    for t in threads:
        t.join()  # 等待至线程中止
    strs1 += '[*] 扫描完成!\n'
    strs1 += '[*] 总共 %d 个开启' % (openNum) + '\n'
    return strs1
def portScanner(host,port):         #扫描端口
    global openNum
    global strs1
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))      # 主动初始化服务器连接,连接出错，返回socket.error错误。
        lock.acquire()              # 当需要独占counter资源时，必须先锁定，这个锁可以是任意的一个锁
        openNum+=1
        strs1 += '[+]端口 %d 开启' % port + '\n'
        lock.release()              # 使用完counter资源必须要将这个锁打开，让其他线程使用
        s.close()
    except:
        pass                        # 如果出错，跳过。
def host() :                #主机扫描模块
    global strs2
    global hostNum
    strs2 = ''
    hostNum = 0
    ip = get_useful_ip()
    ip = ip.split('.')[:-1]
    ip = ('.'.join(ip) + '.' + '0')         #把得到的含有网关的IP地址转换成网段
    IP = easy.enterbox(show_strs() + '\n请输入需要扫描的网段:', '主机扫描', ip)  # 界面获取输入的IP
    if IP == None:  # 判断是否点击cancle
        return
    strs2 += '扫描IP ：' + str(IP)
    start_time = datetime.datetime.now()  # 获取当前时间
    strs2 += '\n[开始时间] ' + str(start_time) + 's\n'
    ping_all(IP)
    end_time = datetime.datetime.now()  # 获取当前时间
    run_time = end_time - start_time    # 多线程运行时间
    strs2 += '扫描到的主机数量为 ' + str(hostNum) + '个\n'
    strs2 += '[运行时间] ' + str(run_time) + 's\n' + '[结束时间] ' + str(end_time) + 's'
    creat_log(strs2, 0)
    flag = easy.ccbox(strs2, '主机扫描', ('继续', '结束'))  # 界面输出结果
    return flag

def ping_ip(ip):  # ping指定IP判断主机是否存活
    global strs2
    global hostNum
    output = os.popen('ping -n 1 %s ' % (ip)).readlines()   # ping -n 1 IP  结果按行读取
    os.popen('exit')        #每次使用完ping命令后关闭cmd端口
    for w in output:
        if str(w).upper().find('TTL') >= 0: # 判断使用ping命令得到的TTL值是否大于0
            strs2 += str(ip) + ' 在线\n'      # 扫描主机结果
            hostNum += 1                      #主机开启数量加1
def ping_all(ip):  # ping所有IP获取所有存活主机
    global threads
    pre_ip = (ip.split('.')[:-1])  # ip以.分割为数字，最后一部分不取
    # 例 192.168.1.1  划分成['192', '168', '1']，最后一部分不取
    for i in range(1, 256):
        add = ('.'.join(pre_ip) + '.' + str(i))     # 列表中间以.隔开，最后添加1~256
        t = threading.Thread(target=ping_ip, args =(add,))# 添加线程到线程列表
        threads.append(t)
        t.start()       # 启动线程
    for t in threads :
        t.join()        # 等待至线程中止
def creat_log(log,flag) :       #生成运行日志
    f = open('log.txt','a+',encoding='utf-8')
    if flag :
        f.write('端口扫描日志：\n')
    else :
        f.write('主机扫描日志：\n')
    f.write(log)
    f.write('\n\n')
    f.close()
def main() :
    setdefaulttimeout(1)        # 设置了全局默认超时时间
    show(easy)

if __name__ == '__main__':
    main()
