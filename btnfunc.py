import  sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication,QPushButton,QDialog,QGridLayout,QLabel,QWidget,QInputDialog,QLineEdit,QMessageBox
from PyQt5.QtCore import QCoreApplication
import requests
import json
import cv2
import btnfunc

#获取apikey
def Get_key():
    f=open('key.txt','r')
    apikey=f.read()
    f.close()
    return apikey

def Get_APOD():
    apikey=Get_key()
    url = "https://api.nasa.gov/planetary/apod?api_key="+apikey
    resp = requests.get(url)
    result = resp.json()
    mediatype = result["media_type"]
    # 资源类型为图片
    if mediatype == "image":

        imstr = result['url']

        img = requests.get(imstr).content
        path = 'APOD.jpg'
        with open(path, 'wb')as f:
            f.write(img)
        date=result['date']
        explanation=result['explanation']
        return path,imstr,date,explanation
    #资源类型为视频或其他
    else:
        return None,None,None,None



def Get_NeoInfo(id_num):
    apikey=Get_key()
    url = 'https://api.nasa.gov/neo/rest/v1/neo/' + id_num + '?api_key='+apikey
    resp = requests.get(url)
    if resp.status_code == 200:
        result = resp.json()
        L=[]
        # 选取指定元素 -接近日期和绕行天体
        for item in result["close_approach_data"]:
            d={}
            d['date']=item["close_approach_date"]
            d["orbiting_body"]=item["orbiting_body"]
            L.append(d)

        return (result['name'],result["absolute_magnitude_h"],result["estimated_diameter"]["kilometers"]["estimated_diameter_min"],result["estimated_diameter"]["kilometers"]["estimated_diameter_max"],L)
    else:
        return False, False, False, False,False


def Grt_Mars_Pic(probe):
    apikey=Get_key()
    url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/' + probe + '/photos?sol=1000&page=1&api_key=v'+apikey
    resp = requests.get(url)
    if resp.status_code == 200:
        result = resp.json()
        pic_id = 0
        for i in range(6):
            pic_url = result['photos'][i]['img_src']
            responce = requests.get(str(pic_url))
            img = responce.content
            path = str(pic_id) + '.jpg'
            with open(path, 'wb')as f:
                f.write(img)
                pic_id += 1
                i += 1
        #打开子窗口
        newWindow = SecondWindow()
        newWindow.show()
        newWindow.exec_()

# 子窗口
class SecondWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.newWindowUI()
    def newWindowUI(self):

        self.resize(500,700)
        self.move(200,200)
        self.buttonNext=QPushButton('Next',self)
        self.buttonPre=QPushButton('Pre',self)
        self.label_pic=QLabel()
        self.num=0
        # 布局设定
        layout2 = QGridLayout(self)
        layout2.addWidget(self.label_pic, 0, 1, 2, 2)
        layout2.addWidget(self.buttonNext, 2, 1, 1, 1)
        layout2.addWidget(self.buttonPre, 2, 2, 1, 1)

        self.label_pic.setPixmap(QPixmap(str(self.num)+'.jpg').scaled(500,500,aspectRatioMode=1))

        self.buttonPre.clicked.connect(self.Previous)
        self.buttonNext.clicked.connect(self.Next)

    #button功能函数
    #前一张图片
    def Previous(self):
        if self.num==0:
            # 消息框
            reply=QMessageBox.information(self,"提示",'没有上一张图片',QMessageBox.Yes,QMessageBox.No)
            print(reply)
        else:
            self.num=self.num-1
            self.label_pic.setPixmap(QPixmap(str(self.num) + '.jpg').scaled(500,500,aspectRatioMode=1))
    
    #后一张图片
    def Next(self):
        if self.num==5:
            reply = QMessageBox.information(self, "提示", '没有下一张图片', QMessageBox.Yes, QMessageBox.No)
            print(reply)
        else:
            self.num=self.num+1
            self.label_pic.setPixmap(QPixmap(str(self.num) + '.jpg').scaled(500,500,aspectRatioMode=1))



