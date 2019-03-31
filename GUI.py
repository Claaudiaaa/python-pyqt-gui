import  sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication,QPushButton,QDialog,QGridLayout,QLabel,QWidget,QInputDialog,QLineEdit,QVBoxLayout,QTextEdit
from PyQt5.QtCore import QCoreApplication
import requests
import json
import cv2
import btnfunc


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title="NASAService"
        self.InitWindow()


    # 主窗口界面设置
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.jpg"))
        self.setWindowTitle(self.title)
        self.resize(400, 800)
        self.btnAPOD = QPushButton('APOD', self)
        self.btnNEO = QPushButton('NEO', self)
        self.btnMARS = QPushButton('MARS', self)
        self.btnQUIT = QPushButton('EXIT', self)
        self.label = QLabel(" ")
        self.text=QTextEdit()
        self.label2=QLabel()
        self.label2.setPixmap(QPixmap('show.jpg').scaled(480,680,aspectRatioMode=1))





        # 布局设定
        #全局布局
        wlayout=QVBoxLayout(self)

        #局部布局
        layout1 = QGridLayout(self)
        vlayout=QVBoxLayout(self)

        #为局部添加控件
        layout1.addWidget(self.label,0,1,1,2)
        layout1.addWidget(self.btnAPOD,1,1,1,1)
        layout1.addWidget(self.btnNEO,1,2,1,1)
        layout1.addWidget(self.btnMARS,1,3,1,1)
        layout1.addWidget(self.btnQUIT, 1,4,1,1)

        vlayout.addWidget(self.label2)
        vlayout.addWidget(self.text)

        #准备两个控件
        gwg=QWidget()
        vwg=QWidget()

        #用两个控件设置局部布局
        vwg.setLayout(vlayout)
        gwg.setLayout(layout1)

        #将两个控件添加到全局布局中去
        wlayout.addWidget(vwg)
        wlayout.addWidget(gwg)

        #将窗口本身设置为全局布局
        self.setLayout(wlayout)

        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.btnAPOD.clicked.connect(self.APOD)
        self.btnNEO.clicked.connect(self.Neo)
        self.btnMARS.clicked.connect(self.Mars)
        self.btnQUIT.clicked.connect(self.quit)

    #button功能函数
    
    #获取每日天文图片
    def APOD(self):
        path,imstr,date,explanation=btnfunc.Get_APOD()
        if path:
            self.label2.setPixmap(QPixmap(path).scaled(480,680,aspectRatioMode=1))
            if date and explanation:
                self.text.setText("date:%s   explanation:%s"%(date,explanation))

        else:
            self.label2.setText('非图片格式，请访问： %s' %imstr)


    #获取小行星信息
    def Neo(self):
        i,ok = QInputDialog.getInt(self,'查找小行星','id：',0,0,9999999,1)
        if ok:
            id_num=str(i)
            (name,magnitude,dmin,dmax,L)=btnfunc.Get_NeoInfo(id_num)
            self.text.clear()  # 清理text
            if name:
                self.label2.setText("名称：%s \n绝对星等： %f\n估计直径/km：最小：%f  最大：%f" %(name,magnitude,dmin,dmax))
                for d in L:
                    self.text.append("接近日期: %s  轨道天体: %s"%(d['date'],d["orbiting_body"]) )
            else:
                self.label2.setText("此id不存在")
                
    #获取火星探测器拍到的图片
    def Mars(self):
        rover = ('curiosity','opportunity','spirit')
        item,ok=QInputDialog.getItem(self,"Mars Rover","请选择探测器：",rover,0,False)
        if ok:
            btnfunc.Grt_Mars_Pic(item)
    #退出程序
    def quit(self):
        sys.exit()

#运行程序

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
