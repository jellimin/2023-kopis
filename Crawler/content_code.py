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
from datetime import timedelta

ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings('ignore')

class ContentCrawler:
    # 디스코드 알림 연동    
    def send_message(self,message):
        DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1140278554609844264/aUubW_3WgjV_hwzVcQPjeWrhQzm1lZBS481VVIHqO7Cq_4A7E0xcJ2FPKsxRtaWy6R1r"
        requests.post(DISCORD_WEBHOOK_URL, data=message)

    def week_no(self):
        s = datetime.today().strftime("%Y-%m-%d") 
        month = datetime.today().month
        target_day = datetime.strptime(s, "%Y-%m-%d")

        firstday = target_day.replace(day=1)
        while firstday.weekday() != 0: 
            firstday += timedelta(days=1)
        
        if target_day < firstday: 
            return 0
    
        return f'{month}월 {(target_day - firstday).days // 7 + 1}주차' 

    # 수집하고자하는 정보 - 영화제목,장르,주요정보,출연진정보(주연&출연)
    # DAUM 영화 - 주간 박스오피스 1위 - 15위
 
    
    def get_movie_info(self): # 영화 제목, 주요정보, 상세페이지 URL
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
            data.append({'제목': name.strip(), '줄거리': summary.strip(), 'URL': url})
        # 데이터프레임 생성
        df = pd.DataFrame(data)

        return df

    def get_movie_detail(self): # 장르, 출연진 정보
        df = self.get_movie_info()
        base_url = 'https://movie.daum.net'
        genre_list = [] # 데이터 넣을 리스트 생성 
        for movie_url in df['URL']:
            #movie_url = movie_url.replace('main','crew')
            detail_url = base_url + movie_url

            headers = {'User-Agent':generate_user_agent(os='win', device_type='desktop')}
            res=requests.get(detail_url, headers=headers) # html 가져오기
            res.raise_for_status()
            soup=BeautifulSoup(res.text,"lxml")
            
            # 장르 - //*[@id="mainContent"]/div/div[1]/div[2]/div[2]/div[1]/dl[2]
            movie_genre = soup.find_all('dl', class_='list_cont')[1].text # 영화 장르
            if '장르' not in movie_genre:
                movie_genre = soup.find_all('dl', class_='list_cont')[2].text.replace('장르',"").replace(" ","") # 영화 장르
            genre_list.append(movie_genre.replace("장르","").replace(" ","").strip())
        df['장르'] = genre_list
        now = self.week_no()
        #df.to_csv(f'./Crawling/data/{now}_영화.csv',index=False)
        message = {'content':f'{now}_영화 박스오피스 크롤링을 완료했습니다.'}
        self.send_message(message)

        return df[['장르','제목','줄거리','URL']]


    # 수집하고자하는 정보 - 드라마제목, 순위, 상세페이지url, 줄거리

    def get_drama_info(self): # 드라마 제목, 상세페이지 url
    
        result_data = []
        query = ['주간 드라마 시청률', '주간 드라마 종합편성시청률', '주간 드라마 케이블시청률']
    
        for i in query:
            base_url = "https://search.naver.com/search.naver"
            query_params = {
                "sm": "tab_hty.top",
                "where": "nexearch",
                "query": i
            }
            res = requests.get(base_url, params=query_params)
            soup = BeautifulSoup(res.content, "html.parser")

            weekly_drama = soup.find(class_ = "tb_list").find_all("tr")[1:4]
            k = 1
            for j in weekly_drama:
                drama = j.find("a")
                if drama == None:
                    continue
                drama_title = drama.text
                drama_rank = str(k)
                drama_url = drama['href']
                k += 1
                result_data.append({'제목':drama_title, '순위':drama_rank, 'URL':drama_url})
        df = pd.DataFrame(result_data)
        return df

    def get_drama_detail(self): # 줄거리
        df = self.get_drama_info()
        url = df['URL']
        base_url = "https://search.naver.com/search.naver"

        drama_content = []
        for i in range(len(url)):
            detail_url = base_url + url[i]
            res = requests.get(detail_url)
            soup = BeautifulSoup(res.content, "html.parser")
            content = soup.find(class_='desc _text').text
            drama_content.append(content)
        df['줄거리'] = drama_content
        now = self.week_no()
        df.to_csv(f'./Crawling/data/{now}_드라마.csv',index=False)
        message = {'content':f'{now}_드라마 줄거리 크롤링을 완료했습니다.'}
        self.send_message(message)

        return df[['제목', '순위', '줄거리', 'URL']]

    def get_entertain_info(self): # 제목, 회차, 방영날짜, 출연진
        result_data = []
        query = ['나 혼자 산다 회차정보', '유 퀴즈 온 더 블럭 회차정보', '놀라운 토요일 회차정보']
        
        for i in query:
            base_url = "https://search.naver.com/search.naver"
            query_params = {
                "sm": "tab_hty.top",
                "where": "nexearch",
                "query": i
            }
            res = requests.get(base_url, params=query_params)
            soup = BeautifulSoup(res.content, "html.parser")

            enter = soup.find_all(class_="list_col _column")
            for j in enter:
                title = i.replace('회차정보', "")
                epis = j.find(class_="num_txt").text
                date = j.find(class_="date_info").text
                actor = j.find("dd").text
                result_data.append({'제목':title, '회차':epis, '날짜':date, '출연진':actor})
        df = pd.DataFrame(result_data)

        now = self.week_no()
        df.to_csv(f'./Crawling/data/{now}_예능.csv',index=False)
        message = {'content':f'{now}_예능 출연진 크롤링을 완료했습니다.'}
        self.send_message(message)

        return df
