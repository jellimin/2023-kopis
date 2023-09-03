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
    show_df = pd.DataFrame(show_result,columns=['id','제목','줄거리','작품설명','장소','주소','기간','장르','이미지URL','URL', '후기유무'] )
    show_df.drop('id', axis=1, inplace=True)
    conn.close()


