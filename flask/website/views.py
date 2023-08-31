from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required, current_user
import pandas as pd
from func.open import open_info, open_info_all, week_no
from func.like import main_open, open_open, update_like_in

# 블루프린트를 이용하면 App의 모든 url을 한 곳에서 관리하지 않아도 됨
# 즉, 여러 파일에서 url에 대한 정의를 선언 가능
# 이곳저곳에 뿌려진 url의 정의를 수집하여 한 곳으로 모아줌
views = Blueprint('views', __name__)

# 뷰를 정의하여 보여질 페이지와 경로를 정의
# 1. 홈 페이지
@views.route('/')
def home():

    ### OpenInfo 플로팅
    opens = open_info()
    
    # main에 띄워진 공연 id 가져오기
    main_open_id = []
    for open in opens:
        main_open_id.append(open['_id'])

    # 좋아요 관련
    try:
        if session['u_id']: # 로그인한 이력이 있는 경우
            user_info = session['u_id']

            opens = main_open(main_open_id, opens, user_info)

            return render_template('home.html', open = opens, user_info = user_info)
    except:
        return render_template('home.html', open = opens)

# 2. 오픈 정보 페이지
@views.route('/open')
def open_all():
    # 오픈 정보 보여주기
    opens = open_info_all()
    week = week_no()

    # 좋아요 관련
    try:
        if session['u_id']: # 로그인한 이력이 있는 경우
            user_info = session['u_id']

            opens = open_open(opens, user_info)

            return render_template('open.html', open = opens, week = week, user_info = user_info)
    except:
        return render_template('open.html', open = opens, week = week)

# 3. 메인 오픈 정보 좋아요
@views.route('/update_like', methods=['POST'])
def main_update_like():
        count = update_like_in()
        return jsonify({"result": "success", 'msg': 'updated', "count": count})

# 4. 더보기 오픈 정보 좋아요
@views.route('/open/update_like', methods=['POST'])
def update_like():
        count = update_like_in()
        return jsonify({"result": "success", 'msg': 'updated', "count": count})

# 5. 큐레이션 페이지
@views.route('/curation')
def curation():
    return render_template('curation.html')

# 6. 유형 테스트 페이지
@views.route('/test')
def test():
    return render_template('test.html')

# 7. 유형 테스트 페이지
@views.route('/service')
def service():
    return render_template('service.html')