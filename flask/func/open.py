import pandas as pd
path = 'C:/Users/alsru/Desktop/Project/Flask_git/2023-kopis/flask/website/data/interpark_open_data.csv'
def open_info():
    
    df = pd.read_csv(path)
    df = df.loc[:5, ['제목', 'URL', '티켓오픈일시', '이미지URL']]
    open = []
    for i in range(len(df)):
        title = df.loc[i, '제목']
        url = df.loc[i, 'URL']
        date = df.loc[i, '티켓오픈일시']
        image = df.loc[i, '이미지URL']
        open_info = {
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image
        }
        open.append(open_info)
    return open

def open_info_all():
    df = pd.read_csv('C:/Users/pmy49/OneDrive/바탕 화면/flask/website/data/interpark_open_data.csv')
    df = df[['제목', 'URL', '티켓오픈일시', '이미지URL']]
    open = []
    for i in range(len(df)):
        title = df.loc[i, '제목']
        url = df.loc[i, 'URL']
        date = df.loc[i, '티켓오픈일시']
        image = df.loc[i, '이미지URL']
        open_info = {
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image
        }
        open.append(open_info)
    return open

from datetime import datetime 
from datetime import timedelta

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