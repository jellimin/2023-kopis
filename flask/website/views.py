from flask import Blueprint, render_template
from flask_login import login_required, current_user

# 블루프린트를 이용하면 App의 모든 url을 한 곳에서 관리하지 않아도 됨
# 즉, 여러 파일에서 url에 대한 정의를 선언 가능
# 이곳저곳에 뿌려진 url의 정의를 수집하여 한 곳으로 모아줌
views = Blueprint('views', __name__)

# 뷰를 정의하여 보여질 페이지와 경로를 정의
# 로그인 여부에 따른 뷰의 분기 작업 -> 로그인 여부 따라 페이지 다르게
@views.route('/')
@login_required
def home():
    return render_template('home.html')