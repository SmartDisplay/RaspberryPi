import json
import sys
import urllib.request

import requests
import urllib3
import csv

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.uic.properties import QtGui

Ui_MainWindow, QtBaseClass = uic.loadUiType("st_mirror.ui")

#requests VS urllib. ...
# 1. 데이터를 보낼때 requests는 딕셔너리 형태, urllib는 인코딩하여 바이너리 형태로 전송합니다.
# 2. requests는 요청 메소드(get, post)를 명시하지만 urllib는 데이터의 여부에 따라 get과 post 요청을 구분합니다.

class MyWindow(QMainWindow):
    def list_fun(list):
        lists = list
    def __init__(self):

        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        userBlueToothAddr = "userBlueToothAddr"
        monitorToken = "monitorToken"
        userId = 0


        URL = 'https://smartmirror.sewingfactory.shop/api/v1/getMonitorToken'
        response = requests.get(URL)
        print(str(response.content))

        f = open('output.csv', 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerow([0, response.content.decode('utf-8')])
        f.close()

        fr = open('output.csv', 'r', encoding='utf-8', newline='')
        rdr = csv.reader(fr)
        eh = ""
        for v in rdr:
            print(v[1])
            eh = v[1]
        fr.close()
        params = """
               {
                   "monitorToken" : """+ "\"" + eh +"\""+ """
                   }
               """
        url = 'https://smartmirror.sewingfactory.shop/api/v1/getMonitorsUserId'
        #토큰값있으면 실행 ㄴㄴ
        print(params)

        #원래라면 블루투스 연결하는 것을 받아와서 변수값에 넣어줘야 됨
        params = """
        {
            "userBlueToothAddr" : "abcd",
            "monitorToken" : "b706e33a", 
            "userId" : 209
            }
        """
        url = 'https://smartmirror.sewingfactory.shop/api/v1/getWeathersSimilarFiveDaysAgo'
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(url=url, data=params, headers=headers)
        print(response.json())
        a = list()
        for i in response.json():
            if i is None:
                print("None이다")
            else:
                a.append(i)
                print(i)
        print(a)
        print(a.__len__())
        print(a[0]['userName'])
        #print(url)
        for aa in range(a.__len__()):
            urlString = a[aa]['imageUrl']
            createdDate = a[aa]['todayTime']
            imageFromWeb = urllib.request.urlopen(urlString).read()
            qPixmapVar = QPixmap()
            qPixmapVar.loadFromData(imageFromWeb)
            if aa == 0:
                self.ui.one.setPixmap(qPixmapVar)
                self.ui.dateEdit.setText(createdDate[0:8])
            elif aa == 1:
                self.ui.two.setPixmap(qPixmapVar)
                self.ui.dateEdit_2.setText(createdDate[0:8])
            elif aa == 2:
                self.ui.three.setPixmap(qPixmapVar)
                self.ui.dateEdit_3.setText(createdDate[0:8])
            elif aa == 3:
                self.ui.four.setPixmap(qPixmapVar)
                self.ui.dateEdit_4.setText(createdDate[0:8])
            elif aa == 4:
                self.ui.five.setPixmap(qPixmapVar)
                self.ui.dateEdit_5.setText(createdDate[0:8])


        self.ui.weather.setText(str(response.status_code)) #이렇게 변경
        self.ui.now_temperature.setText(str(response.status_code)) #이렇게 변경

if __name__ == "__main__":
            app = QApplication(sys.argv)
            window = MyWindow()
            window.show()
            window.showFullScreen()
            app.exec_()



