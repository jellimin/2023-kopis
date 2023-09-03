# 패키지 불러오기
import pandas as pd
import numpy as np
import re # 정규표현식
from tqdm import tqdm
from konlpy.tag import Okt # 형태소분석
from hanspell import spell_checker # 맞춤법 + 띄어쓰기
from collections import Counter
import pymysql
from datetime import timedelta
from datetime import datetime

# MYSQL에서 데이터 가져오기
conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
try:
    cursor = conn.cursor()
    sql = "SELECT mv_name,mv_cont FROM KEYWIDB.Movie"
    cursor.execute(sql)
    movie_result = cursor.fetchall()

    sql = "SELECT dr_name,dr_cont FROM KEYWIDB.Drama"
    cursor.execute(sql)
    drama_result = cursor.fetchall()
    # show_name, rating, review, show_venue, show_address, show_date, img_url, show_url, show_genre, is_review
    # ['제목','장르','줄거리','작품설명','기간','장소','url','이미지url']
    sql = "SELECT show_name, show_summary, show_detail, show_venue, show_address, show_date, img_url, show_url, is_review FROM KEYWIDB.NewShow"
    cursor.execute(sql)
    show_result = cursor.fetchall()

finally:
    movie_df = pd.DataFrame(movie_result,columns = ['제목','content'])
    drama_df = pd.DataFrame(drama_result,columns = ['제목','content'])
    show_df = pd.DataFrame(show_result,columns=['제목','줄거리','작품설명','장소','주소','기간','이미지url','url','후기유무'] )
    conn.close()

# 전처리 함수 정의
def replace_cont(show_df):
    
    content = []
    for i in range(0,show_df.shape[0]):
        row = show_df.iloc[i]
        if (row.줄거리 == '줄거리 없음') & (row.작품설명 == '작품설명 없음'): # 줄거리, 작품설명 둘 다 없는 경우
            content.append(' ')  # 공백
        elif row.줄거리 == '줄거리 없음': # 줄거리만 없는 경우
            content.append(row.작품설명)
        elif row.작품설명 == '작품설명 없음': # 작품설명만 없는 경우
            content.append(row.줄거리)
        else: # 둘 다 있는 경우 - 줄거리 사용
            content.append(row.줄거리)
    show_df['content'] = content
    #show_df.to_csv('./Keywi/Modeling/data/total_show_df.csv', index=False)
    return show_df

# 중복데이터 제거
def duplicate_drop(df):
    duplicate_drop_df = df.drop_duplicates()
    duplicate_drop_df.reset_index(drop = True, inplace = True)
    #print('중복되는 데이터 개수 확인 (제거 전):', df.duplicated().sum())
    #print('중복되는 데이터 개수 확인 (제거 후):', duplicate_drop_df.duplicated().sum())
    return duplicate_drop_df

# 한글, 영어, 숫자표현만 남기기
def extract_word(text):
    hangul = re.compile('[^a-zA-Z0-9가-힣]')
    result = hangul.sub(' ', text)
    return result

# 맞춤법 교정
def grammar_correction(df):
    tmp = df.copy()
    error_idx = []
    for i, res in enumerate(tqdm(tmp['content'])):
        if len(res) > 500: # 텍스트 길이가 500보다 클 때
            # 결과값
            res = ''
            # 반복 횟수 구하기
            if len(tmp.loc[i, 'content']) % 500 == 0:
                iter = len(tmp.loc[i, 'content']) // 500
            else:
                iter = len(tmp.loc[i, 'content']) // 500 + 1
            for i in range(iter):
                if i < (iter-1):
                    res += spell_checker.check(tmp.loc[i, 'content'][500*i:500*(i+1)]).checked
                elif i == (iter-1):
                    res += spell_checker.check(tmp.loc[i, 'content'][500*i:]).checked
            tmp.loc[i, 'content'] = res
        else: # 텍스트 길이가 500보다 작을 때
            try:
              tmp.loc[i, 'content'] = spell_checker.check(res).checked
            except:
              error_idx.append(i)
    return tmp
# 한글만 남기기
def extract_num_eng(text):
    hangul = re.compile('[^가-힣]')
    result = hangul.sub(' ', text)
    return result
# 형태소 - 명사만 추출
# 한 행당 한 리뷰가 들어가게 처리
def tagging(df):
    okt = Okt()
    words = df['content'].tolist()
    total = [] # 한 행당 리뷰 형태소
    for i in tqdm(words):
        morph_list = [] # 한 리뷰당
        for word in okt.pos(i, stem = True):
            if word[1] in ['Noun']:
                morph_list.append(word[0])
        total.append(morph_list)
    return total

def preprocessing_text(df):
    df = duplicate_drop(df)
    df['content'] = df['content'].apply(lambda x: extract_word(x))
    df['content'] = df['content'].apply(lambda x: extract_num_eng(x))
    return df

show_df = replace_cont(show_df) # 공연 내용 - 줄거리,작품설명으로 채우기

# 전처리
show_df = preprocessing_text(show_df)
show_df.drop(['작품설명','줄거리'],axis=1,inplace=True)
movie_df = preprocessing_text(movie_df)
drama_df = preprocessing_text(drama_df)

