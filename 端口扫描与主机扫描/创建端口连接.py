#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *        #套接字
while 1 :
    s = socket(AF_INET,SOCK_STREAM)
    s.bind(('192.168.1.1',996))
    s.listen(1)
