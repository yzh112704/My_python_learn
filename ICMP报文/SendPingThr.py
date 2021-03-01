import socket  # 套接字
import threading  # 多线程
from queue import Queue  # 队列
import time  # 时间


class SendPingThr(threading.Thread):
    '''
    发送ICMP请求报文的线程。
    参数：
        ipPool      -- 可迭代的IP地址池
        icmpPacket  -- 构造的icmp报文
        icmpSocket  -- icmp套字接
        timeout     -- 设置发送超时
    '''

    def __init__(self, ipPool, icmpPacket, icmpSocket, timeout=3):
        threading.Thread.__init__(self)
        self.Sock = icmpSocket
        self.ipPool = ipPool
        self.packet = icmpPacket
        self.timeout = timeout
        self.Sock.settimeout(timeout + 3)

    def run(self):
        time.sleep(0.01)  # 等待接收线程启动
        for ip in self.ipPool:
            try:
                self.Sock.sendto(self.packet, (ip, 0))
            except socket.timeout:
                break
        time.sleep(self.timeout)
