class SendPing():
    '''
    发送单个ICMP请求报文
    参数：
        ip     -- IP地址
        icmpPacket  -- 构造的icmp报文
        icmpSocket  -- icmp套字接
        timeout     -- 设置发送超时
    '''

    def __init__(self, ip, icmpPacket, icmpSocket, timeout=3):
        self.Sock = icmpSocket
        self.ip = ip
        self.packet = icmpPacket
        self.timeout = timeout
        self.Sock.settimeout(timeout + 3)

    def run(self):
        self.Sock.sendto(self.packet, (self.ip, 0))  # 发送报文到ip
