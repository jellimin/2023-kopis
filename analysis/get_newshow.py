import pymysql
import pandas as pd
from tqdm import tqdm
df_topic = pd.read_csv('C:/Users/alsru/Desktop/Project/Flask_git/2023-kopis/analysis/data/현재공연중_후기유무열_추가.csv')
conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
# 커서 생성
def prepro_df(df):    
    df = df.apply(lambda x: x.replace("'",""))
    df = df.apply(lambda x: x.replace('"',""))
    df = df.apply(lambda x: x.replace('',""))       
    return df
df_topic['줄거리'] = prepro_df(df_topic['줄거리'] )
df_topic['작품설명'] = prepro_df(df_topic['작품설명'] )
db = conn.cursor()
# 쿼리 실행
sql_state = """DELETE FROM KEYWIDB.NewShow"""
db.execute(sql_state)
# 제목,장소,주소,기간,이미지url,상세url,세부장르,후기유무,줄거리,작품설명
for show_name,show_summary,show_detail,show_venue,show_address,show_date,show_url,img_url,show_genre,is_review in zip(df_topic['제목'],df_topic['줄거리'],df_topic['작품설명'],df_topic['장소'],df_topic['주소'],
                                                                 df_topic['기간'],df_topic['상세url'],df_topic['이미지url'],df_topic['세부장르'],df_topic['후기유무']):
    sql_state = """INSERT INTO KEYWIDB.NewShow(show_name,show_summary,show_detail,show_venue,show_address,show_date,show_url,img_url,show_genre,is_review)
                VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""%(tuple([show_name,show_summary,show_detail,show_venue,show_address,show_date,show_url,img_url,show_genre,is_review]))
    db.execute(sql_state)

conn.commit()
# 연결 종료
conn.close()