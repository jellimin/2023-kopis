from openfold.open import OpenCrawler
import pandas as pd
import pymysql

crawler = OpenCrawler()
interpark_df = crawler.Interpark("http://ticket.interpark.com/webzine/paper/TPNoticeList.asp?tid1=in_scroll&tid2=ticketopen&tid3=board_main&tid4=board_main")
yes24_df = crawler.Yes24("http://ticket.yes24.com/")
ticketlink_df = crawler.Ticketlink("https://www.ticketlink.co.kr/help/notice#TICKET_OPEN")

open_df = pd.concat([interpark_df, yes24_df, ticketlink_df], axis = 0)

conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')

# 커서 생성
db = conn.cursor()
# 쿼리 실행
for name, url, image_url, date, in zip(open_df['제목'],open_df['URL'],open_df['이미지URL'],open_df['티켓오픈일시']):
    sql_state = """INSERT INTO KEYWIDB.OpenInfo(name, detail_url, image_url, open_date) 
                VALUES ("%s", "%s", "%s", "%s")"""%(tuple([name, url, image_url, date]))
    db.execute(sql_state)
conn.commit()
# 연결 종료
conn.close()