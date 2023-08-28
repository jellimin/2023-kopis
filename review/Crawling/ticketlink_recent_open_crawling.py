# 필요한 라이브러리 로딩
import requests
import time
import re
import lxml
import pandas as pd
import os
import sys
import urllib.request
import warnings
import ssl
import pymysql
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm_notebook
from user_agent import generate_user_agent, generate_navigator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import datetime
from datetime import datetime
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.error import HTTPError, URLError

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1140278554609844264/aUubW_3WgjV_hwzVcQPjeWrhQzm1lZBS481VVIHqO7Cq_4A7E0xcJ2FPKsxRtaWy6R1r"
def send_message(message):
    requests.post(DISCORD_WEBHOOK_URL, data=message)

ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings('ignore')

# 페이지 내 자체 정렬 기능 X
# 10페이지까지 수집 후 오늘 날짜 이후 공지만 남기기

def get_detailinfo(driver):
    data = []

    # 제목, 날짜 가져오기
    show_titles = driver.find_elements(By.CSS_SELECTOR, 'td.tl.p_reative > a')
    show_dates = driver.find_elements(By.CSS_SELECTOR, '.open_info')

    for titles,dates in zip(show_titles,show_dates):
        title = titles.text.replace('[단독판매]', '').replace('티켓오픈 안내','').replace(" ","")
        href = titles.get_attribute('href')
        date = dates.text.replace('오픈:', '')
        date = re.sub(pattern = r'\([^)]*\)',repl='',string=date)
        datetime_format = " %Y.%m.%d %H:%M"
        date = datetime.strptime(date,datetime_format)
        data.append({'공연제목': title.strip(), '티켓오픈일시': date, 'URL': href.strip()})
    df = pd.DataFrame(data)
    return df

def get_openinfo():
    result = pd.DataFrame()
    # 페이지 이동
    query = "https://www.ticketlink.co.kr/help/notice#TICKET_OPEN"
    chrome_options = Options()
    #chrome_options.add_argument("headless") #창숨기기
    
    service = Service(executable_path = "./Crawling/chromedriver.exe" )
    driver = webdriver.Chrome(service = service, options=chrome_options)
    driver.get(query)
    driver.implicitly_wait(5)
    
    for i in range(4,14):
        df = get_detailinfo(driver)
        result = pd.concat([result,df],axis=0)
        elem = driver.find_element(By.CSS_SELECTOR, f"#pagination > a:nth-child({i})")
        elem.send_keys(Keys.ENTER)
    result.reset_index(inplace=True,drop=True)
    # 현재 날짜보다 이전에 오픈하는 공연 제거
    for i,dates in enumerate(result['티켓오픈일시']):
        now = datetime.now() # 현재 시간 가져오기
        if dates < now:
            result.drop(index=i, inplace=True)
    result = result.sort_values(by='티켓오픈일시',ascending=False,ignore_index=True) # 오픈일시기준 내림차순 정렬 & 인덱스 초기화

    return result

result = get_openinfo()

# 상세페이지에서 이미지 URL 가져오기
#df = pd.read_csv(path)

def get_image_info(df):
    img_urls = []
    chrome_options = Options()
    #chrome_options.add_argument("headless") #창숨기기
    service = Service(executable_path = "./Crawling/chromedriver.exe" )
    driver = webdriver.Chrome(service = service, options=chrome_options)
    #print(len(df['URL']))
    for url in df['URL']:
        print(url)
        driver.get(url)
        driver.implicitly_wait(3)
        url_tag = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/dl/dt/dl/dd[1]/img').get_attribute("src")
        img_urls.append(url_tag)
    df['IMG'] = img_urls
    return df
df = get_image_info(result)
now = datetime.datetime.today().strftime('%Y%m%d')
num = len(df)
path = f'./Crawling/data/{now}_티켓링크_오픈공연_{num}.csv'
df.to_csv(path,index=False)
message = {'content':f'{now}_티켓링크 오픈정보 크롤링을 완료했습니다.'}
send_message(message)

# conn = pymysql.connect(host='admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com', user='hashtag', password='hashtag123', db='test_db', charset='utf8')


# # 커서 생성
# db = conn.cursor()
# # 쿼리 실행
# for name,date,url in zip(result['공연제목'],result['티켓오픈일시'],result['URL']):
#     sql_state = """INSERT INTO test_db.open_info(show_name, open_date, show_url) 
#     VALUES ('%s', '%s', '%s')"""%(tuple([name,date,url]))
#     db.execute(sql_state)
# conn.commit()
# # 연결 종료
# conn.close()
