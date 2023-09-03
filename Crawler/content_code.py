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
from tqdm import tqdm
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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from datetime import timedelta
from selenium.common.exceptions import NoSuchElementException

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
        while firstday.weekday() != 0: # 1주차의 시작요일을 월요일로
            firstday += timedelta(days=1)

        if target_day < firstday: 
            return f'{month}월 0주차'

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
        #self.send_message(message)

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
            time.sleep(1)
            content = soup.find(class_='desc _text').text
            drama_content.append(content)
        df['줄거리'] = drama_content
        now = self.week_no()
        #df.to_csv(f'./Crawling/data/{now}_드라마.csv',index=False)
        message = {'content':f'{now}_드라마 줄거리 크롤링을 완료했습니다.'}
        #self.send_message(message)

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
        #df.to_csv(f'./Crawling/data/{now}_예능.csv',index=False)
        message = {'content':f'{now}_예능 출연진 크롤링을 완료했습니다.'}
        # self.send_message(message)

        return df

class PerformCrawler:
    # 디스코드 알림 연동    
    def send_message(self,message):
        DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1140278554609844264/aUubW_3WgjV_hwzVcQPjeWrhQzm1lZBS481VVIHqO7Cq_4A7E0xcJ2FPKsxRtaWy6R1r"
        requests.post(DISCORD_WEBHOOK_URL, data=message)

   
    def week_no(self):
        s = datetime.today().strftime("%Y-%m-%d") 
        month = datetime.today().month
        target_day = datetime.strptime(s, "%Y-%m-%d")

        firstday = target_day.replace(day=1)
        while firstday.weekday() != 0: # 1주차의 시작요일을 월요일로
            firstday += timedelta(days=1)

        if target_day < firstday: 
            return f'{month}월 0주차'

        return f'{month}월 {(target_day - firstday).days // 7 + 1}주차' 
 
    # 플레이DB - 현재공연중인 공연 list [제목, 장르, url]

    def get_perform_list(self):
        # 현재 공연중 -> 공연 리스트 먼저
        perform_list = []
        for i in [1, 2, 3, 5]:   
            query = f"http://www.playdb.co.kr/playdb/playdblist.asp?sReqMainCategory=00000{i}&sReqSubCategory=&sReqDistrict=&sReqTab=2&sPlayType=2&sStartYear=&sSelectType=1" # 사이트 주소
            driver = webdriver.Chrome()
            driver.get(query)
            driver.implicitly_wait(3)

            c = '//*[@id="contents"]/div[1]/ul/li[{}]/a/img'.format(i) # 장르
            cc = driver.find_element(By.XPATH, c).get_attribute('alt')
                        
            page = 0

            while(True):
                try:
                    for j in range(1, 11): # 10개의 탭 존재
                        for k in range(1, 16): # 한 탭에 15개의 공연 존재
                            kk = 2*k + 1
                            
                            a = "/html/body/div[1]/div[2]/div[2]/table/tbody/tr[11]/td/table/tbody/tr[{}]/td/table/tbody/tr/td[1]/table/tbody/tr/td[3]/table/tbody/tr[1]/td/b/font/a".format(kk) # 제목
                            b = '//*[@id="contents"]/div[2]/table/tbody/tr[11]/td/table/tbody/tr[{}]/td/table/tbody/tr/td[1]/table/tbody/tr/td[3]/table/tbody/tr[1]/td/b/font/a'.format(kk) # url
                            
                            aa = driver.find_element(By.XPATH, a).text
                            bb = driver.find_element(By.XPATH, b).get_attribute('onclick')
                            
                            bb = re.sub(r'[^0-9]', '', bb)

                            perform_list.append({"제목":aa, "URL":bb, '장르':cc})

                        # 다음페이지 클릭
                        if (page==0 & j < 10):
                            botton = '//*[@id="contents"]/div[2]/table/tbody/tr[11]/td/table/tbody/tr[35]/td/a[{}]'.format(j)
                            driver.find_element(By.XPATH, botton).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                        elif (page > 0 & j < 10):
                            botton = '//*[@id="contents"]/div[2]/table/tbody/tr[11]/td/table/tbody/tr[35]/td/a[{}]'.format(j+1)
                            driver.find_element(By.XPATH, botton).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                        #10번 다음페이지
                        elif (page == 1 & j == 10):
                            botton_2 = '//*[@id="contents"]/div[2]/table/tbody/tr[11]/td/table/tbody/tr[35]/td/a[10]'
                            driver.find_element(By.XPATH, botton_2).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                        else:
                            botton_2 = '//*[@id="contents"]/div[2]/table/tbody/tr[11]/td/table/tbody/tr[35]/td/a[11]'
                            driver.find_element(By.XPATH, botton_2).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                    page += 1
                    print(page)
                except: # 더이상 없으면 멈춤
                    break

        for i in [4, 7]:      
            query = f"http://www.playdb.co.kr/playdb/playdblist.asp?sReqMainCategory=00000{i}&sReqSubCategory=&sReqDistrict=&sReqTab=2&sPlayType=2&sStartYear=&sSelectType=1" # 사이트 주소
            driver = webdriver.Chrome()
            driver.get(query)
            driver.implicitly_wait(5)

            c = '//*[@id="contents"]/div[1]/ul/li[{}]/a/img'.format(i) # 장르
            cc = driver.find_element(By.XPATH, c).get_attribute('alt')
                        
            page = 0

            while(True):
                try:
                    for j in range(1, 11): # 10개의 탭 존재
                        for k in range(1, 16): # 한 탭에 15개의 공연 존재
                            kk = 2*k + 1
                            
                            a = "/html/body/div[1]/div[2]/div[2]/table/tbody/tr[9]/td/table/tbody/tr[{}]/td/table/tbody/tr/td[1]/table/tbody/tr/td[3]/table/tbody/tr[1]/td/b/font/a".format(kk) # 제목
                            b = '//*[@id="contents"]/div[2]/table/tbody/tr[9]/td/table/tbody/tr[{}]/td/table/tbody/tr/td[1]/table/tbody/tr/td[3]/table/tbody/tr[1]/td/b/font/a'.format(kk) # url
                            
                            aa = driver.find_element(By.XPATH, a).text
                            bb = driver.find_element(By.XPATH, b).get_attribute('onclick')
                            
                            bb = re.sub(r'[^0-9]', '', bb)

                            perform_list.append({"제목":aa, "URL":bb, '장르':cc})
                        
                        # 다음페이지 클릭
                        if (page==0 & j < 10):
                            botton = '//*[@id="contents"]/div[2]/table/tbody/tr[9]/td/table/tbody/tr[35]/td/a[{}]'.format(j)
                            driver.find_element(By.XPATH, botton).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                        elif (page > 0 & j < 10):
                            botton = '//*[@id="contents"]/div[2]/table/tbody/tr[9]/td/table/tbody/tr[35]/td/a[{}]'.format(j+1)
                            driver.find_element(By.XPATH, botton).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                        #10번 다음페이지
                        elif (page == 1 & j == 10):
                            botton_2 = '//*[@id="contents"]/div[2]/table/tbody/tr[9]/td/table/tbody/tr[35]/td/a[10]'
                            driver.find_element(By.XPATH, botton_2).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                        else:
                            botton_2 = '//*[@id="contents"]/div[2]/table/tbody/tr[9]/td/table/tbody/tr[35]/td/a[11]'
                            driver.find_element(By.XPATH, botton_2).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                    page += 1
                            
                except: # 더이상 없으면 멈춤
                    break

        for i in [6]:      
            query = f"http://www.playdb.co.kr/playdb/playdblist.asp?sReqMainCategory=00000{i}&sReqSubCategory=&sReqDistrict=&sReqTab=2&sPlayType=2&sStartYear=&sSelectType=1" # 사이트 주소
            driver = webdriver.Chrome()
            driver.get(query)
            driver.implicitly_wait(5)

            c = '//*[@id="contents"]/div[1]/ul/li[{}]/a/img'.format(i) # 장르
            cc = driver.find_element(By.XPATH, c).get_attribute('alt')
                        
            page = 0

            while(True):
                try:
                    for j in range(1, 11): # 10개의 탭 존재
                        for k in range(1, 16): # 한 탭에 15개의 공연 존재
                            kk = 2*k + 1
                            
                            a = "/html/body/div[1]/div[2]/div[2]/table/tbody/tr[8]/td/table/tbody/tr[{}]/td/table/tbody/tr/td[1]/table/tbody/tr/td[3]/table/tbody/tr[1]/td/b/font/a".format(kk) # 제목
                            b = '//*[@id="contents"]/div[2]/table/tbody/tr[8]/td/table/tbody/tr[{}]/td/table/tbody/tr/td[1]/table/tbody/tr/td[3]/table/tbody/tr[1]/td/b/font/a'.format(kk) # url
                            
                            aa = driver.find_element(By.XPATH, a).text
                            bb = driver.find_element(By.XPATH, b).get_attribute('onclick')
                            
                            bb = re.sub(r'[^0-9]', '', bb)

                            perform_list.append({"제목":aa, "URL":bb, '장르':cc})
                        
                        # 다음페이지 클릭
                        if (page==0 & j < 10):
                            botton = '//*[@id="contents"]/div[2]/table/tbody/tr[8]/td/table/tbody/tr[35]/td/a[{}]'.format(j)
                            driver.find_element(By.XPATH, botton).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                        elif (page > 0 & j < 10):
                            botton = '//*[@id="contents"]/div[2]/table/tbody/tr[8]/td/table/tbody/tr[35]/td/a[{}]'.format(j+1)
                            driver.find_element(By.XPATH, botton).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                        #10번 다음페이지
                        elif (page == 1 & j == 10):
                            botton_2 = '//*[@id="contents"]/div[2]/table/tbody/tr[8]/td/table/tbody/tr[35]/td/a[10]'
                            driver.find_element(By.XPATH, botton_2).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                        else:
                            botton_2 = '//*[@id="contents"]/div[2]/table/tbody/tr[8]/td/table/tbody/tr[35]/td/a[11]'
                            driver.find_element(By.XPATH, botton_2).send_keys(Keys.ENTER)
                            driver.implicitly_wait(5)

                    page += 1
                            
                except: # 더이상 없으면 멈춤
                    break

        df = pd.DataFrame(perform_list)
        return df

    def get_perform_detail(self):

        # 빈 리스트 생성
        date = []
        place = []
        place_url = []
        image = []
        content = [] # 줄거리
        detail = [] # 상세정보
        info_url = []
        genre2 = []
        df = self.get_perform_list()
        # for문을 이용해 data의 링크에 하나씩 접근
        for k in tqdm(range(len(df))):
        # 공연 사이트 주소
            try:
                query = f"http://www.playdb.co.kr/playdb/playdbDetail.asp?sReqPlayno={df['URL'][k]}" # 사이트 주소
                driver = webdriver.Chrome()

                driver.get(query)
                driver.implicitly_wait(5)
            except:
                continue
            
            try:
                ur = driver.find_element(By.CSS_SELECTOR, '#wrap > div.pddetail > div.pddetail_info > div.detaillist > p > a').get_attribute('href')
            except:
                ur = '후기탭 없음'
            info_url.append(ur)

            # 공연소개 탭으로 이동(줄거리)
            tab = '//*[@alt="공연소개"]'
            a = driver.find_element(By.XPATH, tab)
            driver.execute_script("arguments[0].click();", a)
            driver.implicitly_wait(5)

            a = '//*[@id="wrap"]/div[3]/div[1]/div[2]/table/tbody/tr[2]/td[2]' # 기간
            b = '//*[@id="wrap"]/div[3]/div[1]/div[2]/table/tbody/tr[3]/td[2]/a' # 장소
            c = '//*[@id="wrap"]/div[3]/h2/img' # 이미지 주소
            d = '//*[@id="wrap"]/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[2]/a[2]' # 세부장르

            aa = driver.find_element(By.XPATH, a).text
            bb = driver.find_element(By.XPATH, b).text
            bb2 = driver.find_element(By.XPATH, b).get_attribute("href")
            cc = driver.find_element(By.XPATH, c).get_attribute('src')
            dd = driver.find_element(By.XPATH, d).text
            print(aa,bb,bb2,cc,dd)
            date.append(aa)
            place.append(bb)
            place_url.append(bb2)
            image.append(cc)
            genre2.append(dd)

            driver.switch_to.frame("iFrmContent") #iframe 페이지로 전환
            cont = driver.find_elements(By.CLASS_NAME, 'news')
            
            if cont != []:
                dd = cont[0].text # 작품설명
                if len(cont) > 1: # 줄거리 있는 경우
                    ff = cont[1].text # 줄거리
                else:
                    ff = "줄거리 없음"
            else:
                dd = "작품설명 없음"
                ff = "줄거리 없음"
                
            driver.close() 

            detail.append(dd)
            content.append(ff)
        
        df['기간'] = date
        df['장소'] = place
        df['장소url'] = place_url
        df['세부장르'] = genre2
        df['이미지url'] = image
        df['줄거리'] = content
        df['작품설명'] = detail
        df['상세url'] = info_url

        return df

    def get_perform_address(self):
        
        df = self.get_perform_detail()
        address = []
        # for문을 이용해 data의 링크에 하나씩 접근
        for k in tqdm(range(len(df))):
        # 공연 사이트 주소
            try:
                query = f"{df['장소url'][k]}" # 사이트 주소
                driver = webdriver.Chrome()

                driver.get(query)
                driver.implicitly_wait(5)
            except:
                address.append("주소정보없음")
                continue

            try:
                a = '//*[@id="Keyword"]/table/tbody/tr[3]/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td'
                add = driver.find_element(By.XPATH, a).text
                add = add.replace('주소: ', "")
                address.append(add)
            except:
                address.append("주소정보없음")
                continue

        df['주소'] = address
        df.drop_duplicates(inplace=True) # 전체열이 중복되는 공연 정보 없애기
        df.reset_index(drop=True, inplace=True)
        return df


    ### 후기, 후기유무열 추출(최종) -> 전처리 후 L-LDA에 사용

    # 예매안내 관련 팝업 닫는 함수
    def check_exists_by_element(self,driver,by,name):
        try:
            driver.find_element(by, name)
        except NoSuchElementException:
            return False
        return True

    def get_perform_review(self):
        
        # 통합 URL + 인덱스 파일 이용해서 추출할 부분만 가져오기
        data = self.get_perform_address()
        empty_df = pd.DataFrame()
        review_ox = []
        # for문을 이용해 data의 링크에 하나씩 접근

        for k in tqdm(range(len(data))):
            # 별점 + 텍스트 + 날짜 + 공연코드 빈 리스트 생성
            ratings =[]
            texts =[]
            showcodes = []
            places = []
            dates = []
            images = []
            info_url = []
            genre2 = []
            address = []
            review_ox = []
            # 공연 사이트 주소 + 상품 정보 없으면 넘어가는 코드 (try-except 이용)
            try:
                query = f"{data['상세url'][k]}" # 사이트 주소
                driver = webdriver.Chrome()
                driver.get(query)
                driver.implicitly_wait(5)
                # 예매안내 관련 팝업이 있다면 팝업 닫기
                ticketingInfo_check = self.check_exists_by_element(driver, By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div[3]/button")
                if ticketingInfo_check:
                    driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div[3]/button").click()
                driver.implicitly_wait(5)
            except: # 상품 정보가 없어서 에러가 나면 해당 공연 넘기기
                ratings.append('X')
                texts.append('X')
                showcodes.append(data['제목'][k])
                places.append(data['장소'][k])
                address.append(data['주소'][k])
                dates.append(data['기간'][k])
                images.append(data['이미지url'][k])
                info_url.append(data['상세url'][k])
                genre2.append(data['세부장르'][k])
                review_ox.append('X')
                dic ={'제목':showcodes, 'rating':ratings, 'text':texts, '장소':places, '주소':address, '기간':dates, '이미지url':images, '상세url':info_url, '세부장르':genre2, '후기유무':review_ox}
                df = pd.DataFrame(dic)
                empty_df = empty_df.append(df)
                driver.close()
                continue
                
            # 연극 관람후기로 이동
            try: # 리뷰 탭 없는 경우 다음 공연으로 이동
                elem = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/nav/div/div/ul/li[4]/a")
            except:
                ratings.append('X')
                texts.append('X')
                showcodes.append(data['제목'][k])
                places.append(data['장소'][k])
                address.append(data['주소'][k])
                dates.append(data['기간'][k])
                images.append(data['이미지url'][k])
                info_url.append(data['상세url'][k])
                genre2.append(data['세부장르'][k])
                review_ox.append('X')
                dic ={'제목':showcodes, 'rating':ratings, 'text':texts, '장소':places, '주소':address, '기간':dates, '이미지url':images, '상세url':info_url, '세부장르':genre2, '후기유무':review_ox}
                df = pd.DataFrame(dic)
                empty_df = empty_df.append(df)
                continue

            # 리뷰페이지로 이동 가끔 3번째에 있을때도 있음
            dataTarget = elem.get_attribute("data-target")
            if(dataTarget != "REVIEW"):
                elem = driver.find_element(By.XPATH,"/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/nav/div/div/ul/li[3]/a")
            elem.send_keys(Keys.ENTER)
            driver.implicitly_wait(5)
            # 리뷰 개수 확인
            review_num = driver.find_element(By.CLASS_NAME, "countNum").text
            # 999+ 개의 리뷰인 경우, + 삭제
            if '+' in review_num:
                review_num = review_num.replace('+', '')
            if int(review_num) == 0:
                ratings.append('X')
                texts.append('X')
                showcodes.append(data['제목'][k])
                places.append(data['장소'][k])
                address.append(data['주소'][k])
                dates.append(data['기간'][k])
                images.append(data['이미지url'][k])
                info_url.append(data['상세url'][k])
                genre2.append(data['세부장르'][k])
                review_ox.append('X')
                dic ={'제목':showcodes, 'rating':ratings, 'text':texts, '장소':places, '주소':address, '기간':dates, '이미지url':images, '상세url':info_url, '세부장르':genre2, '후기유무':review_ox}
                df = pd.DataFrame(dic)
                empty_df = empty_df.append(df)
                driver.close()
                continue
            # 베스트 리뷰 / 리뷰가 나눠져 있음
            # 클래스에서 베스트를 찾고 없으면 빈값을 내보냄
            try:
                best = driver.find_element(By.CLASS_NAME, "bastBadge").text
            except:
                best = ""
            tmp = True # 아래에서 리뷰 데이터 1000개 이상이면 tmp = False로 바꾸기
            # 베스트 리뷰가 없는 경우
            if(best != "베스트"):
                while(True):
                    try: # try문은 더이상 리뷰가 없을 때 오류가 발생하기 때문에 넣어주어야 함
                        for j in range(1,11): # 1~10페이지까지
                            for i in range(1,16): # 한 페이지내에 리뷰 15개 존재
                                a= "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[3]/ul/li["+str(i)+"]/div/div[1]/div[1]/div/div[1]/div" # 별점
                                b= "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[3]/ul/li["+str(i)+"]/div/div[2]/div[1]" # 리뷰
                                rating = driver.find_element(By.XPATH, a).get_attribute("data-star") # 별점 가져오기
                                text = driver.find_element(By.XPATH, b).text # 리뷰 가져오기
                                ratings.append(rating)
                                texts.append(text)
                                showcodes.append(data['제목'][k])
                                places.append(data['장소'][k])
                                address.append(data['주소'][k])
                                dates.append(data['기간'][k])
                                images.append(data['이미지url'][k])
                                info_url.append(data['상세url'][k])
                                genre2.append(data['세부장르'][k])
                                review_ox.append('O')
                                if len(texts) >= 1000: # 리뷰 데이터 1000개 넘어가면 tmp = False로 하여 안쪽 for문 탈출
                                    tmp = False
                                    break
                            if tmp == False: # tmp = False이면 바깥쪽 for문도 탈출
                                break
                            #다음페이지 클릭
                            if(j<10):
                                botton = "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/ol/li["+str(j+1)+"]/a"
                                elem = driver.find_element(By.XPATH, botton)
                                elem.send_keys(Keys.ENTER)
                                driver.implicitly_wait(5)
                            else:
                                #10번 다음페이지
                                elem = driver.find_element(By.CLASS_NAME, "pageNextBtn.pageArrow")
                                elem.send_keys(Keys.ENTER)
                                driver.implicitly_wait(5)
                    except: # 리뷰가 더이상 없으면 멈춤
                        break
                    else: # 그것도 아니고 리뷰 텍스트가 1000개 이상이면 멈춤
                        if tmp == False:
                            break
            # 베스트리뷰가 있는 경우 (코드는 베스트리뷰가 없는 경우와 동일)
            else:
                while(True):
                    try:
                        for j in range(1,11):
                            for i in range(1,16):
                                a= "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[4]/ul/li["+str(i)+"]/div/div[1]/div[1]/div/div[1]/div"
                                b= "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[4]/ul/li["+str(i)+"]/div/div[2]/div[1]"
                                rating = driver.find_element(By.XPATH, a).get_attribute("data-star")
                                text = driver.find_element(By.XPATH, b).text
                                ratings.append(rating)
                                texts.append(text)
                                showcodes.append(data['제목'][k])
                                places.append(data['장소'][k])
                                address.append(data['주소'][k])
                                dates.append(data['기간'][k])
                                images.append(data['이미지url'][k])
                                info_url.append(data['상세url'][k])
                                genre2.append(data['세부장르'][k])
                                review_ox.append('O')
                                if len(texts) >= 1000:
                                    tmp = False
                                    break
                            if tmp == False:
                                break
                            #다음페이지 클릭
                            if(j<10):
                                botton = "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[4]/div[2]/ol/li["+str(j+1)+"]/a"
                                elem = driver.find_element(By.XPATH, botton)
                                elem.send_keys(Keys.ENTER)
                                driver.implicitly_wait(5)
                            else:
                                #10번 다음페이지
                                elem = driver.find_element(By.CLASS_NAME, "pageNextBtn.pageArrow")
                                elem.send_keys(Keys.ENTER)
                                driver.implicitly_wait(5)
                    except:
                        break
                    else:
                        if tmp == False:
                            break

            driver.close()
            
            dic ={'제목':showcodes, 'rating':ratings, 'text':texts, '장소':places, '주소':address, '기간':dates, '이미지URL':images, '상세URL':info_url, '세부장르':genre2, '후기유무':review_ox}
            df = pd.DataFrame(dic)
            empty_df = empty_df.append(df)
            empty_df = pd.DataFrame(empty_df)
        
        now = self.week_no()
        #empty_df.to_csv(f'./Crawling/data/{now}_현재공연중_후기.csv',index=False)
        message = {'content':f'{now}_현재공연중 후기 크롤링을 완료했습니다.'}
        self.send_message(message)
        
        return empty_df

    ### (최종) -> 유사도계산에 사용할 파일

    def get_perform_contents(self):
        df_ad = self.get_perform_address()
        df_ad.drop_duplicates(inplace=True)
        df_ad.reset_index(drop=True, inplace=True)

        df = self.get_perform_review()
        df2 = df.copy()
        df2.drop(['text', 'rating'], axis=1, inplace=True)
        df2.drop_duplicates(inplace=True)
        df2.reset_index(drop=True, inplace=True)
        df2['줄거리'] = df_ad['줄거리']
        df2['작품설명'] = df_ad['작품설명']
        df2['작품설명'] = df2['작품설명'].apply(lambda x : x.replace('"',""))
        df2['작품설명'] = df2['작품설명'].apply(lambda x : x.replace("'",""))
        df2['줄거리'] = df2['줄거리'].apply(lambda x : x.replace('"',""))
        df2['줄거리'] = df2['줄거리'].apply(lambda x : x.replace("'",""))

        now = self.week_no()
        #df2.to_csv(f'./Crawling/data/{now}_현재공연중_줄거리.csv',index=False)
        message = {'content':f'{now}_현재공연중 줄거리 크롤링을 완료했습니다.'}
        self.send_message(message)
        
        return df, df2
