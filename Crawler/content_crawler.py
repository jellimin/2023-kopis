from content_code import ContentCrawler
import pymysql

crawler = ContentCrawler()
movie_df = crawler.get_movie_detail()
drama_df = crawler.get_drama_info()
ent_df = crawler.get_entertain_info()

conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
# 커서 생성
#db = conn.cursor()
# 쿼리 실행
# sql_state = """DELETE FROM KEYWIDB.MovieGenre"""
# db.execute(sql_state)
# sql_state = """ALTER TABLE KEYWIDB.MovieGenre AUTO_INCREMENT = 1"""
# db.execute(sql_state)
# sql_state = "DELETE FROM KEYWIDB.Movie"
# sql_state = """ALTER TABLE KEYWIDB.Movie AUTO_INCREMENT = 1"""
# db.execute(sql_state)
# db.execute(sql_state)
# for genre,name,summary,url in zip(movie_df['장르'],movie_df['제목'],movie_df['줄거리'],movie_df['URL']):
#     sql_state = """INSERT INTO KEYWIDB.MovieGenre(genre_name)
#                 VALUES ("%s")"""%(tuple([genre]))
#     db.execute(sql_state)
#     sql_state = """INSERT INTO KEYWIDB.Movie(mv_name,mv_cont,mv_url) 
#                 VALUES ("%s", "%s", "%s")"""%(tuple([name, summary, url]))
#     db.execute(sql_state)
# sql_state = """DELETE FROM KEYWIDB.Drama"""
# db.execute(sql_state)
# sql_state = """ALTER TABLE KEYWIDB.Drama AUTO_INCREMENT = 1"""
# db.execute(sql_state)
# for name,summary,url in zip(drama_df['제목'],drama_df['줄거리'],drama_df['URL']):
#     sql_state = """INSERT INTO KEYWIDB.Drama(dr_name,dr_cont,dr_url) 
#                 VALUES ("%s", "%s", "%s")"""%(tuple([name, summary, url]))
# #     db.execute(sql_state)
# sql_state = """DELETE FROM KEYWIDB.Entertain"""
# db.execute(sql_state)
# sql_state = """ALTER TABLE KEYWIDB.Entertain AUTO_INCREMENT = 1"""
# db.execute(sql_state)
# sql_state = """DELETE FROM KEYWIDB.EntertainCrew"""
# db.execute(sql_state)
# sql_state = """ALTER TABLE KEYWIDB.EntertainCrew AUTO_INCREMENT = 1"""
# db.execute(sql_state)

# for name,num,date,crew in zip(ent_df['제목'],ent_df['회차정보'],ent_df['방영날짜'],ent_df['출연진']):
#     sql_state = """INSERT INTO KEYWIDB.Entertain(et_name,et_num,et_date) 
#                 VALUES ("%s", "%s", "%s")"""%(tuple([name, num, date]))
#     db.execute(sql_state)
#     sql_state = """INSERT INTO KEYWIDB.EntertainCrew(cr_name)
#                 VALUES ("%s")"""%(tuple([crew]))
#     db.execute(sql_state)
    

# conn.commit()
# # 연결 종료
# conn.close()