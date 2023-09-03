### 메인페이지 관련 함수

from datetime import datetime 
from datetime import timedelta
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 메인페이지 오픈공연 함수
def open_info():
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from KEYWIDB.OpenInfo limit 6")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    open = []
    for i in range(len(data)):
        id = data[i][0]
        title = data[i][1]
        url = data[i][2]
        date = data[i][4]
        image = data[i][3]
        open_info = {
            '_id' : id,
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image
        }
        open.append(open_info)
    return open

# 메인페이지 핫공연 함수
def hot_info():
    # search User in database & compare password
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select id, concat('[', category, ' ', cont_name, ' ', '와/과 유사한', ']', ' ', show_name) as title, show_url, show_date, img_url from KEYWIDB.HotInfo limit 6")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    hot = []
    for i in range(len(data)):
        id = data[i][0]
        title = data[i][1]
        url = data[i][2]
        date = data[i][3]
        image = data[i][4]
        hot_info = {
            '_id' : id,
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image
        }
        hot.append(hot_info)
    return hot

# 더보기 오픈페이지 오픈 공연 함수
def open_info_all():
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from KEYWIDB.OpenInfo")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    open = []
    for i in range(len(data)):
        id = data[i][0]
        title = data[i][1]
        url = data[i][2]
        date = data[i][4]
        image = data[i][3]
        open_info = {
            '_id' : id,
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image
        }
        open.append(open_info)
    return open

# 더보기 핫페이지 핫 공연 함수
def hot_info_all():
    # search User in database & compare password
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select id, concat('[', category, ' ', cont_name, ' ', '와/과 유사한', ']', ' ', show_name) as title, show_url, show_date, img_url from KEYWIDB.HotInfo")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    hot = []
    for i in range(len(data)):
        id = data[i][0]
        title = data[i][1]
        url = data[i][2]
        date = data[i][3]
        image = data[i][4]
        hot_info = {
            '_id' : id,
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image
        }
        hot.append(hot_info)
    return hot

# 더보기 페이지의 주차 나타내는 함수
def week_no():
    s = datetime.today().strftime("%Y-%m-%d") 
    month = datetime.today().month
    target_day = datetime.strptime(s, "%Y-%m-%d")

    firstday = target_day.replace(day=1)
    while firstday.weekday() != 0: # 1주차의 시작요일을 월요일로
      firstday += timedelta(days=1)

    if target_day < firstday: 
      return f'{month}월 0주차'

    return f'{month}월 {(target_day - firstday).days // 7 + 1}주차' 