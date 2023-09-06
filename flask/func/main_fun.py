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
    cursor.execute("SELECT show_id, cont_num, concat('[', category, ' ', cont_name, ' ', '와/과 유사한', ']') as cont_name, show_name as title, show_url, show_date, img_url, show_address, show_venue FROM KEYWIDB.HotInfo GROUP BY cont_num HAVING max(simm) LIMIT 6")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    hot = []
    for i in range(len(data)):
        show_id = data[i][0]
        cont_num = data[i][1]
        cont_name = data[i][2]
        title = data[i][3]
        url = data[i][4]
        date = data[i][5]
        image = data[i][6]
        address = data[i][7]
        venue = data[i][8]
        hot_info = {
            '_id' : show_id,
            'num' : cont_num,
            'name' : cont_name,
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image,
            'address' : address,
            'place' : venue
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
    cursor.execute("select show_id, concat('[', category, ' ', cont_name, ' ', '와/과 유사한', ']')as cont_name, show_name as title, show_url, show_date, img_url, show_address, show_venue from KEYWIDB.HotInfo")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    hot = []
    for i in range(len(data)):
        show_id = data[i][0]
        cont_name = data[i][1]
        title = data[i][2]
        url = data[i][3]
        date = data[i][4]
        image = data[i][5]
        address = data[i][6]
        venue = data[i][7]
        hot_info = {
            '_id' : show_id,
            'name': cont_name,
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image,
            'address' : address,
            'place' : venue
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


# 큐레이션 페이지 함수
def curation_content1():
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from KEYWIDB.CurationContent where 구분 = '공연정보' LIMIT 4")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    curation1 = []
    for i in range(len(data)):
        cate = data[i][0]
        cura_url = data[i][1]
        cura_title = data[i][2]
        cura_image = data[i][3]
        curation_info1 = {
            'cate' : cate,
            'url': cura_url,
            'title' : cura_title,
            'image' : cura_image,
        }
        curation1.append(curation_info1)
    return curation1
def curation_content2():
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from KEYWIDB.CurationContent where 구분 = '플레이리스트' LIMIT 4")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    curation2 = []
    for i in range(len(data)):
        cate = data[i][0]
        cura_url = data[i][1]
        cura_title = data[i][2]
        cura_image = data[i][3]
        curation_info2 = {
            'cate' : cate,
            'url': cura_url,
            'title' : cura_title,
            'image' : cura_image,
        }
        curation2.append(curation_info2)
    return curation2
def curation_content3():
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from KEYWIDB.CurationContent where 구분 = '공연소개' LIMIT 4")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    curation3 = []
    for i in range(len(data)):
        cate = data[i][0]
        cura_url = data[i][1]
        cura_title = data[i][2]
        cura_image = data[i][3]
        curation_info3 = {
            'cate' : cate,
            'url': cura_url,
            'title' : cura_title,
            'image' : cura_image,
        }
        curation3.append(curation_info3)
    return curation3