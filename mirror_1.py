import matplotlib.pyplot as plt
import mysql as mysql
import numpy as np
import pandas as pd

from mysql.connector import Error

##필요 -> ##
from datetime import datetime

def today_datetime_tem():
    today_datetime = datetime.today().strftime("%Y%m%d")    # YYYYmmddHHMMSS 형태
    print(today_datetime)

    try:
        #connection = mysql.connector.connect(host='34.64.124.92',
        #                                     database='smartmirror',
        #                                     user='smartmirror',
        #                                     password='smartmirror9699!!')
        connection = mysql.connector.connect(host='smartmirror.sewingfactory.shop',
                                             database='smartmirror',
                                             user='smartmirror',
                                             password='q1w2e3r4!!')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            query = f"select * from weather_history where date_time like '{today_datetime}';"
            cursor.execute(query)
            # record = cursor.fetchone()
            record = cursor.fetchall()
            # print("You're connected to database: ", record)
            size = record.__sizeof__()
            datatype = record.__class__
            attr = ['date_time', 'created_date', 'modified_date', 'area', 'aver_temperature',
                    'max_temperature','min_temperature', 'mm', 'rain','snow','sensory_temperature',
                    'detail_dust', 'dust']
            df = pd.DataFrame(data = record ,columns=attr)
            print("평균 기온")
            print(df['aver_temperature']) #평균 기온
            return df['aver_temperature']
            print(df)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def will():

    try:
        connection = mysql.connector.connect(host='smartmirror.sewingfactory.shop',
                                             database='smartmirror',
                                             user='smartmirror',
                                             password='q1w2e3r4!!')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            aver_tem_p = int(today_datetime_tem() + 3)
            aver_tem_m = int(today_datetime_tem() - 3)
            query = f"select weather_history.date_time, weather_history.min_temperature, weather_history.max_temperature, weather_history.aver_temperature ,review_today.user_name, review_today.review_today_point from weather_history left join review_today on weather_history.date_time = review_today.today_time where weather_history.aver_temperature >= {aver_tem_m} and weather_history.aver_temperature <= {aver_tem_p};"
            cursor.execute(query)
            record = cursor.fetchall()
            size = record.__sizeof__()
            datatype = record.__class__
            attr = ['date_time', 'min_temperature', 'max_temperature', 'aver_temperature', 'user_name',
                    'review_today_point']
            df = pd.DataFrame(data=record, columns=attr)
            # 사용자의 이름 필요
            # 사용자가 비슷한 온도에 point한 것들 필요
            # 그 point가 각각 몇 개 있는지 구하기
            # 가장 비율이 높은 것 찾기
            # 그 비율이 높은 것으로 오늘 point 예측

            point_value = dict()

            point_value["cold"] = len(df[(df.review_today_point == -2) & (df.user_name == 'testkimgood')])
            point_value["cool"] = len(df[(df.review_today_point == -1) & (df.user_name == 'testkimgood')])
            point_value["normal"] = len(df[(df.review_today_point == 0) & (df.user_name == 'testkimgood')])
            point_value["warm"] = len(df[(df.review_today_point == 1) & (df.user_name == 'testkimgood')])
            point_value["hot"] = len(df[(df.review_today_point == 2) & (df.user_name == 'testkimgood')])

            max_key = list(point_value.keys())[list(point_value.values()).index(max(point_value.values()))]

            today_datetime = datetime.today().strftime("%Y%m%d")  # YYYYmmddHHMMSS 형태
            today_datetimes = int(today_datetime[4:6])
            print("월 : " + str(today_datetimes))
            today_mon = ""
            if (today_datetimes>=3 and today_datetimes<=5 and max_key == "cold"): #봄
                today_mon += "추움이라"
            elif (today_datetimes>=3 and today_datetimes<=5 and max_key == "hot"): #봄
                today_mon += "더움이라"
            elif (today_datetimes>=6 and today_datetimes<=8 and max_key == "hot"): #봄
                today_mon += "매우 더움이라"
            elif (today_datetimes>=6 and today_datetimes<=8 and max_key == "hot"): #봄
                today_mon += "덜 더움이라"
            elif (today_datetimes>=9 and today_datetimes<=11 and max_key == "normal"): #봄
                today_mon += "약간 더움이라"
            elif (today_datetimes>=9 and today_datetimes<=11 and max_key == "hot"): #봄
                today_mon += "견딜만한 더움이라"
            elif (today_datetimes>=9 and today_datetimes<=11 and max_key == "cool"): #봄
                today_mon += "약간 추움이라"
            elif ((today_datetimes==12 or today_datetimes==1 or today_datetimes==2)  and max_key == "cold"): #봄
                today_mon += "매우 추움이라"
            elif ((today_datetimes==12 or today_datetimes==1 or today_datetimes==2)  and max_key == "normal"): #봄
                today_mon += "따뜻함이라."
            elif ((today_datetimes==12 or today_datetimes==1 or today_datetimes==2)  and max_key == "cool"): #봄
                today_mon += "견딜만한 추움이라."
            result = "오늘은 " +max_key +" 이라 " + today_mon + "\n" + "느낄거라고 예상됩니다."
            return result


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def csvfile():
    try:
        connection = mysql.connector.connect(host='34.64.124.92',
                                             database='smartmirror',
                                             user='smartmirror',
                                             password='smartmirror9699!!')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select * from review_today;")
            # record = cursor.fetchone()
            record = cursor.fetchall()
            # print("You're connected to database: ", record)
            size = record.__sizeof__()
            datatype = record.__class__
            attr = ['review_today_id', 'created_date', 'image_url', 'review_today_point', 'today_time', 'user_id',
                    'user_name', 'modified_date']
            df = pd.DataFrame(data=record, columns=attr)
            df.to_csv('review_today.csv')

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            csv_pngfile()

