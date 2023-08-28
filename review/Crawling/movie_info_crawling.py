# 라이브러리 불러오기
# 필요한 라이브러리 로딩
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import re
import datetime
from datetime import datetime
import lxml
import pandas as pd
from tqdm import tqdm_notebook
import requests
from user_agent import generate_user_agent, generate_navigator
import os
import sys
import urllib.request
import warnings
import ssl
from urllib.error import HTTPError, URLError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings('ignore')

# 디스코드 알림 연동
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1140278554609844264/aUubW_3WgjV_hwzVcQPjeWrhQzm1lZBS481VVIHqO7Cq_4A7E0xcJ2FPKsxRtaWy6R1r"
def send_message(message):
    requests.post(DISCORD_WEBHOOK_URL, data=message)

ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings('ignore')

# 수집하고자하는 정보 - 영화제목,장르,주요정보,출연진정보(주연&출연)
# DAUM 영화 - 주간 박스오피스 1위 - 15위

def get_movie_info(): # 영화 제목, 주요정보, 상세페이지 URL
    base_url = 'https://movie.daum.net/ranking/boxoffice/weekly' # url 설정
    
    headers = {'User-Agent':generate_user_agent(os='win', device_type='desktop')}
    res=requests.get(base_url, headers=headers) # html 가져오기
    res.raise_for_status()
    soup=BeautifulSoup(res.text,"lxml")

    data = [] # 데이터 넣을 리스트 생성 

    movie_names = soup.find_all('a', class_='link_txt') # 영화 제목
    movie_summarys = soup.find_all('a', class_='link_story') # 영화 내용
    for movie_name, movie_summary in zip(movie_names, movie_summarys):
        name = movie_name.text
        summary = movie_summary.text
        url = movie_summary['href']
        #print(name,summary,url)
        # 데이터 리스트에 추가
        data.append({'name': name.strip(), 'summary': summary.strip(), 'url': url})
    # 데이터프레임 생성
    df = pd.DataFrame(data)

    return df

df = get_movie_info()

def get_movie_detail(df): # 장르, 출연진 정보
    base_url = 'https://movie.daum.net'
    genre_list = [] # 데이터 넣을 리스트 생성 
    crew_list = []
    for movie_url in df['url']:
        movie_url = movie_url.replace('main','crew')
        detail_url = base_url + movie_url

        headers = {'User-Agent':generate_user_agent(os='win', device_type='desktop')}
        res=requests.get(detail_url, headers=headers) # html 가져오기
        res.raise_for_status()
        soup=BeautifulSoup(res.text,"lxml")
        
        # 장르 - //*[@id="mainContent"]/div/div[1]/div[2]/div[2]/div[1]/dl[2]
        movie_genre = soup.find_all('dl', class_='list_cont')[1].text # 영화 장르
        if '장르' not in movie_genre:
            movie_genre = soup.find_all('dl', class_='list_cont')[2].text.replace('장르',"").replace(" ","") # 영화 장르
        
        # chrome_options = Options()
        # chrome_options.add_argument("headless") #창숨기기
        # service = Service(executable_path = "./Crawling/chromedriver.exe" )

        # driver = webdriver.Chrome(service = service, options=chrome_options)

        # driver.get(detail_url)
        # driver.implicitly_wait(5)
        # html = driver.page_source
        # soup=BeautifulSoup(html,"lxml")
        # crew_names= soup.find_all('strong',class_='tit_item')
        # name_list = []
        # for name in crew_names:
        #     name_list.append(name.text.strip())

        genre_list.append(movie_genre.strip())
        #crew_list.append(name_list)
    df['genre'] = genre_list
    #df['crew_names'] = crew_list
    return df
detail_df = get_movie_detail(df)
now = datetime.today().strftime('%Y%m%d')
detail_df.to_csv(f'./Crawling/data/{now}_영화.csv',index=False)
message = {'content':f'{now}_영화 박스오피스 크롤링을 완료했습니다.'}
send_message(message)

