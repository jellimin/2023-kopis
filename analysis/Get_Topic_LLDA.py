import pandas as pd
import pymysql
from tqdm import tqdm
import model.labeled_lda as llda

## L-LDA 학습 부분
# 학습 데이터 파일 (토픽모델링 후)
df = pd.read_csv('C:/Users/sumin/OneDrive/바탕 화면/Labeled-LDA-Python-master/L-LDA_입력데이터.csv')
tmp = df
tmp.reset_index(drop = True, inplace = True)

labeled_documents = []

for i in tqdm(range(len(tmp))):
    labeled_documents.append((tmp.loc[i, 'Text'] * 10, [tmp.loc[i, 'Topic']]))

# new a Labeled LDA model
llda_model = llda.LldaModel(labeled_documents=labeled_documents, alpha_vector=0.01)
print(llda_model)

# training
# llda_model.training(iteration=10, log=True)
while True:
    print("iteration %s sampling..." % (llda_model.iteration + 1))
    llda_model.training(1)
    print("after iteration: %s, perplexity: %s" % (llda_model.iteration, llda_model.perplexity()))
    print("delta beta: %s" % llda_model.delta_beta)
    if llda_model.is_convergent(method="beta", delta=0.01):
        break

# iteration 2477 sampling...
# gibbs sample count:  7755998
# after iteration: 2477, perplexity: 704.1906997596153
# delta beta: 0.04938661875470182

save_model_dir = "data/model"
# llda_model.save_model_to_dir(save_model_dir, save_derivative_properties=True)
llda_model.save_model_to_dir(save_model_dir)

# load from disk
llda_model = llda.LldaModel()
llda_model.load_model_from_dir(save_model_dir, load_derivative_properties=False)

## L-LDA 예측 부분
# 새로운 리뷰 불러오기 (현재공연중_전처리완료된파일)
df = pd.read_csv('C:/Users/pmy49/OneDrive/바탕 화면/Labeled-LDA-Python-master/공연중_리뷰_데이터_최종.csv')
df = df.dropna(subset=['text'])

for i, document in tqdm(enumerate(df['text'])):
    topics = llda_model.inference(document=document * 100, iteration=100, times=10)
    # 가장 높은 확률의 토픽이 common_topic인 경우
    if topics[0][0] == 'common_topic':
        df.loc[i, 'topic'] = topics[1][0]
    # 아닌 경우
    else:
        df.loc[i, 'topic'] = topics[0][0]

# 각 공연별 topic 살펴보기 위한 그룹화
count_df = df[['제목', 'topic', 'text']].groupby(['제목', 'topic']).count()

# 그룹화 -> 데이터프레임 생성
count_df = count_df.reset_index()
print(count_df)

# 가장 많은 토픽으로 분류하기
title = count_df['제목'].unique()
out_df = pd.DataFrame()

for i in title:
    tmp = count_df[count_df['제목'] == i]
    idx = tmp["text"].idxmax()
    max_tmp = tmp.loc[idx]
    max_tmp = pd.DataFrame([max_tmp])
    out_df = pd.concat([out_df, max_tmp], axis = 0)

# 데이터 병합 및 내보내기
new_df = df[df.columns.difference(['rating', 'text'])].drop_duplicates().dropna() # 제목, topic과 병합할 나머지 컬럼을 가진 데이터프레임
result = pd.merge(out_df[['제목', 'topic']], new_df, on = '제목', how = 'left')
# result.to_csv('./테스트5.csv', index = False)

## L-LDA 결과 -> DB
# df_topic = pd.read_csv("테스트5.csv")

# 제목, 기간, 공연장, 주소, 이미지url, 상세url, topic => (DB ShowInfo 테이블)
conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='KEYWIDB', charset='utf8')
# 커서 생성

db = conn.cursor()
# 쿼리 실행
sql_state = """DELETE FROM KEYWIDB.ShowInfo"""
db.execute(sql_state)

for name,date,place,address,image_url,detail_url,topic in zip(df_topic['제목'],df_topic['기간'],df_topic['장소'],df_topic['주소'],df_topic['이미지url'],df_topic['상세url'],df_topic['topic']):
    sql_state = """INSERT INTO KEYWIDB.ShowInfo(name,date,place,address,image_url,detail_url,topic)
                VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")"""%(tuple([name,date,place,address,image_url,detail_url,topic]))
    db.execute(sql_state)

conn.commit()
# 연결 종료
conn.close()