def csv_pngfile():
    #import csv
    # 전체 유저가 그날 어떤 감정을 느꼈는지 나타내주는 값들 다 더해주고 평균내고 하자
    df = pd.read_csv('review_today.csv')
    newrow = []
    hot = 0
    warm = 0
    normal = 0
    cool = 0
    cold = 0
    sum = 0
    date_list = set(df['today_time'].sort_values(ascending=True))
    date_list = sorted(date_list)
    print(date_list)
    for i in date_list:
        dayNumericalStatement = df[df['today_time'] == i]
        # print("오늘의 리뷰 개수 " + str(dayNumericalStatement.__len__()))
        hot = dayNumericalStatement[dayNumericalStatement['review_today_point'] == 2].__len__()
        warm = dayNumericalStatement[dayNumericalStatement['review_today_point'] == 1].__len__()
        normal = dayNumericalStatement[dayNumericalStatement['review_today_point'] == 0].__len__()
        cool = dayNumericalStatement[dayNumericalStatement['review_today_point'] == -1].__len__()
        cold = dayNumericalStatement[dayNumericalStatement['review_today_point'] == -2].__len__()
        sum = hot
        newrow.append(np.asarray([i, int(sum)]))

    X = np.asanyarray(newrow)
    plt.xlabel("2020 02 ~ 2020 06")
    plt.ylabel("Very Hot")
    plt.title("Very Hot")
    plt.scatter(X[:, 0], X[:, 1])
    plt.savefig('foo.png', bbox_inches='tight')



def weather_history_date_get():
    try:
        connection = mysql.connector.connect(host='34.64.124.92',
                                             database='smartmirror',
                                             user='smartmirror',
                                             password='smartmirror9699!!')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            # 요기 수정

            cursor.execute("select * from users_feeling_percentage;")
            # cursor.execute(query)
            # record = cursor.fetchone()
            record = cursor.fetchall()
            size = record.__sizeof__()
            datatype = record.__class__
            # attr = ['date_time', 'created_date', 'area', 'aver_temperature', 'min_temperature', 'max_temperature',
            #        'mm', 'rain','snow','sensory_temperature','modified_date','detail_dust','dust']
            attr = ['date_time', 'created_date', 'modified_date', 'cold', 'cool', 'normal', 'warm', 'hot']

            df = pd.DataFrame(data=record, columns=attr)
            print(df)
            df.to_csv('weather_history_date_get.csv')

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def weather_history_date_get_grape():
    weather_history_date_get()
    # csv 파일 읽기
    file3 = 'C:\\Users\\kimbh\\weather_history_date_get.csv'
    df3 = pd.read_csv(file3)

    print(df3)

    # plt.plot(list_predicted_date, list_predicted_point)
    plt.plot(df3['date_time'], df3['cold'])
    plt.plot(df3['date_time'], df3['cool'])
    plt.plot(df3['date_time'], df3['normal'])
    plt.plot(df3['date_time'], df3['warm'])
    plt.plot(df3['date_time'], df3['hot'])
    # X=np.array(list_predicted_kMeans)
    # plt.scatter(X[:,0],X[:,1])
    plt.savefig('grape.png', bbox_inches='tight')