stop_word = pd.read_csv('C:/Users/alsru/Desktop/Project/Flask_git/2023-kopis/analysis/data/중간불용어_조정_완성.csv')
stop_word_list = stop_word['stopword'].tolist()
add_list = ['가젔습', '갈껍니', '갈렵', '감쩌', '강추핮', '강츄입', '강츄합', '걑습', '거깉', '거랍',
            '거슬렀', '거웠습', '것과', '것깉', '겉습', '견지', '관계', '관랍했', '구기', '군무', '굴렸습',
            '굿닝', '귭핫쏘', '극어', '기대', '깅추입', '깜짝', '꺄아', '꼽으시', '뀨용쏘', '끅끅대', '끼렸습',
            '나빌레', '낚였', '남버', '낫띵', '넘나듭', '넜습', '놨답', '놨습', '눴습', '뉴듹입', '느껴젔습', '님이셨습',
            '님입', '닝곡', '다니렵', '다릊지', '다시', '다웠습', '다채롭습', '댄스', '델꾸', '뎃줄', '도흐나', '동생', '동화',
            '돟았습', '돠었습', '되뇌었답', '듀뷴', '드럼', '드리큘', '드이스퀴스', '디립', '디캠', '떙떙', '떠드', '또랍', '또헤',
            '락뮤같', '락뮤입', '락입', '랂습', '러답', '러라아냋처러어', '러루', '러빗입', '러였', '러입', '런용', '렁스입', '렁스했',
            '레플', '렐레', '렛미플', '롭습', '룰러', '뤠줴에', '리카', '마렵', '막레전', '맘깉', ' 맴찣입', '맺혔습', '맺힙', '먼님',
            '면회', '몇핸', '몰랏다', '몰려듭', '몰입', '뫘습', '무대', '뭉텅', '므흣합', '믈랐습', '미소', '미챴', '밀려듭', ' 밍스',
            '바둥', '바랬습', '바부', '반대', '발기', '밟힙', '밭았습', '번득', '베르입', '보냤습', '보넙', '보싳', '보캅', '볼콘',
            '봈습', '봣숩', '뵀습', '부숩', '부인', '붉혔', '블랑슈로', '블메포입', '블며들엇', '블엑입', '븨입', '비걱거리', '비작',
            '비튤', '비트', '빠체입', '빡됩', '빨렸습', '뻔혔답', '뻘쭘합', '뽀삐', '뽯팅', '뽱뽱터', '뿜뿜입', '뿜뿜합', '사랑', '살럈',
            '살타', '상상', '상쇄합', '생각', '샤큘입', '센스', '셉트', '셨으', '소문', ' 소화', '솔렘', '송입', '솧투리봐', '순정', '숩데',
            '숮미', '슈또풍입', '슈또풍했', '슝가', '스베넷', '슬포', '슾르', '싄나', '신비', '쎄에롸', '쏜켱옌', '쓰앵님', '씐나씐', '씬뭐',
            '아쉡', '아쉽웠습', '아싀웠', '아트', '아픚', '악마', '앖습', '앙드', '애릿합', '앵콜', '어떘', '어습', '어지게', '어쨋', '어쩌느',
            '어쩌므그', '어쩌실', '어찌됏', '어햎보', '어햎입', '언됩', '엄다녤이엇습', '엄댜', '엄드큘입', '엄치척입', '엇습', '었던거갗',
            '에에에에', '엘송입', '엠알이', '엮었습', '연출', '엺차', '염큘', '영화', '예벘', '예브', '오렵', '오르펩', '오므리', '오비',
            '옥덴', '온순', '온주', '옮았습', '완벼크합', '왕습', '욨습', '우블', '우쿠렐', '욱했', '웃음', '웜합', '위로', '위트', '유너',
            '유승', '윱핫혀', '응웝합', '잊힙', '잏었', '자밋었 습', '잘맆', '잘봒습', '잘봣슨니', '잘봫습', '잘생맆', '잘힌시', '재맜습',
            '재맜었습', '재미', '재밌엏습', '재밌짆', '잼밌습', '정략', '젛겠', '젛았습', '젤맆', '존버탈', '존잼턍입', '졸귀', '종합', '좇으면',
            '좋깄습', '좋아씅', '좋앗슴', '좋앟습', '좋윽거같', '좠습', '죠았슴', '중블아', '줗았습', '쥬세', '쥬찬', '쥰잼입', '즇았습',
            '즡거웠습', '직딩입', '짊어', '집중', '짜룽합', '짜릿햇슿', '쫀쫀합', '쫄깃합', '쭈굴쭈굴합', '쮸뼛', '찢킬입', '찬쭌', '찰떱',
            '참촣', '챴습', '초연', '촘촘', '최고', '최애', '쵝옵', '추억', '취합', '치얐', '치혜료', '카베', '캐럴', '캐슷입', '캐슷체',
            '캬아', '커퀴', '케랙', '켸르', '콘드', '콜레보', '크럼', '클쏭', '클캣', '터트렸습', '턴슨', '턴했', '테츠', '토끼', '토씬',
            '톰소', '투닥거렸', '투처', '트레플', ' 트함', '팔락이', '퍼바님', '퍼입', '펄떡', '펐습', '포디콰했', '푹빠젔습', '프로', '프블',
            '플렛', '핑입', '하자', '핬잖', '항목', '해보렵', '핸글', ' 핸복햇슴', '핸볼햇흡', '행맆', '행복', '햤다', '향쭌', '허름합', '협소합',
            '형식', '호흡', '홀렸거', '홀렸습', '홀립', '화음', '화잇팅입', '홙쥬', '후 텁', '훈몔', '훈성욱', '훌치', '훟륭합', '흔듭', '힜으']
