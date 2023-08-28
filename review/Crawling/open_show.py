# 필요한 모듈 불러오기
import re
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
from tqdm import tqdm
from tqdm import trange
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import warnings
warnings.filterwarnings('ignore')
chrome_options = Options()
chrome_options.add_experimental_option('detach', True) # 자동 창꺼짐 방지

# [기간/줄거리/장소/이미지 url/인터파크 url] 추출
# 1. 현재 공연중
data1 = pd.read_csv("./data/공연중_list.csv")[:1]

# 빈 리스트 생성
date = []
place = []
image = []
actor = []
content = [] # 줄거리
detail = [] # 상세정보
url = [] # 후기 추출을 위한 인터파크  url

# for문을 이용해 data의 링크에 하나씩 접근
for k in tqdm(range(len(data1))):
  # 공연 사이트 주소
  try:
    query = f"http://www.playdb.co.kr/playdb/playdbDetail.asp?sReqPlayno={data1['url'][k]}" # 사이트 주소
    service = Service(executable_path = "./chromedriver.exe" )
    driver = webdriver.Chrome(service = service, options=chrome_options)

    driver.get(query)
    driver.implicitly_wait(5)
  except:
      continue
  
  try:
    ur = driver.find_element(By.CSS_SELECTOR, '#wrap > div.pddetail > div.pddetail_info > div.detaillist > p > a').get_attribute('href')
  except:
    ur = '후기탭 없음'
  url.append(ur)

  # 공연소개 탭으로 이동(줄거리)
  tab = '//*[@alt="공연소개"]'
  a = driver.find_element(By.XPATH, tab)
  driver.execute_script("arguments[0].click();", a)
  driver.implicitly_wait(5)

  a = '//*[@id="wrap"]/div[3]/div[1]/div[2]/table/tbody/tr[2]/td[2]' # 기간
  b = '//*[@id="wrap"]/div[3]/div[1]/div[2]/table/tbody/tr[3]/td[2]/a' # 장소
  c = '//*[@id="wrap"]/div[3]/h2/img' # 이미지 주소

  temp = [] # 배우
  while(True):
    try:
      for p in range(1, 6):
        e = f'//*[@id="wrap"]/div[3]/div[1]/div[2]/table/tbody/tr[4]/td[2]/a[{p}]'
        ee = driver.find_element(By.XPATH, e).text
        temp.append(ee)
      temp = ",".join(temp)
    except:
      break
  actor.append(temp)

  aa = driver.find_element(By.XPATH, a).text
  bb = driver.find_element(By.XPATH, b).text
  cc = driver.find_element(By.XPATH, c).get_attribute('src')
  
  driver.switch_to.frame("iFrmContent") #iframe 페이지로 전환

  cont = driver.find_elements(By.CLASS_NAME, 'news')
  dd = cont[0].text # 작품설명
  if len(cont) > 1: # 줄거리 있는 경우
    ee = cont[1].text # 줄거리
  else:
    ee = '줄거리없음'

  date.append(aa)
  place.append(bb)
  image.append(cc) 

data1['기간'] = date
data1['장소'] = place
data1['이미지url'] = image
data1['배우'] = actor
data1['후기용url'] = url

# data1.to_csv("공연중_후기용_list.csv", index=False)