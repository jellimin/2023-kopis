import pandas as pd
import pymysql
import numpy as np

conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
try:
    cursor = conn.cursor()
    sql = "SELECT show_id, name,date,place,address,image_url,detail_url,topic FROM KEYWIDB.ShowInfo"
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
    uni = df['topic'].unique()
    uni_keyword_list = list(uni)
    uni_keyword_list.remove(' ')
    uni_keyword = np.array(uni_keyword_list)
    keyword = []
    for i in range(len(uni_keyword)):
        keyw = {'keyword' : uni_keyword[i],
                'url' : "keyword" + str(i+1)}
        keyword.append(keyw)
    return keyword

def search_keyword1_6():
    global df
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[0]][:6]
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
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[1]][:6]
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
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[2]][:6]
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
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[3]][:6]
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
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[4]][:6]
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
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[5]][:6]
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

def search_keyword1():
    global df
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[0]]
    search_df = search_df.reset_index(drop=True)
    keyword1 = []
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
        keyword1.append(search_info)
    return keyword1

def search_keyword2():
    global df
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[1]]
    search_df = search_df.reset_index(drop=True)
    keyword2 = []
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
        keyword2.append(search_info)
    return keyword2

def search_keyword3():
    global df
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[2]]
    search_df = search_df.reset_index(drop=True)
    keyword3 = []
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
        keyword3.append(search_info)
    return keyword3

def search_keyword4():
    global df
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[3]]
    search_df = search_df.reset_index(drop=True)
    keyword4 = []
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
        keyword4.append(search_info)
    return keyword4

def search_keyword5():
    global df
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[4]]
    search_df = search_df.reset_index(drop=True)
    keyword5 = []
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
        keyword5.append(search_info)
    return keyword5

def search_keyword6():
    global df
    uniq = df['topic'].unique()
    uni_keyword_list = list(uniq)
    uni_keyword_list.remove(' ')
    uniq_keyword = np.array(uni_keyword_list)
    search_df = df[df['topic'] == uniq_keyword[5]]
    search_df = search_df.reset_index(drop=True)
    keyword6 = []
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
        keyword6.append(search_info)
    return keyword6