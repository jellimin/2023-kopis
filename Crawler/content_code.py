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

    ## 드라마 줄거리 추출
    def get_drama_info(self):
        # 크롤링 오류 발생 제거
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("headless") #창숨기기
        

        query = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%8B%9C%EC%B2%AD%EB%A5%A0+%EC%88%9C%EC%9C%84&oquery=08%EC%9B%9407%EC%9D%BC%EC%A3%BC+%EC%A7%80%EC%83%81%ED%8C%8C+%EC%8B%9C%EC%B2%AD%EB%A5%A0&tqi=iLF5ZlprvN8ssix3jbsssssssn4-214140"
        service = Service(executable_path = "./chromedriver.exe" )
        # driver = webdriver.Chrome(service = service, options=chrome_options)

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(query)

        rank = []
        title = []
        url = []

        # '주간' 클릭
        driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[1]/section[1]/div/div[2]/div[2]/div[1]/ul/li[2]/a").click()
                
        for j in range(1, 4):
            # 지상파, 종합편성, 케이블 페이지 존재
            page = "/html/body/div[3]/div[2]/div/div[1]/section[1]/div/div[2]/div[1]/ul/li[{}]/a".format(j)
            driver.find_element(By.XPATH, page).click()

            # 드라마       
            select = "/html/body/div[3]/div[2]/div/div[1]/section[1]/div/div[2]/div[2]/div[2]/select/option[2]"
            driver.find_element(By.XPATH, select).click()

            for i in range(1, 4):   
                a = str(i) # rank
                b = "/html/body/div[3]/div[2]/div/div[1]/section[1]/div/div[2]/div[3]/div/table/tbody/tr[{}]/td[2]/p/a".format(i) # 제목, url
            
                titlee = driver.find_element(By.XPATH, b).text
                urll = driver.find_element(By.XPATH, b).get_attribute('href')

                rank.append(a)
                title.append(titlee)
                url.append(urll)

        dict = {'순위':rank, '제목':title, 'URL':url}
        data = pd.DataFrame(dict)
        url = data['URL']

        content = [] # 줄거리

        # 드라마
        for i in range(len(url)):
            query = url[i]
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(query)
            # driver.implicitly_wait(10)

            cont = driver.find_element(By.CSS_SELECTOR, 'span.desc._text').text
            content.append(cont)

        data['줄거리'] = content
        #data.drop('URL', axis=1, inplace=True)
        now = self.week_no()
        #data.to_csv(f"./Crawling/data/{now}_drama.csv", index=False, sep=",")

        # 함수 정의 후 크롤링 끝난 뒤 send_message 하기 ! 
        message = {'content':f'{now}_드라마 줄거리 크롤링을 완료했습니다.'}
        self.send_message(message)
        return data[['제목','줄거리','URL']]
    
    def get_entertain_info(self):
        ## 시청률 관련 크롤링 - 예능
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("headless") #창숨기기
        
        service = Service(executable_path = "./chromedriver.exe" )
        # 예능 출연진 크롤링

        ent_title = ['나 혼자 산다', '유 퀴즈 온 더 블럭', '놀라운 토요일'] # 예능프로 제목

        title = []
        actor = [] # 출연진 내용
        series = [] # 회차
        date = [] # 날짜

        # 예능
        for i in range(len(ent_title)):
            query = "https://search.naver.com/search.naver?query={}".format(ent_title[i])
            driver = webdriver.Chrome(service=service,options=options)
            driver.get(query)
            # driver.implicitly_wait(10)

            driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[4]/div/div/ul/li[5]/a").click() #회차정보 탭으로 이동

            for j in range(1, 3): # 2개 회차
                title.append(ent_title[i])
                a = "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[{}]/ul/li[1]/div/div[1]/strong/a/span".format(j)
                aa = driver.find_element(By.XPATH, a).text
                series.append(aa)
                b = "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[{}]/ul/li[1]/div/div[1]/span".format(j)
                bb = driver.find_element(By.XPATH, b).text
                date.append(bb)
            
                temp=[]
                while(True):
                    try:
                        for k in range(1, 6):
                            c = "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[{0}]/ul/li[1]/div/dl/dd/a[{1}]".format(j, k)
                            act = driver.find_element(By.XPATH, c).text
                            temp.append(act)   
                        temp = ",".join(temp)
                    except:
                        break
                actor.append(temp)

        dict = {'제목':title, '회차정보':series, '방영날짜':date, '출연진':actor}
        df = pd.DataFrame(dict)
        now = self.week_no()
        #df.to_csv(f"./Crawling/data/{now}_entertainment.csv", index=False, sep=",")

        # 함수 정의 후 크롤링 끝난 뒤 send_message 하기 ! 
        message = {'content':f'{now}_예능 출연진 크롤링을 완료했습니다.'}
        self.send_message(message)
        return df[['제목','회차정보','방영날짜','출연진']]


