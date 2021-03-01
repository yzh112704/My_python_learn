from tkinter import *  # 界面
from tkinter import messagebox as msgbox  # 帮助弹窗
from NetworkScan import *


class Gui:  # 可视化界面
    def __init__(self):
        self.master = Tk()
        self.text = ''  # 文本信息
        self.parameter = StringVar()  # 参数
        self.IP = StringVar()  # IP地址

    def new(self):  # 重新运行
        self.text = ''
        self.main()

    def log(self):  # 读取日志
        path = 'log.txt'  # 日志文件名
        f = open(path, 'r')
        self.text = '日志内容:\n' + f.read() + '\n'
        self.show(0)  # 从开头显示
        f.close()

    def help(self):  # 文件说明
        msgbox.showinfo('说明', '''这是一个探测工具！
功能说明:

  -i          探测主机存活，输入框输入主机IP，例：192.168.1.1
  -s          探测内网存活的主机，输入框输入一个内网网段，例：192.168.1.0

    选择相应的功能，输入IP地址，点击开始进行测试。
    ''')

    def run(self):
        ip = self.IP.get()  # 获得IP地址
        p = self.parameter.get()  # 获得参数
        ping = NetworkScan(ip=ip)  # 继承类
        if p == 'i':
            ping.i()  # 单个发送报文
            self.text += ping.text + '\n'
        elif p == 's':
            ping.s()  # 多个发送报文
            self.text += ping.text + '\n'
        self.show(1)  # 显示最新内容（从结尾显示）

    def show(self, flag):
        text = Text(self.master, width=30, height=10)  # 文本显示大小
        text.grid(row=3, column=0, rowspan=4)  # 文本显示位置
        text.insert(INSERT, self.text)  # 显示self.text的文本
        if flag:  # 是否从结尾显示
            text.see(END)
        text.update()  # 更新显示文本

    def main(self):
        self.master.title('Ping命令')  # 窗口标题
        self.master.geometry('400x200')  # 窗口大小
        # 标签1
        l1 = Label(self.master, text='输入IP地址或网段：', font=("Arial", 15))
        l1.grid(row=0, column=0)  # 位置
        # 输入框
        insert = Entry(self.master, textvariable=self.IP)
        insert.grid(row=0, column=1, sticky=W)
        # 标签2 标签3
        l2 = Label(self.master, text='运行结果：')
        l2.grid(row=1, column=0, sticky=W)
        l3 = Label(self.master, text='从下列选择一个功能：')
        l3.grid(row=1, column=1)
        # 功能
        i = Radiobutton(self.master, text='-i 扫描一个', variable=self.parameter, value='i')
        i.grid(row=3, column=1, sticky=S + N)
        s = Radiobutton(self.master, text='-s 扫描网段', variable=self.parameter, value='s')
        s.grid(row=4, column=1, sticky=S + N)
        # 按钮
        button = Button(self.master, text='开始', command=self.run)
        button.grid(row=5, column=1, ipadx=20, ipady=10)
        # 显示文本框
        Text(self.master, width=30, height=10).grid(row=3, column=0, rowspan=4)
        # 菜单栏
        all = Menu(self.master)
        # menu菜单
        menu = Menu(all, tearoff=0)
        all.add_cascade(label='Menu', menu=menu)
        menu.add_command(label='New', command=self.new)
        menu.add_separator()  # 添加一条分隔线
        menu.add_command(label='Exit', command=self.master.destroy)
        # other菜单
        othermenu = Menu(all, tearoff=0)
        all.add_cascade(label='Other', menu=othermenu)
        othermenu.add_command(label='Log', command=self.log)
        othermenu.add_command(label='Help', command=self.help)
        self.master.config(menu=all)
        # 显示可视化
        mainloop()
