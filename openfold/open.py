# 필요한 라이브러리 로딩
import requests
import time
import re
import lxml
import pandas as pd
import numpy as np
import os
import sys
import urllib.request
import warnings
import ssl
import pymysql
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime
from datetime import datetime
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.error import HTTPError, URLError
import chromedriver_autoinstaller
import warnings
warnings.filterwarnings('ignore')

class OpenCrawler:
    def __init__(self):
        print('오픈 크롤러를 생성했습니다.')

    # 디스코드 알림 메시지 
    def send_message(self, message):
        requests.post("https://discord.com/api/webhooks/1140278554609844264/aUubW_3WgjV_hwzVcQPjeWrhQzm1lZBS481VVIHqO7Cq_4A7E0xcJ2FPKsxRtaWy6R1r",
                      data=message)

    # 크롬 드라이버 생성
    def chrome_driver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        chrome_ver = chromedriver_autoinstaller.get_chrome_version()  # 크롬 브라우저 버전 확인하기
        print(f'크롬 현재 버전: {chrome_ver}')  # 116.0.5359.125
        chromedriver = f'./{chrome_ver.split(".")[0]}/chromedriver.exe'
        if not os.path.exists(chromedriver):
            os.makedirs(os.path.dirname(chromedriver), exist_ok=True)
            res = chromedriver_autoinstaller.install(True)  # 크롬 드라이버 다운로드
            if res:
                print(f'크롬 드라이버 설치 완료!({chrome_ver.split(".")[0]} 버전)')
            else:
                print(f'크롬 드라이버 설치 오류 발생!({chrome_ver.split(".")[0]} 버전)')
        driver = webdriver.Chrome(chromedriver, options=options)
        return driver
    
    ### (1) 인터파크 오픈정보 크롤러
    def Interpark(self, query):
        # 크롬 드라이버 불러오기
        driver = self.chrome_driver()
        driver.get(query)
        driver.implicitly_wait(60)

        #iframe 페이지로 전환
        driver.switch_to.frame("iFrmNotice")

        # 오픈일 순 버튼 클릭
        elem = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[2]/ul/li[3]/a")
        elem.send_keys(Keys.ENTER)

        # 10페이지 후 다음 페이지 버튼 기본값 설정
        j = 1 

        while True:
            try:
                for i in range(0, 10): # 1~10 페이지까지
                    # 티켓 오픈 정보가 저장되어 있는 테이블 선택
                    table = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/table")

                    if i == 0:
                        
                        column = []

                        # thead, 컬럼
                        thead = table.find_element_by_tag_name("thead")
                        # thead > tr > th
                        thead_th = thead.find_element_by_tag_name("tr").find_elements_by_tag_name("th")
                        for idx, th in enumerate(thead_th):
                            column.append(th.text)
                            if idx == 1:
                                column.append('URL')

                        df = pd.DataFrame(columns = column)

                    
                    # tbody, 각 행들
                    tbody = table.find_element_by_tag_name("tbody")

                    # tbody > tr > td
                    for tr in tbody.find_elements_by_tag_name("tr"):
                        row = []
                        for idx, td in enumerate(tr.find_elements_by_tag_name("td")):
                            row.append(td.get_attribute("innerText"))
                            if idx == 1:
                                url = td.find_element(By.TAG_NAME, "a").get_attribute("href")
                                row.append(url)
                        temp = pd.DataFrame([row], columns = column)
                        df = pd.concat([df, temp], ignore_index = True)

                    # 다음페이지 클릭
                    if(i<10):
                        botton = "/html/body/div/div/div[2]/div[2]/span[1]/a["+str(i+1)+"]"
                        elem = driver.find_element(By.XPATH, botton)
                        elem.send_keys(Keys.ENTER)
                        driver.implicitly_wait(5)
                    else:
                        #10번 다음페이지 (처음 버튼이 2부터 시작)
                        botton = "/html/body/div/div/div[2]/div[2]/a["+str(j+1)+"]"
                        elem = driver.find_element(By.XPATH, botton)
                        elem.send_keys(Keys.ENTER)
                        driver.implicitly_wait(5)
                        j += 1
            except:
                break

        # 이미지 URL 가져오기
        for idx, query in enumerate(df['URL']):
            try:
                response = requests.get(query)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                image = soup.select('#wrapBody > div > div > div.board > div.detail_top > div.info > span > img')[0]['src']
                df.loc[idx, '이미지URL'] = image
            except:
                continue
        else:
            message = {'content':'인터파크 오픈정보 크롤링을 완료했습니다.'}
            self.send_message(message)
            return df[['제목', 'URL', '이미지URL', '티켓오픈일시']]

    ### (2) 티켓링크 오픈정보 크롤러
    def get_detailinfo(self, driver):
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
            data.append({'제목': title.strip(), '티켓오픈일시': date, 'URL': href.strip()})
        df = pd.DataFrame(data)
        return df
    
    def get_openinfo(self, driver, query):
        result = pd.DataFrame()

        driver.get(query)
        driver.implicitly_wait(5)
        
        for i in range(4,14):
            df = self.get_detailinfo(driver)
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
    
    def get_image_info(self, driver, df):
        img_urls = []
        for url in df['URL']:
            try:
                driver.get(url)
                driver.implicitly_wait(3)
                url_tag = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/dl/dt/dl/dd[1]/img').get_attribute("src")
                img_urls.append(url_tag)
            except:
                img_urls.append(np.NaN)
        df['이미지URL'] = img_urls

        return df

    def Ticketlink(self, query):
        ssl._create_default_https_context = ssl._create_unverified_context

        # 크롬 드라이버 불러오기
        driver = self.chrome_driver()
        tmp = self.get_openinfo(driver, query)
        df = self.get_image_info(driver, tmp)

        message = {'content':'인터파크 오픈정보 크롤링을 완료했습니다.'}
        self.send_message(message)

        return df[['제목', 'URL', '이미지URL', '티켓오픈일시']]
        
    ### (3) 예스24 오픈정보 크롤러
    def Yes24(self, query):
        # 크롬 드라이버 불러오기
        driver = self.chrome_driver()
        driver.get(query)
        driver.implicitly_wait(60)

        # 팝업창 닫기
        tabs = driver.window_handles
        while len(tabs) != 1:
            driver.switch_to.window(tabs[1])
            driver.close()
        driver.switch_to.window(tabs[0])

        ## 티켓오픈 더보기 + 버튼 클릭 
        driver.find_element(By.XPATH, '//*[@id="mainForm"]/section[2]/a').click()
        #elem.send_keys(Keys.ENTER)

        ## 오픈일순으로 정렬
        driver.find_element(By.XPATH, '//*[@id="SelectOrder"]/a[2]').click()

        # 구분 + 공연제목 + 티켓오픈일시 + URL + 이미지 URL 빈 리스트 생성
        title = []
        dates = []
        url = []
        image = []

        while(True):
            try:
                for j in range(1, 11):
                    for i in range(1, 21): # 한 페이지 내에 공연 20개 존재
                        page = '//*[@id="BoardList"]/div/table/tbody/tr[{}]/td[2]/a'.format(i+1)
                        driver.find_element(By.XPATH, page).click()
                        time.sleep(3)

                        # a = "/html/body/div[5]/div[2]/div[1]/span" # 구분
                        b = '//*[@id="NoticeRead"]/div[3]/div/div[2]/p' # 공연제목
                        c = '//*[@id="title1"]' # 티켓오픈일시
                        # d = "/html/body/div[5]/div[1]/div[4]/div/table/tbody/tr[2]/td[2]/a" # URL
                        e = '//*[@id="NoticeRead"]/div[3]/div/div[1]/img' # 이미지 URL

                        # aa = driver.find_element(By.XPATH, a).text
                        bb = driver.find_element(By.XPATH, b).text
                        cc = driver.find_element(By.XPATH, c).text
                        dd = driver.find_element(By.XPATH, page).get_attribute('href')
                        ee = driver.find_element(By.XPATH, e).get_attribute('src')

                        title.append(bb)
                        dates.append(cc)
                        url.append(dd)
                        image.append(ee)
                        
                        driver.back()
                        time.sleep(3)
            except:
                print(f'{str(i)}번째 오류발생')
                break

        dict = {'제목':title, '티켓오픈일시':dates, 'URL':url, '이미지URL':image}
        result = pd.DataFrame(dict)

        def clean(x):
            x = x.replace('단독판매', '')
            return x

        result['제목'] = result['제목'].apply(lambda x: clean(x))

        message = {'content':'인터파크 오픈정보 크롤링을 완료했습니다.'}
        self.send_message(message)
        
        return result[['제목', 'URL', '이미지URL', '티켓오픈일시']]