import easygui as t
import os
from bs4 import BeautifulSoup

xml = ''

def creat_xml() :
    global xml
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet href="biaoge.xsl" type="text/xsl" ?>
<学生信息表>\n'''
    n = t.enterbox('请输入学生的数量:','信息录入',)
    if n == None :
        return
    else:
        n = int(n)
    for i in range(n) :
        flag = 1
        message = ['学号', '姓名','性别','年龄','院系','入学时间']
        student = t.multenterbox('第个' + str(i+1) +'学生的信息：', '信息录入', message,)
        if student == None :
            return
        while flag :
            for mes in student :
                if mes == '' :
                    flag = 1
                    student = t.multenterbox('请重新输入第' + str(i + 1) + '个学生的信息：', '信息录入', message, )
                    break
            for mes in student :
                if mes != '' :
                    flag += 1
            if flag == 7 :
                flag = 0
        xml += creat_student_xml(student)
    xml += '</学生信息表>'
def creat_student_xml(message) :
    xml = ''
    xml += '<学生>\n'
    xml += '<学号>' + message[0] + '</学号>\n'
    xml += '<姓名>' + message[1] + '</姓名>\n'
    xml += '<性别>' + message[2] + '</性别>\n'
    xml += '<年龄>' + message[3] + '</年龄>\n'
    xml += '<院系>' + message[4] + '</院系>\n'
    xml += '<入学时间>' + message[5] + '</入学时间>\n'
    xml += '</学生>\n'
    return xml
def creat_xml_file(name,strs) :
    f = open(name, 'w',encoding='utf-8')
    f.write(strs)
    f.close()
def creat_xsl() :
    global xsl
    xsl = '''<?xml version="1.0" encoding="gb2312"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<html style="margin:0;
		        background:#E1FFFF;
				padding:0;
				font-style:normal;
				font-weight:normal;">

			<body style="margin:0 auto;padding:10px;">
				<center>
					<h1 style="font-size:25px; padding:50px auto">
					所有学生相关信息</h1>
					<table cellpadding="0px" cellspacing="0px" border="1px solid #8B3A3A" width="70%"
					 style="font:15px;font-family:'Times New Roman',Georgia,Serif;" >
						<tbody>
							<tr>
								<th width="16%" >学号</th>
								<th width="16%" >姓名</th>
								<th width="16%" >性别</th>
								<th width="16%" >年龄</th>
								<th width="16%" >所在院系</th>
								<th width="16%" >入学时间</th>
							</tr>
							<xsl:for-each select="/学生信息表/学生">
								<tr>
									<td align="center"><xsl:value-of select="学号"/></td>
									<td align="center"><xsl:value-of select="姓名"/></td>
									<td align="center"><xsl:value-of select="性别"/></td>
									<td align="center"><xsl:value-of select="年龄"/></td>
									<td align="center"><xsl:value-of select="院系"/></td>
									<td align="center"><xsl:value-of select="入学时间"/></td>
								</tr>
							</xsl:for-each>
						</tbody>
					</table>
				</center>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>
    '''
def creat_xsl_flie(name,strs) :
    f = open(name, 'w', encoding='gb2312')
    f.write(strs)
def use_xml() :
    global xml
    flag = ''
    f = open('biaoge.xml','r',encoding='utf-8')
    xml = f.read()
    new_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet href="biaoge.xsl" type="text/xsl" ?>
<学生信息表>\n'''
    message = ['学号', '姓名', '性别', '年龄', '院系', '入学时间']
    chioce = t.choicebox('选择要查找的方式','查找学生',message)
    if chioce == None :
        return
    m = t.enterbox('请输入需要查找的' + chioce + '信息：', '按' + chioce + '查找')
    while m == '' :
        m = t.enterbox('查找的' + chioce + '信息输入为空白，请重新输入：', '按' + chioce + '查找')
    soup = BeautifulSoup(xml,'xml')
    flag2 = 1
    for student in soup.find_all('学生') :
        if chioce == '学号' and student.学号.string == m and flag != '结束':
            flag = show_student_message(student)
            flag2 = 0
        if chioce == '姓名' and student.姓名.string == m and flag != '结束':
            flag = show_student_message(student)
            flag2 = 0
        if chioce == '性别' and student.性别.string == m and flag != '结束':
            flag = show_student_message(student)
            flag2 = 0
        if chioce == '年龄' and student.年龄.string == m and flag != '结束':
            flag = show_student_message(student)
            flag2 = 0
        if chioce == '院系' and student.院系.string == m and flag != '结束':
            flag = show_student_message(student)
            flag2 = 0
        if chioce == '入学时间' and student.入学时间.string == m and flag != '结束':
            flag = show_student_message(student)
            flag2 = 0
        if flag == '修改学生信息' :
            now_message = [student.学号.string,student.姓名.string,student.性别.string,student.年龄.string,student.院系.string,student.入学时间.string]
            student = t.multenterbox('输入需要修改的信息', '信息修改', message, now_message)
            if student == None:
                return
            student = creat_student_xml(student)
            flag = ''
        if flag == '删除':
            student = ''
            flag = ''
        new_xml += str(student)
    f.close()
    if flag2 :
        t.msgbox('没有符合要求的学生。')
        return
    return new_xml
