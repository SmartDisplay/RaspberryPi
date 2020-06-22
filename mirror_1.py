import json
import sys
import threading
import urllib.request

import requests
import urllib3
import csv

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.uic.properties import QtGui
from time import sleep
import predict_point

Ui_MainWindow, QtBaseClass = uic.loadUiType("st_mirror.ui")

class MyWindow(QMainWindow):

    def TodayPoint(self, point):
        points = ""
        if point == -2:
            points = "매우 추움"
        elif point == -1:
            points = "추움"
        elif point == 0:
            points = "보통"
        elif point == 1:
            points = "더움"
        elif point == 2:
            points = "매우더움"
        return points

    def dust_check(self,dust):
        if dust == "좋음":
            return "good"
        elif dust == "보통":
            return "so"
        elif dust == "나쁨":
            return "bed"

    def weatherimage(self):
        URL = 'https://smartmirror.sewingfactory.shop/api/v1/getToday'
        response = requests.get(URL)
        print(response.content)
        json_data = json.loads(response.content)
        rain = json_data['rain']
        snow = json_data['snow']
        maxTemperature = json_data['maxTemperature']
        minTemperature = json_data['minTemperature']
        self.ui.now_temperature.setText("최대 : "+ str(maxTemperature))
        self.ui.now_temperature_maxmin.setText("최소 : "+str(minTemperature))
        dust = json_data['dust']
        detailDust = json_data['detailDust']
        self.ui.dust.setText("미세먼지 : "+ str(dust))
        self.ui.dust_ui.setText("초미세먼지 : "+str(detailDust))

        dust_string = self.dust_check(dust)
        dustdetail_string = self.dust_check(detailDust)
        dust_full = dust_string + dustdetail_string + ".png"
        print("dust_full : "+ dust_full)
        pixmap = QPixmap(dust_full)
        pixmap = pixmap.scaledToWidth(50)
        pixmap = pixmap.scaledToHeight(50)
        self.ui.mask.setPixmap(QPixmap(pixmap))

        if (rain is False and snow is False):
            pixmap = QPixmap("sun.png")
            pixmap = pixmap.scaledToWidth(150)
            pixmap = pixmap.scaledToHeight(150)
            self.ui.weather.setPixmap(pixmap)
            print("해")
        elif (rain is True and snow is False):
            pixmap = QPixmap("rain.png")
            pixmap = pixmap.scaledToWidth(150)
            pixmap = pixmap.scaledToHeight(150)
            self.ui.weather.setPixmap(QPixmap(pixmap))
            print("비")
        elif (rain is False and snow is True):
            pixmap = QPixmap("snow.png")
            pixmap = pixmap.scaledToWidth(150)
            pixmap = pixmap.scaledToHeight(150)
            self.ui.weather.setPixmap(QPixmap(pixmap))
            print("눈")
        else:
            print("모른닷")

    def monitortoken(self):
        fr = open('output.csv', 'r', encoding='utf-8', newline='')
        rdr = csv.reader(fr)
        eh = ""
        for v in rdr:
            print(v[1])
            eh = v[1]
        fr.close()
        return eh

    def userId(self):
        eh = self.monitortoken()
        if eh == "":
            URL = 'https://smartmirror.sewingfactory.shop/api/v1/getMonitorToken'
            response = requests.get(URL)
            print(str(response.content))
            f = open('oprintitutput.csv', 'w', encoding='utf-8', newline='')
            wr = csv.writer(f)
            wr.writerow([0, response.content.decode('utf-8')])
            f.close()
        params = """
                                           {
                                               "monitorToken" : """ + "\"" + eh + "\"" + """
                                               }
                                           """
        print(params)

        url = 'https://smartmirror.sewingfactory.shop/api/v1/getMonitorsUserId'
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(url=url, data=params, headers=headers)
        print("어때? : " + str(response))

        print("뭐뭐 출력해줘 : " + str(response.content.decode('utf-8')))

        if (str(response.content) is not None):
            print("값을 잘 받아올 때")
            self.ui.monitortoken.setText("일련번호 : " + eh)
            return str(response.content.decode('utf-8'))
        else:
            print("안받아올 떄")


    def monitors_infor(self):
        while True:
            print("monitor")
            eh = self.monitortoken()
            if eh == "":
                URL = 'https://smartmirror.sewingfactory.shop/api/v1/getMonitorToken'
                response = requests.get(URL)
                print(str(response.content))
                f = open('oprintitutput.csv', 'w', encoding='utf-8', newline='')
                wr = csv.writer(f)
                wr.writerow([0, response.content.decode('utf-8')])
                f.close()
            params = """
                                   {
                                       "monitorToken" : """ + "\"" + eh + "\"" + """
                                       }
                                   """
            print(params)

            url = 'https://smartmirror.sewingfactory.shop/api/v1/getMonitorsUserId'
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            response = requests.post(url=url, data=params, headers=headers)

            if (str(response.content) is not None):
                print("값을 잘 받아올 때")
                self.ui.monitortoken.setText("토큰 : " + eh)
                break
            else:
                print("안받아올 떄")
                sleep(5)


    def user_information(self):
        #유저 정보 게속 받아오기
        while True:
            monitor = self.monitortoken()
            userid = self.userId()
            if monitor == "":
                print("공백")
            else:
                print("유저정보 30초마다")

                params = """
                                {
                                    "userBlueToothAddr" : "abcdef",
                                    "monitorToken" : """ + "\"" + monitor + "\"" + """, 
                                    "userId" : """ + userid + """
                                    }
                                """

                print(params)

                url = 'https://smartmirror.sewingfactory.shop/api/v1/getWeathersSimilarFiveDaysAgo'
                headers = {'Content-Type': 'application/json; charset=utf-8'}
                response = requests.post(url=url, data=params, headers=headers)
                #print("json 값 : " + response.content())
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

                #image 지우기
                self.reset()
                for aa in range(a.__len__()):
                    urlString = a[aa]['imageUrl']
                    createdDate = a[aa]['todayTime']
                    reviewTodayPoint = a[aa]['reviewTodayPoint']
                    imageFromWeb = urllib.request.urlopen(urlString).read()
                    qPixmapVar = QPixmap()
                    qPixmapVar.loadFromData(imageFromWeb)
                    qPixmapVar = qPixmapVar.scaledToWidth(250)
                    qPixmapVar = qPixmapVar.scaledToHeight(700)

                    points = self.TodayPoint(reviewTodayPoint)
                    if aa == 0:
                        self.ui.one.setPixmap(qPixmapVar)
                        self.ui.dateEdit.setText(createdDate[0:8])
                        self.ui.point_1.setText(points)
                    elif aa == 1:
                        self.ui.two.setPixmap(qPixmapVar)
                        self.ui.dateEdit_2.setText(createdDate[0:8])
                        self.ui.point_2.setText(points)
                    elif aa == 2:
                        self.ui.three.setPixmap(qPixmapVar)
                        self.ui.dateEdit_3.setText(createdDate[0:8])
                        self.ui.point_3.setText(points)
                    elif aa == 3:
                        self.ui.four.setPixmap(qPixmapVar)
                        self.ui.dateEdit_4.setText(createdDate[0:8])
                        self.ui.point_4.setText(points)
                    elif aa == 4:
                        self.ui.five.setPixmap(qPixmapVar)
                        self.ui.dateEdit_5.setText(createdDate[0:8])
                        self.ui.point_5.setText(points)
                self.weatherimage()
            sleep(20)

    def csvfile_(self):
        self.ui.predict.setText(predict_point.will())
        #predict_point.csvfile()
        pixmap = QPixmap("foo.png")
        pixmap = pixmap.scaledToWidth(200)
        pixmap = pixmap.scaledToHeight(150)
        self.ui.grape1.setPixmap(pixmap)

    def csvfile__(self):
       # predict_point.weather_history_date_get_grape()
        pixmap = QPixmap("grape.png")
        pixmap = pixmap.scaledToWidth(200)
        pixmap = pixmap.scaledToHeight(150)
        self.ui.grape2.setPixmap(pixmap)

    def reset(self):

        qPixmapVar = QPixmap("")
        qPixmapVar = qPixmapVar.scaledToWidth(250)
        qPixmapVar = qPixmapVar.scaledToHeight(700)

        self.ui.one.setPixmap(qPixmapVar)
        self.ui.dateEdit.setText("")
        self.ui.point_1.setText("")

        self.ui.two.setPixmap(qPixmapVar)
        self.ui.dateEdit_2.setText("")
        self.ui.point_2.setText("")

        self.ui.three.setPixmap(qPixmapVar)
        self.ui.dateEdit_3.setText("")
        self.ui.point_3.setText("")

        self.ui.four.setPixmap(qPixmapVar)
        self.ui.dateEdit_4.setText("")
        self.ui.point_4.setText("")

        self.ui.five.setPixmap(qPixmapVar)
        self.ui.dateEdit_5.setText("")
        self.ui.point_5.setText("")

    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #monitor 5초마다
        thread_monitor = threading.Thread(target=self.monitors_infor)
        thread_monitor.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread_monitor.start()

        #유저정보 30초마다
        thread_userInfo = threading.Thread(target=self.user_information)
        thread_userInfo.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread_userInfo.start()

        self.csvfile_()
        self.csvfile__()



if __name__ == "__main__":
            app = QApplication(sys.argv)
            window = MyWindow()
            window.show()
            oimage = QImage("backgroundimage.png")

            palette = QPalette()
            palette.setBrush(10, QBrush(oimage))
            window.setPalette(palette)

            window.showFullScreen()
            app.exec_()