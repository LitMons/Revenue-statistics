import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QTableView
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from add import *

import sqlite3

#数据写入程序v1.1 
#增加写入数据反馈 
#数据为空反馈
#备注下拉列表方便输入

#未实现功能
#数据合法性检查
#错误数据报错 重复写入问题

class Ui_add(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self,parent=None):
        super(Ui_add, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.add)#按钮事件绑定，二级界面在此写
        self.pushButton_2.clicked.connect(self.quitdate)
    
    #添加数据函数
    def add(self):
        date=self.lineEdit.text()#输入框内容获取
        remarks=self.comboBox.currentText()
        a=self.lineEdit_3.text()

        if date=='' or a=='':
            self.textBrowser.append('没有数据，请输入数据')
        else:
            conn=sqlite3.connect('mrsoft.db')
            cursor=conn.cursor()
            sql='insert into income(income_date,remarks,income) values(?,?,?)'
            income=float(a)
            data=[(date,remarks,income),]#写入数据
            cursor.executemany(sql,data)
            conn.commit()
            cursor.close()
            conn.close()
            self.textBrowser.append('['+date+','+remarks+','+a+']'+'  数据写入成功！')

    #退出
    def quitdate(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Ui_add()
    w.show()
    sys.exit(app.exec_())