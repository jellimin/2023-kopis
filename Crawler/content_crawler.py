from content_code import ContentCrawler, PerformCrawler
import pymysql
import tqdm

crawler_content = ContentCrawler()
crawler_perform = PerformCrawler()
movie_df = crawler_content.get_movie_detail()
drama_df = crawler_content.get_drama_detail()
ent_df = crawler_content.get_entertain_info()

review_df,simm_df = crawler_perform.get_perform_contents()
review_df['text'] = review_df['text'].apply(lambda x: x.replace("'",""))
review_df['text'] = review_df['text'].apply(lambda x: x.replace('"'),"")
review_df['text'] = review_df['text'].apply(lambda x: x.replace('\n'),"")

review_df.to_csv('C:/Users/alsru/Desktop/Project/Flask_git/2023-kopis/analysis/data/Review.csv', index=False)
simm_df.to_csv('C:/Users/alsru/Desktop/Project/Flask_git/2023-kopis/analysis/data/Simm.csv', index=False)


def update_DB():
    conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
    # 커서 생성
    db = conn.cursor()
    # 쿼리 실행
    sql_state = """DELETE FROM KEYWIDB.MovieGenre"""
    db.execute(sql_state)
    sql_state = """ALTER TABLE KEYWIDB.MovieGenre AUTO_INCREMENT = 1"""
    db.execute(sql_state)
    sql_state = "DELETE FROM KEYWIDB.Movie"
    db.execute(sql_state)
    sql_state = """ALTER TABLE KEYWIDB.Movie AUTO_INCREMENT = 1"""
    db.execute(sql_state)

    for genre,name,summary,url in zip(movie_df['장르'],movie_df['제목'],movie_df['줄거리'],movie_df['URL']):
        sql_state = """INSERT INTO KEYWIDB.MovieGenre(genre_name)
                    VALUES ("%s")"""%(tuple([genre]))
        db.execute(sql_state)
        sql_state = """INSERT INTO KEYWIDB.Movie(mv_name,mv_cont,mv_url) 
                    VALUES ("%s", "%s", "%s")"""%(tuple([name, summary, url]))
        db.execute(sql_state)
    sql_state = """DELETE FROM KEYWIDB.Drama"""
    db.execute(sql_state)
    sql_state = """ALTER TABLE KEYWIDB.Drama AUTO_INCREMENT = 1"""
    db.execute(sql_state)
    for name,summary,url in zip(drama_df['제목'],drama_df['줄거리'],drama_df['URL']):
        sql_state = """INSERT INTO KEYWIDB.Drama(dr_name,dr_cont,dr_url) 
                    VALUES ("%s", "%s", "%s")"""%(tuple([name, summary, url]))
        db.execute(sql_state)
    sql_state = """DELETE FROM KEYWIDB.Entertain"""
    db.execute(sql_state)
    sql_state = """ALTER TABLE KEYWIDB.Entertain AUTO_INCREMENT = 1"""
    db.execute(sql_state)
    sql_state = """DELETE FROM KEYWIDB.EntertainCrew"""
    db.execute(sql_state)
    sql_state = """ALTER TABLE KEYWIDB.EntertainCrew AUTO_INCREMENT = 1"""
    db.execute(sql_state)

    for name,num,date,crew in zip(ent_df['제목'],ent_df['회차'],ent_df['날짜'],ent_df['출연진']):
        sql_state = """INSERT INTO KEYWIDB.Entertain(et_name,et_num,et_date) 
                    VALUES ("%s", "%s", "%s")"""%(tuple([name, num, date]))
        db.execute(sql_state)
        sql_state = """INSERT INTO KEYWIDB.EntertainCrew(cr_name)
                    VALUES ("%s")"""%(tuple([crew]))
        db.execute(sql_state)

    sql_state = """DELETE FROM KEYWIDB.ShowReview"""
    db.execute(sql_state)
    sql_state = """ALTER TABLE KEYWIDB.ShowReview AUTO_INCREMENT = 1"""
    db.execute(sql_state)
    review_df['text'] 
    for show_name, rating, review, show_url, is_review in tqdm(zip(review_df['제목'],review_df['rating'],review_df['text'],review_df['상세URL'],review_df['후기유무'])):
        sql_state = """INSERT INTO KEYWIDB.ShowReview(show_name, rating, review, show_url, is_review) 
                    VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""%(tuple([show_name, rating, review, show_url, is_review ]))
        db.execute(sql_state)

    sql_state = """DELETE FROM KEYWIDB.NewShow"""
    db.execute(sql_state)
    sql_state = """ALTER TABLE KEYWIDB.NewShow AUTO_INCREMENT = 1"""
    db.execute(sql_state)
    for show_name, show_summary, show_detail, show_venue, show_address, show_date, show_genre, show_url, img_url, is_review in tqdm(zip(simm_df['제목'],simm_df['줄거리'],simm_df['작품설명'],simm_df['장소'],simm_df['주소'],simm_df['기간']
                                                                                    ,simm_df['이미지url'],simm_df['상세url'],simm_df['세부장르'],simm_df['후기유무'])):
        sql_state = """INSERT INTO KEYWIDB.NewShow(show_name, show_summary, show_detail,show_venue, show_address, show_date, show_genre, show_url, img_url, is_review) 
                VALUES ("%s", "%s", "%s","%s", "%s", "%s", "%s", "%s", "%s", "%s")"""%(tuple([show_name, show_summary, show_detail, show_venue, show_address, show_date, show_genre, show_url, img_url, is_review ]))
        db.execute(sql_state)

        
    ContentCrawler.send_message({'content':'DB업데이트를 완료했습니다.'})

    conn.commit()
    # 연결 종료
    conn.close()

update_DB()