def show_student_message(student) :
    message = [student.学号.string,student.姓名.string,student.性别.string,student.年龄.string,student.院系.string,student.入学时间.string]
    strs = ''
    strs += '学号' + message[0]
    strs += '\n姓名' + message[1]
    strs += '\n性别' + message[2]
    strs += '\n年龄' + message[3]
    strs += '\n院系' + message[4]
    strs += '\n入学时间' + message[5] +'\n'
    flag = t.buttonbox(strs,'查找到的学生信息',('修改学生信息','删除','继续'))
    return flag
def add()  :
    xml = ''
    flag = 1
    message = ['学号', '姓名', '性别', '年龄', '院系', '入学时间']
    student = t.multenterbox('输入添加学生的信息：', '信息录入', message, )
    while flag:
        for mes in student:
            if mes == '':
                flag = 1
                student = t.multenterbox('输入有错误，请重新输入学生的信息：', '信息录入', message, )
                break
        for mes in student:
            if mes != '':
                flag += 1
        if flag == 7:
            flag = 0
    xml += creat_student_xml(student) + '\n</学生信息表>'
    f = open('biaoge.xml', 'r', encoding='utf-8')
    q = open('biaoge2.xml', 'w', encoding='utf-8')
    line = f.readline()
    while line :
        if line == '</学生信息表>' :
            break
        q.write(line)
        line = f.readline()
    q.write(xml)
    f.close()
    q.close()
def change() :
    f = open('biaoge2.xml', 'r', encoding='utf-8')
    q = open('biaoge.xml', 'w', encoding='utf-8')
    strs = f.read()
    q.write(strs)
    f.close()
    q.close()
def creat_new_xml(new_xml) :
    new_xml += '\n</学生信息表>'
    creat_xml_file('biaoge.xml',new_xml)
def main() :
    chioce = t.buttonbox('选择从新录入信息或读取已有的信息', '学生信息管理', ('新建', '打开'))
    if chioce == '新建' :
        creat_xml()
        creat_xml_file('biaoge.xml', xml)
        creat_xsl()
        creat_xsl_flie('biaoge.xsl',xsl)
    flag = ''
    while flag != '退出' :
        flag = t.buttonbox('选择下列功能','选择面板',('功能（查找、修改、删除）','打开xml','添加','退出'))
        if flag == '功能（查找、修改、删除）' :
            new_xml = use_xml()
            if new_xml != None :
                creat_new_xml(new_xml)
        if flag == '打开xml' :
            os.system('"C:\\Program Files\\Internet Explorer\\iexplore.exe" ' + os.getcwd() + '\\biaoge.xml')
            #os.system('"D:\\Firefox\\firefox.exe" biaoge.xml')
        if flag == '添加' :
            add()
            change()

if __name__ == '__main__' :
    main()
