import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QTableView
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from combobox import *
from addmain import *

import sqlite3

#收入统计程序v1.0.1
#增加数据添加功能
#数据修改功能暂未开放
#修改显示方式，取消lineEdit显示，使用label直接显示，程序界面未更新

class mwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(mwindow, self).__init__(parent)
        self.setupUi(self)
        
        self.lineEdit.hide()
        self.lineEdit_2.hide()
        self.pushButton_2.setEnabled(False)
        self.comboBox.addItem('2019')
        self.comboBox_3.addItem('2019')
        #下拉列表添加内容
        for i in range(9):
            self.comboBox_2.addItem('0'+str(i+1))
            self.comboBox_4.addItem('0'+str(i+1))
        for i in range(3):
            self.comboBox_2.addItem(str(i+10))
            self.comboBox_4.addItem(str(i+10))
        
        #设置表格
        self.model=QStandardItemModel(0,0)
        self.model.setHorizontalHeaderLabels(['年份','备注','金额'])
        self.tableView.setModel(self.model)

        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    #实现查询功能
    def getlist(self):
        syear=self.comboBox_3.currentText()#下拉列表内容获取
        smonth=self.comboBox_4.currentText()
        eyear=self.comboBox.currentText()
        emonth=self.comboBox_2.currentText()
        start='"'+syear+'-'+smonth+'-01"'
        end='"'+eyear+'-'+emonth+'-31"'

        if emonth>=smonth:
            #数据库查询
            conn=sqlite3.connect('mrsoft.db')
            cursor=conn.cursor()
            sql='select*from income where income_date>='+start+' and income_date<='+end
            cursor.execute(sql)
            result1=cursor.fetchall()
            num=len(result1)

            self.model=QStandardItemModel(num,3)#数据写入表格
            for row in range(num):
                for column in range(3):
                    i=QStandardItem(str(result1[row][column]))
                    self.model.setItem(row,column,i)
            self.model.setHorizontalHeaderLabels(['年份','备注','金额'])
            self.tableView.setModel(self.model)
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            #对查询金额统计
            sun=0
            for x in range(num):
                income=result1[x][2]
                sun=sun+income
            sun=round(sun,2)
            arv=round(sun/(int(emonth)-int(smonth)+1),2)
            text1='当前查询总额:'+str(sun)+'元'
            text2='月均:'+str(arv)+'元'
            self.label_3.setText(text1)
            self.label_8.setText(text2)
            #self.lineEdit.setText(str(sun)+'元')#设置输入框内容
            #self.lineEdit_2.setText(str(arv)+'元')
            cursor.close()
            conn.close()
        else:
            self.model=QStandardItemModel(0,0)
            self.tableView.setModel(self.model)
            self.label_3.setText('查询错误，请检查查询范围')
            self.label_8.setText('')
            self.lineEdit.hide()
            self.lineEdit_2.hide()
    
    #二级查询页面弹出
    def createdb(self):
        Ui_add.show()

    #退出主程序
    def closed(self):
        Ui_add.close()
        self.close()      
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mwindow()
    w.pushButton.clicked.connect(w.getlist)#按钮事件绑定
    w.pushButton_3.clicked.connect(w.createdb)
    w.pushButton_4.clicked.connect(w.closed)
    Ui_add=Ui_add()
    w.show()
    sys.exit(app.exec_())