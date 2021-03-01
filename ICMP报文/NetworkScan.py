import os  # 操作系统
import IPy  # IP地址处理模块
import time  # 时间
import array  # 列表
import struct  #
import socket  # 套接字
import datetime  # 获取当前时间
import threading  # 多线程
from queue import Queue  # 队列
from SendPing import *
from SendPingThr import *


class NetworkScan():
    '''
    参数：
        timeout    -- Socket超时，默认3秒
        IPv6       -- 是否是IPv6，默认为False
    '''

    def __init__(self, ip, timeout=3, IPv6=False):
        self.ip = ip
        self.timeout = timeout
        self.IPv6 = IPv6
        self._LOGS = Queue()
        self.text = ''
        '''
        按照给定的格式(fmt),把数据转换成字符串(字节流)
        ,并将该字符串返回.
        '''
        self.__data = struct.pack('d', time.time())  # 用于ICMP报文的负荷字节（8bit）
        self.__id = os.getpid()  # 构造ICMP报文的ID字段，无实际意义

    @property  # 属性装饰器
    def __icmpSocket(self):
        # socket.getprotobyname('icmp')创建ICMP Socket
        if not self.IPv6:
            # socket.SOCK_RAW 原始套接字
            # 作用：获得网络协议名（如：'icmp'）对应的值
            Sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        else:
            Sock = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.getprotobyname("ipv6-icmp"))
        return Sock

    def __inCksum(self, packet):
        '''ICMP 报文效验和计算方法
           & 按位与运算符：参与运算的两个值,如果两个相应位都为1,则该位的结果为1,否则为0
        '''
        if len(packet) & 1:
            packet = packet + '\\0'
        words = array.array('h', packet)
        sum = 0
        for word in words:
            sum += (word & 0xffff)
            '''
            右移动运算符：把">>"左边的运算数的各二进位全部右移若干位，>> 右边的数字指定了移动的位数
            '''
        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        # 按位取反运算符：对数据的每个二进制位取反,即把1变为0,把0变为1 。~x 类似于 -x-1
        return (~sum) & 0xffff

    @property  # 负责把一个方法变成属性调用
    def __icmpPacket(self):
        '''构造 ICMP 报文'''
        if not self.IPv6:
            header = struct.pack('bbHHh', 8, 0, 0, self.__id, 0)
            # 是构造一个icmp 回显请求包
            # header ：type(8)类型  code (8)编码   checksum  (16)检验和
            # id  (16)IP地址  sequence(16)序列号
        else:
            header = struct.pack('BbHHh', 128, 0, 0, self.__id, 0)
        packet = header + self.__data  # 包没有检验和
        chkSum = self.__inCksum(packet)  # 生成检验和
        if not self.IPv6:
            header = struct.pack('bbHHh', 8, 0, chkSum, self.__id, 0)
        else:
            header = struct.pack('BbHHh', 128, 0, chkSum, self.__id, 0)
        return header + self.__data  # 返回有检验和的包

    def isUnIP(self, IP):
        '''判断IP是否是一个合法的单播地址'''
        IP = [int(x) for x in IP.split('.') if x.isdigit()]
        # IP地址按“.”分开为四部分存储到IP列表当中
        if len(IP) == 4:
            if (0 < IP[0] < 223 and IP[0] != 127 and IP[1] < 256 and IP[2] < 256 and 0 < IP[3] < 255):
                return True
        return False

    def isUnIPs(self, IP):
        '''判断IP是否是一个合法的网段'''
        IP = [int(x) for x in IP.split('.') if x.isdigit()]
        # IP地址按“.”分开为四部分存储到IP列表当中
        if len(IP) == 4:
            if (0 < IP[0] < 223 and IP[0] != 127 and IP[1] < 256 and IP[2] < 256 and 0 == IP[3]):
                return True
        return False

    def makeIpPool(self, startIP, lastIP):
        '''生产 IP 地址池'''
        IPver = 6 if self.IPv6 else 4
        intIP = lambda ip: IPy.IP(ip).int()  # 将IP地址转换为整型格式
        ipPool = {IPy.intToIp(ip, IPver) for ip in range(intIP(startIP), intIP(lastIP) + 1)}

        return {ip for ip in ipPool if self.isUnIP(ip)}

    def mPings(self, ipPool):
        '''利用ICMP报文探测网络主机存活
        参数：
            ipPool  -- 可迭代的IP地址池
        '''
        Sock = self.__icmpSocket
        Sock.settimeout(self.timeout)
        packet = self.__icmpPacket
        recvFroms = set()  # 接收线程的来源IP地址容器

        sendThr = SendPingThr(ipPool, packet, Sock, self.timeout)
        sendThr.start()  # 线程开始

        while True:
            # 接受响应数据包
            try:
                '''Sock.recvfrom(1024)返回值为二元组 
                第一个返回值为数据报类容
                第二个为发送该数据包的客户端地址 
                '''
                recvFroms.add(Sock.recvfrom(1024)[1][0])
            except Exception:
                pass
            # 无论是否发生异常都执行下面代码
            finally:
                # 判断线程是否运行
                if not sendThr.isAlive():
                    break
        return recvFroms & ipPool

    def mPing(self, ip):
        '''利用ICMP报文探测网络主机存活
        参数：
            ip  -- IP地址
        '''
        Sock = self.__icmpSocket
        Sock.settimeout(self.timeout)
        packet = self.__icmpPacket
        send = SendPing(ip, packet, Sock, self.timeout)  # 发送ICMP请求报文到目的ip
        send.run()
        try:
            s = Sock.recvfrom(1024)[1][0]
            self.flag = 1  # flag 判断发送报文是否成功
        except:
            self.text += '连接超时'
            self.flag = 0
        return ip  # 返回IP地址

    def i(self):
        self.text += '探测单个主机：\n'
        if self.isUnIP(self.ip):  # 判断IP是否合法
            self.mPing(self.ip)  # 发送单个ICMP请求报文
            if self.flag:
                self.text += str(self.ip) + " 主机存活."
            else:
                self.text += str(self.ip) + ' 主机无响应.'
        else:
            self.text += '输入IP地址有误。'
        self.text += '\n'
        self.save_log()

    def s(self):
        self.text += "开始内网主机扫描：\n"
        if self.isUnIPs(self.ip):
            args = "".join(self.ip)  # 以“.”分割IP地址为4部分
            ip_prefix = '.'.join(args.split('.')[:-1])
            ip_start = ip_prefix + ".1"  # 网段第一个IP地址
            ip_end = ip_prefix + ".255"  # 网段最后一个IP地址
            ipPool = self.makeIpPool(ip_start, ip_end)  # 生成地址池
            alive_ip = self.mPings(ipPool)  # 多线程测试地址池中所有地址
            for i in alive_ip:
                self.text += str(i) + " 主机存活。\n"
        else:
            self.text += '输入IP地址有误。'
        self.text += '\n'
        self.save_log()

    def save_log(self):  # 本文件目录下保存日志文件
        f = open('log.txt', 'a')
        f.write(str(datetime.datetime.now()) + 's\n')  # 当前日期
        f.write(self.text)
        f.close()
