# 필요한 라이브러리 로딩
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import re
import pandas as pd
from tqdm import tqdm_notebook
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import warnings
warnings.filterwarnings('ignore')

chrome_options = Options()
chrome_options.add_argument("headless") #창숨기기

# 크롤링 할 csv 파일 로딩
data = pd.read_csv('./data/통합_티켓링크_URL코드.csv')
index_df = pd.read_csv('./data/티켓링크_인덱스.csv')[395:]
data = data.iloc[index_df['마민경'].values]
data.reset_index(drop=True,inplace=True)

# 100%:5점,100%:5점,80%:4점,60%:3점,40%:2점,20%:1점
def scoring(review_score):
    # 별점 -> 점수로 변환(1-5점) 함수
    percent = list(map(lambda x : review_score[x]['style'].split(' ')[1][0:3],range(0,len(review_score))))
    convert_score = [] # 점수 리스트
    for per in percent:
        if per == '100':
            convert_score.append(5.0)
        else:
            convert_score.append(int(per[0])/2 )
    return convert_score


def scrape_ticketlink_review(url_df):
    zero_review = [] # 리뷰 없는 URL 인덱스 저장 리스트
    total_result = pd.DataFrame(columns =['showcode','date','rating','text']) # 최종 리뷰 저장용 데이터프레임
    result = pd.DataFrame(columns =['공연코드','날짜','별점','리뷰']) # 공연 당 리뷰 저장 데이터프레임
    url_list = url_df['판매페이지URL'] # 수집 대상 URL
    head = 'http://www.ticketlink.co.kr/product/' 
    check_zero = 0 # 리뷰 없는 페이지 개수 확인용 변수
    for k in tqdm_notebook(range(len(url_list))): # url_list에서 하나씩 반복
        web_url = head + str(url_list[k])
        try:
            service = Service(executable_path = "./chromedriver.exe" )
            driver = webdriver.Chrome(service = service, options=chrome_options)
            wait = WebDriverWait(driver, 5)
            print("#######{}번째 페이지 접속 시작#######".format(k+1+395))
            driver.get(web_url) # 예매 페이지 접속
            driver.implicitly_wait(2)
            x_path = '//*[@id="content"]/section[3]/div/div/div/ul/li[2]/button'
            
            try:
                review_tab = driver.find_element(By.XPATH,x_path) # 리뷰탭 element 찾기
                tab_header = review_tab.text
                if tab_header != '관람후기':
                    x_path = '//*[@id="content"]/section[5]/div/div/div/ul/li[2]/a' # 리뷰탭이 다른 칸에 있는 경우
                    review_tab = driver.find_element(By.XPATH,x_path) # 리뷰탭 element 찾기
                    
                driver.execute_script("arguments[0].click();", review_tab)
                time.sleep(5) # 리뷰 로딩까지 대기 
                review_num = driver.find_element(By.XPATH,'//*[@id="productReview"]/div[1]/h2/span').text # 리뷰 개수
                if int(review_num)%10 == 0:
                        total_page = int(review_num)//10
                else:
                    total_page = int(review_num)//10+1 # 한 페이지당 리뷰 10개씩 나타남 
                print("리뷰 개수:",int(review_num)) # 전체 리뷰 개수 확인
                review_num = int(review_num)
                if review_num >= 10: # 리뷰가 10개 이상 존재하는 경우
                    date_list = [] # 리뷰 작성 날짜 저장 리스트
                    score_list = [] # 리뷰 점수 저장 리스트
                    text_list = [] # 리뷰 텍스트 저장 리스트
                    if review_num > 1000: # 리뷰가 1000개가 넘는 경우
                        total_page = 100 # 최대 1000개까지 수집
                    else:  
                        for page_num in range(total_page): # 총 페이지 개수만큼 반복
                            html = driver.page_source # 리뷰 탭 선택 후 html 가져오기
                            bs = BeautifulSoup(html,'lxml') # lxml 파싱
                            # 별점 처리
                            get_score = bs.find_all('span',class_='product_star14_per') # 별점만 가져오기
                            driver.implicitly_wait(2)
                            score_list.extend(scoring(get_score)) # 별점 -> 점수로 변환하는 함수
                            # 리뷰 날짜
                            date = bs.find_all('span', class_='comment_date') # 날짜 가져오기
                            driver.implicitly_wait(2)
                            date_text = [re.sub('<.+?>','',str(s),0).strip()  for s in date] # 태그 제외 텍스트만 추출
                            date_list.extend(date_text)
                            # 리뷰 텍스트
                            text = bs.find_all('p', class_='product_comment_desc') # 리뷰 텍스트 가져오기
                            driver.implicitly_wait(2)
                            text_list.extend([re.sub('<.+?>','',str(review),0).strip()  for review in text]) # 태그 제외 텍스트만 추출
                            if int(review_num) > 10: # 리뷰가 한 페이지 이상인 경우
                                # 다음 페이지로 이동
                                x_path_page = '//*[@id="productReview"]/div[3]/a[{}]'.format(page_num+3) # 다음 페이지 x_path
                                next_page = driver.find_element(By.XPATH,x_path_page) # 다음 페이지 x_path
                                driver.execute_script("arguments[0].click();", next_page)
                                wait.until(EC.presence_of_element_located((By.CLASS_NAME,'product_comment_desc'))) # 다 넘어갈 때 까지 대기
                        if not date_list or not score_list or not text_list: # 빈 리스트가 있는 경우
                            pass
                        else:
                            code = [url_df['공연코드'][k] for i in range(int(review_num))] # 데이터프레임 저장용 공연코드 리스트 생성
                            print(code,date_list,score_list,text_list) # 수집 확인
                            result_val = {'showcode':code,'date':date_list,'rating':score_list,'text':text_list}
                            result = pd.DataFrame(result_val) # 수집한 데이터 저장
                            total_result = pd.concat([total_result,result],axis=0) # 최종 데이터프레임에 저장
                            total_result = total_result.reset_index(drop=True)
                            print(total_result) # 저장 확인
                elif review_num < 10: # 리뷰가 10개 이하인 경우
                    print("리뷰가 10개 이하 입니다.")
                    zero_review.append(k) # 리뷰 10개 이하 페이지 개수 확인용
                    check_zero += 1
            except NoSuchElementException: # 리뷰 탭이 존재하지 않거나 페이지가 존재하지 않는 경우
                print('존재하지 않는 페이지 입니다.')
                pass # for문 재생하지 않고 넘어감
        except ElementNotVisibleException:
            print('오류발생') 
        
        if k % 100 == 99: # 10개마다 끊어서 저장 !
            total_result.to_csv(f'./ticketlink_review/티켓링크_{k + 1}번째리뷰.csv', index = False)
            total_result = pd.DataFrame(columns =['showcode','date','rating','text'])   
    return total_result


total_result= scrape_ticketlink_review(data) # 티켓링크 리뷰 가져오기
print(total_result)
total_result.to_csv(f'./ticketlink_review/티켓링크_마지막_리뷰.csv', index = False)
# import os

# file_list = os.listdir('./TL_Review/')
# print ("file_list: {}".format(file_list[:]))
# list_tmp = file_list[:]
# review_total = pd.DataFrame()
# review_total
# for i in list_tmp:
#     review_tmp = pd.read_csv(f'./TL_Review/{i}')
#     review_total = review_total.append(review_tmp)
# review_total.to_csv('./ticketlink_review/티켓링크_리뷰_민경.csv')