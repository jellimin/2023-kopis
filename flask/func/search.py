# ShowInfo 테이블에서 키워드별 공연 정보 가져오기기
import pandas as pd
import pymysql
import numpy as np

conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
try:
    cursor = conn.cursor()
    sql = "SELECT id,name,date,place,address,image_url,detail_url,topic FROM KEYWIDB.ShowInfo"
    cursor.execute(sql)
    result = cursor.fetchall()
    search_data = []
    for record in result:
        search_data.append(record)
    
finally:
    df = pd.DataFrame(search_data)
    df.columns = ['아이디', '제목', '기간', '공연장명', '주소', '이미지url', '상세url', 'topic']
    conn.close()

def uniq_keyword():
    global df
    uni_keyword_list = ['함께 보기 좋은', '연출이 완벽한',  '웃기고 유쾌한', '손꼽아 기다려지는', '따뜻한 위로가 되는', '스토리가 탄탄한', '음악과 함께하는']
    uni_keyword = np.array(uni_keyword_list)
    keyword = []
    for i in range(len(uni_keyword)):
        keyw = {'keyword' : uni_keyword[i],
                'url' : "keyword" + str(i+1)}
        keyword.append(keyw)
    return keyword

def search_keyword1_6():
    global df
    search_df = df[df['topic'] == '함께 보기 좋은'][:6]
    search_df = search_df.reset_index(drop=True)
    keyword1_6 = []
    for i in range(len(search_df)):
        id = search_df.loc[i, '아이디']
        title = search_df.loc[i, '제목']
        date = search_df.loc[i, '기간']
        image = search_df.loc[i, '이미지url']
        url = search_df.loc[i, '상세url']
        place = search_df.loc[i, '공연장명']
        address = search_df.loc[i, '주소']
        search_info = {
            '_id' : id,
            'title' : title,
            'date' : date,
            'image' : image,
            'url' : url,
            'place' : place,
            'address' : address
        }
        keyword1_6.append(search_info)
    return keyword1_6

def search_keyword2_6():
    global df
    search_df = df[df['topic'] == '연출이 완벽한'][:6]
    search_df = search_df.reset_index(drop=True)
    keyword2_6 = []
    for i in range(len(search_df)):
        id = search_df.loc[i, '아이디']
        title = search_df.loc[i, '제목']
        date = search_df.loc[i, '기간']
        image = search_df.loc[i, '이미지url']
        url = search_df.loc[i, '상세url']
        place = search_df.loc[i, '공연장명']
        address = search_df.loc[i, '주소']
        search_info = {
            '_id' : id,
            'title' : title,
            'date' : date,
            'image' : image,
            'url' : url,
            'place' : place,
            'address' : address
        }
        keyword2_6.append(search_info)
    return keyword2_6

def search_keyword3_6():
    global df
    search_df = df[df['topic'] == '웃기고 유쾌한'][:6]
    search_df = search_df.reset_index(drop=True)
    keyword3_6 = []
    for i in range(len(search_df)):
        id = search_df.loc[i, '아이디']
        title = search_df.loc[i, '제목']
        date = search_df.loc[i, '기간']
        image = search_df.loc[i, '이미지url']
        url = search_df.loc[i, '상세url']
        place = search_df.loc[i, '공연장명']
        address = search_df.loc[i, '주소']
        search_info = {
            '_id' : id,
            'title' : title,
            'date' : date,
            'image' : image,
            'url' : url,
            'place' : place,
            'address' : address
        }
        keyword3_6.append(search_info)
    return keyword3_6

def search_keyword4_6():
    global df
    search_df = df[df['topic'] == '손꼽아 기다려지는'][:6]
    search_df = search_df.reset_index(drop=True)
    keyword4_6 = []
    for i in range(len(search_df)):
        id = search_df.loc[i, '아이디']
        title = search_df.loc[i, '제목']
        date = search_df.loc[i, '기간']
        image = search_df.loc[i, '이미지url']
        url = search_df.loc[i, '상세url']
        place = search_df.loc[i, '공연장명']
        address = search_df.loc[i, '주소']
        search_info = {
            '_id' : id,
            'title' : title,
            'date' : date,
            'image' : image,
            'url' : url,
            'place' : place,
            'address' : address
        }
        keyword4_6.append(search_info)
    return keyword4_6

def search_keyword5_6():
    global df
    search_df = df[df['topic'] == '따뜻한 위로가 되는'][:6]
    search_df = search_df.reset_index(drop=True)
    keyword5_6 = []
    for i in range(len(search_df)):
        id = search_df.loc[i, '아이디']
        title = search_df.loc[i, '제목']
        date = search_df.loc[i, '기간']
        image = search_df.loc[i, '이미지url']
        url = search_df.loc[i, '상세url']
        place = search_df.loc[i, '공연장명']
        address = search_df.loc[i, '주소']
        search_info = {
            '_id' : id,
            'title' : title,
            'date' : date,
            'image' : image,
            'url' : url,
            'place' : place,
            'address' : address
        }
        keyword5_6.append(search_info)
    return keyword5_6

def search_keyword6_6():
    global df
    search_df = df[df['topic'] == '스토리가 탄탄한'][:6]
    search_df = search_df.reset_index(drop=True)
    keyword6_6 = []
    for i in range(len(search_df)):
        id = search_df.loc[i, '아이디']
        title = search_df.loc[i, '제목']
        date = search_df.loc[i, '기간']
        image = search_df.loc[i, '이미지url']
        url = search_df.loc[i, '상세url']
        place = search_df.loc[i, '공연장명']
        address = search_df.loc[i, '주소']
        search_info = {
            '_id' : id,
            'title' : title,
            'date' : date,
            'image' : image,
            'url' : url,
            'place' : place,
            'address' : address
        }
        keyword6_6.append(search_info)
    return keyword6_6

def search_keyword7_6():
    global df
    search_df = df[df['topic'] == '음악과 함께하는'][:6]
    search_df = search_df.reset_index(drop=True)
    keyword7_6 = []
    for i in range(len(search_df)):
        id = search_df.loc[i, '아이디']
        title = search_df.loc[i, '제목']
        date = search_df.loc[i, '기간']
        image = search_df.loc[i, '이미지url']
        url = search_df.loc[i, '상세url']
        place = search_df.loc[i, '공연장명']
        address = search_df.loc[i, '주소']
        search_info = {
            '_id' : id,
            'title' : title,
            'date' : date,
            'image' : image,
            'url' : url,
            'place' : place,
            'address' : address
        }
        keyword7_6.append(search_info)
    return keyword7_6