stop_word_list = stop_word_list + add_list

def tokenizer(raw, pos=['Noun'],stopword=stop_word_list):
    from konlpy.tag import Okt
    okt = Okt()
    return [word for word, tag in okt.pos(raw) if len(word) > 1 and tag in pos and word not in stopword]

# difflib
import difflib
def tokenizer_2(raw, pos=['Noun','Verb'],stopword=stop_word_list):
    from konlpy.tag import Okt
    okt = Okt()
    lst = [word for word, tag in okt.pos(raw) if len(word) > 1 and tag in pos and word not in stopword]
    return " ".join(lst)

show_df['token'] = show_df['content'].apply(lambda x: tokenizer_2(x))
movie_df['token'] = movie_df['content'].apply(lambda x: tokenizer_2(x))
drama_df['token'] = drama_df['content'].apply(lambda x: tokenizer_2(x))


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

def get_matcher(cat,answer_df,show_df):
    data = []
    answer_list = answer_df['token']
    for i,answer in enumerate(answer_list):
        for j,show_string in enumerate(show_df['token']):
            answer_bytes = bytes(answer, 'utf-8')   
            show_bytes = bytes(show_string, 'utf-8')
            answer_bytes_list = list(answer_bytes)
            show_bytes_list = list(show_bytes)

            sm = difflib.SequenceMatcher(None, answer_bytes_list, show_bytes_list)
            similar = sm.ratio()*100
            if similar >= 25:
                #print(show_df['제목'][j],similar)
                data.append({'카테고리':cat, "콘텐츠제목":answer_df['제목'][i],'제목':show_df['제목'][j],'유사도':round(similar,2),
                             '공연날짜':show_df['기간'][j],'장소':show_df['장소'][j],'주소':show_df['주소'][j],'이미지URL':show_df['이미지url'][j],'상세URL':show_df['url'][j]})
    df = pd.DataFrame(data)
    df.sort_values(by=['콘텐츠제목','유사도'], inplace=True, ignore_index=True, ascending=False)
    df.drop('유사도',axis=1,inplace=True)
    return df

movie_simm_df = get_matcher('영화',movie_df, show_df)
drama_simm_df = get_matcher('드라마',drama_df, show_df)

final_df = pd.concat([movie_simm_df,drama_simm_df], axis=0, ignore_index=True)
#final_df.to_csv(f'./Keywi/Modeling/final/{week_no()}_유사공연.csv',index=False)
num = 0
cat_num = []
    
for name in final_df['콘텐츠제목'].unique():
    for i in range(len(final_df)):
        if final_df.loc[i,'콘텐츠제목'] == name:
            # print(num,name)
            cat_num.append(num)
    num += 1

final_df['콘텐츠번호'] = cat_num
# DB에 올리기
conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
# 커서 생성
db = conn.cursor()
# 쿼리 실행
sql_state = """alter table KEYWIDB.HotLiked drop foreign key HotLiked_ibfk_2""" # 참조하는 경우 테이블 삭제 안되므로 외래키 제거
db.execute(sql_state)
sql_state = """TRUNCATE KEYWIDB.HotInfo"""
db.execute(sql_state)
sql_state = """ALTER TABLE KEYWIDB.HotInfo AUTO_INCREMENT = 1"""
db.execute(sql_state)
# DB 올릴때 더 빠른 방법 없을까 ?? 165개 업로드하는데 1분 걸림
for cat,cont_num,cont_name,show_name,show_venue,show_address,show_date,show_url,img_url in tqdm(zip(final_df['카테고리'],final_df['콘텐츠번호'],final_df['콘텐츠제목'],final_df['제목'],final_df['장소'],final_df['주소'],final_df['공연날짜'],final_df['상세URL'],final_df['이미지URL'])):
    sql_state = """INSERT INTO KEYWIDB.HotInfo(category,cont_num,cont_name,show_name,show_venue,show_address,show_date,show_url,img_url) 
                VALUES ("%s","%s","%s", "%s", "%s", "%s", "%s", "%s", "%s")"""%(tuple([cat,cont_num,cont_name,show_name,show_venue,show_address,show_date,show_url,img_url]))
    db.execute(sql_state)

# 외래키 다시 추가하기
sql_state = """alter table KEYWIDB.HotLiked add constraint HotLiked_ibfk_2 foreign key(show_id) references KEYWIDB.HotInfo(id) ON DELETE CASCADE"""
db.execute(sql_state)

conn.commit()
conn.close()


