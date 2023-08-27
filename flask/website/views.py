from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import pandas as pd
from func.open import open_info, open_info_all, week_no

# 블루프린트를 이용하면 App의 모든 url을 한 곳에서 관리하지 않아도 됨
# 즉, 여러 파일에서 url에 대한 정의를 선언 가능
# 이곳저곳에 뿌려진 url의 정의를 수집하여 한 곳으로 모아줌
views = Blueprint('views', __name__)

# 뷰를 정의하여 보여질 페이지와 경로를 정의
# 로그인 여부에 따른 뷰의 분기 작업 -> 로그인 여부 따라 페이지 다르게
@views.route('/')
def home():
    open = open_info()
    return render_template('home.html', open = open)

# 오픈 정보 페이지
@views.route('/open')
def open_all():
    open = open_info_all()
    week = week_no()
    return render_template('open.html', open = open, week = week)

# 큐레이션 페이지
@views.route('/curation')
def curation():
    return render_template('curation.html')

# 유형 테스트 페이지
@views.route('/test')
def test():
    return render_template('test.html')

# 유형 테스트 페이지
@views.route('/service')
def service():
    return render_template('service.html')