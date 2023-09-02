# 메인페이지 + 메인페이지에 연결된 페이지들

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required, current_user
import pandas as pd
from func.main_fun import open_info, open_info_all, hot_info, hot_info_all, week_no
from func.like_fun import main_open, main_hot, open_open, hot_hot, update_like_in, update_like_in_hot

# 블루프린트를 이용하면 App의 모든 url을 한 곳에서 관리하지 않아도 됨
# 즉, 여러 파일에서 url에 대한 정의를 선언 가능
# 이곳저곳에 뿌려진 url의 정의를 수집하여 한 곳으로 모아줌
views = Blueprint('views', __name__)

# 뷰를 정의하여 보여질 페이지와 경로를 정의
# 1. 홈 페이지
@views.route('/')
def home():

    ### HotInfo 플로팅
    hots = hot_info()

    ### OpenInfo 플로팅
    opens = open_info()
    
    # main에 띄워진 오픈공연 id 가져오기
    main_open_id = []
    for open in opens:
        main_open_id.append(open['_id'])

    # main에 띄워진 핫공연 id 가져오기
    main_hot_id = []
    for hot in hots:
        main_hot_id.append(hot['_id'])

    # 좋아요 관련
    try:
        if session['u_id']: # 로그인한 이력이 있는 경우
            user_info = session['u_id']

            opens = main_open(main_open_id, opens, user_info)
            hots = main_hot(main_hot_id, hots, user_info)

            return render_template('home.html', open = opens, hot = hots, user_info = user_info)
    except:
        return render_template('home.html', open = opens, hot = hots)

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
    
# 3. 핫 정보 페이지
@views.route('/hot')
def hot_all():
    # 오픈 정보 보여주기
    hots = hot_info_all()
    week = week_no()

    # 좋아요 관련
    try:
        if session['u_id']: # 로그인한 이력이 있는 경우
            user_info = session['u_id']

            hots = hot_hot(hots, user_info)

            return render_template('hot.html', hot = hots, week = week, user_info = user_info)
    except:
        return render_template('hot.html', hot = hots, week = week)

# 4. 메인페이지 오픈 정보 좋아요
@views.route('/update_like', methods=['POST'])
def main_open_update_like():
        count = update_like_in()
        return jsonify({"result": "success", 'msg': 'updated', "count": count})

# 5. 더보기 오픈 정보 좋아요
@views.route('/open/update_like', methods=['POST'])
def open_update_like():
        count = update_like_in()
        return jsonify({"result": "success", 'msg': 'updated', "count": count})

# 6. 메인페이지 핫 정보 좋아요
@views.route('/update_like_hot', methods=['POST'])
def main_hot_update_like():
        count = update_like_in_hot()
        return jsonify({"result": "success", 'msg': 'updated', "count": count})

# 7. 더보기 핫 정보 좋아요
@views.route('/hot/update_like', methods=['POST'])
def hot_update_like():
        count = update_like_in_hot()
        return jsonify({"result": "success", 'msg': 'updated', "count": count})

# 8. 큐레이션 페이지
@views.route('/curation')
def curation():
    return render_template('curation.html')

# 9. 유형 테스트 페이지
@views.route('/test')
def test():
    return render_template('test.html')

# 10. 유형 테스트 페이지
@views.route('/service')
def service():
    return render_template('service.html')