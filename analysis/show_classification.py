import pandas as pd
from tqdm import tqdm
import pymysql

conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
db = conn.cursor()
try:
    cursor = conn.cursor()
    # show_name, show_summary, show_detail, show_venue, show_address, show_date, show_genre, img_url, show_url, is_review
    sql = "SELECT * FROM KEYWIDB.NewShow"
    cursor.execute(sql)
    show_result = cursor.fetchall()

finally:
    show_df = pd.DataFrame(show_result,columns=['id','제목','줄거리','작품설명','장소','주소','기간','URL','이미지URL','장르','후기유무'] )
    #show_df.drop('id', axis=1, inplace=True)
    conn.close()
    show_df = show_df[show_df['후기유무']=='X'].reset_index(drop=True)

def classificate_show(show_df):
    topic = []
    for i in tqdm(range(len(show_df))):
        content = show_df.loc[i,'줄거리']
        detail = show_df.loc[i,'작품설명']
        genre = show_df.loc[i,'장르']
        date = show_df.loc[i,'기간']
        list_1 = ['코미디','코믹','웃음','웃기','개그','유쾌']
        list_2 = ['따뜻한','감동','위로','눈물','슬픈','기억','힐링','아름']
        list_3 = ['라이브','조명','화려','연주']
        list_4 = ['내한','인기','작가','어워즈','돌아']
        list_5 = ['유명감독','탄탄','예술','소설','원작','새롭','각색'] # 스토리가 탄탄한
        list_6 = ['엄마','아빠','가족','함께','부모님','추억','친구','선물','교훈']
        list_7 = ['몰입','대사','깊다','인상','스토리','완벽','연출','감독','장면','시상','완성'] # 연출이 완벽한
        if (any(keyword in content for keyword in list_1)) or (any(keyword in detail for keyword in list_1)):
            topic.append('웃기고 유쾌한')
        elif (any(keyword in content for keyword in list_7)) or (any(keyword in detail for keyword in list_7)):
            topic.append('연출이 완벽한')
        elif (any(keyword in content for keyword in list_2)) or (any(keyword in detail for keyword in list_2)):
            topic.append('따뜻한 위로가 되는')
        elif (any(keyword in content for keyword in list_5)) or (any(keyword in detail for keyword in list_5)) or (genre=='퍼포먼스'):
            topic.append('스토리가 탄탄한')
        elif (any(keyword in content for keyword in list_6)) or (any(keyword in detail for keyword in list_6)) or (genre == '어린이/가족'):
            topic.append('함께 보기 좋은')
        elif (any(keyword in content for keyword in list_4)) or (any(keyword in detail for keyword in list_4)) or (genre=='라이선스') or ("오픈런" in date):
            topic.append('손꼽아 기다려지는')
        elif (any(keyword in content for keyword in list_3)) or (any(keyword in detail for keyword in list_3)) or (genre in ['클래식','오페라','콘서트']):
            topic.append('음악과 함께하는')
        else:
            topic.append(' ')
    return topic

show_df['topic'] = classificate_show(show_df)
print(show_df['topic'].value_counts())
# DB에 올리기
conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
# 커서 생성
db = conn.cursor()
# 쿼리 실행
for name,date,place,address,image_url,detail_url,topic,id in tqdm(zip(show_df['제목'],show_df['기간'],show_df['장소'],show_df['주소'],show_df['이미지URL'],
                                                                      show_df['URL'],show_df['topic'],show_df['id'])):
    sql_state = """INSERT INTO KEYWIDB.ShowInfo(name,date,place,address,image_url,detail_url,topic,id) 
                VALUES ("%s","%s","%s", "%s", "%s", "%s", "%s", "%s")"""%(tuple([name,date,place,address,image_url,detail_url,topic,id]))
    db.execute(sql_state)

conn.commit()
conn.close()
