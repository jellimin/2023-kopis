### 메인페이지 오픈 정보 관련 함수

import pandas as pd
<<<<<<< HEAD
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def open_info():
    # search User in database & compare password
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from KEYWIDB.OpenInfo limit 8")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

=======
path = 'C:/Users/alsru/Desktop/Project/Flask_git/2023-kopis/flask/website/data/interpark_open_data.csv'
def open_info():

    df = pd.read_csv(path)
    df = df.loc[:5, ['제목', 'URL', '티켓오픈일시', '이미지URL']]
>>>>>>> c67feb001b0120fe490ce3cf484a2d2f815c99a1
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

def open_info_all():
    # search User in database & compare password
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

from datetime import datetime 
from datetime import timedelta

def week_no():
    s = datetime.today().strftime("%Y-%m-%d") 
    month = datetime.today().month
    target_day = datetime.strptime(s, "%Y-%m-%d")

    firstday = target_day.replace(day=1)
    while firstday.weekday() != 0: 
      firstday += timedelta(days=1)

    if target_day < firstday: 
      return 0

    return f'{month}월 {(target_day - firstday).days // 7 + 1}주차' 