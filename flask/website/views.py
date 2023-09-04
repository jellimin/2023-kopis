# 메인페이지 + 메인페이지에 연결된 페이지들

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
# from flask_login import login_required, current_user
import pandas as pd
from func.main_fun import open_info, open_info_all, hot_info, hot_info_all, week_no
from func.like_fun import main_open, main_hot, open_open, hot_hot, update_like_in, update_like_in_hot
# from flask_paginate import Pagination, get_page_args
from func.search import uniq_keyword, search_keyword1, search_keyword2, search_keyword3, search_keyword4, search_keyword5, search_keyword6, search_keyword1_6, search_keyword2_6,search_keyword3_6,search_keyword4_6,search_keyword5_6,search_keyword6_6


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

    ### ShowInfo 플로팅
    keyword = uniq_keyword()
    keyword1 = search_keyword1_6()
    keyword2 = search_keyword2_6()
    keyword3 = search_keyword3_6()
    keyword4 = search_keyword4_6()
    keyword5 = search_keyword5_6()
    keyword6 = search_keyword6_6()

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

            return render_template('home.html', open = opens, hot = hots, keyword = keyword, user_info = user_info)
    except:
        return render_template('home.html', open = opens, hot = hots, keyword = keyword, keyword1=keyword1, keyword2=keyword2, keyword3=keyword3, keyword4=keyword4, keyword5=keyword5, keyword6=keyword6)

# 2. 오픈 정보 페이지
@views.route('/open')
def open_all():
    # 주차 정보 보여주기
    week = week_no()

    # 페이지네이션 관련
    per_page = 24
    page, _, offset = get_page_args(per_page = per_page)
    
    from . import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select count(*) from KEYWIDB.OpenInfo")
    total = cursor.fetchone()[0]
    cursor.execute("select * from KEYWIDB.OpenInfo LIMIT %s OFFSET %s;", (per_page, offset))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    opens = []
    for i in range(len(data)):
        id = data[i][0]
        title = data[i][1]
        url = data[i][2]
        date = data[i][4]
        image = data[i][3]
        open_info = {
            '_id' : id,
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image
        }
        opens.append(open_info)

    # 좋아요 관련
    try:
        if session['u_id']: # 로그인한 이력이 있는 경우
            user_info = session['u_id']

            opens = open_open(opens, user_info)

            return render_template('open.html', 
                                   open = opens, week = week, user_info = user_info, 
                                   pagination=Pagination(page=page,  # 지금 우리가 보여줄 페이지는 1 또는 2, 3, 4, ... 페이지인데,
                                                        total=total,  # 총 몇 개의 포스트인지를 미리 알려주고,
                                                        per_page=per_page,  # 한 페이지당 몇 개의 포스트를 보여줄지 알려주고,
                                                        prev_label="<<",  # 전 페이지와,
                                                        next_label=">>",  # 후 페이지로 가는 링크의 버튼 모양을 알려주고,
                                                        format_total=True,  # 총 몇 개의 포스트 중 몇 개의 포스트를 보여주고있는지 시각화,
                                                        ),
                                   search=True,  # 페이지 검색 기능을 주고,
                                   bs_version=5,  # Bootstrap 사용시 이를 활용할 수 있게 버전을 알려줍니다.
                                   )
    except:
        return render_template('open.html', open = opens, week = week,
                                            pagination=Pagination(page=page,  # 지금 우리가 보여줄 페이지는 1 또는 2, 3, 4, ... 페이지인데,
                                                        total=total,  # 총 몇 개의 포스트인지를 미리 알려주고,
                                                        per_page=per_page,  # 한 페이지당 몇 개의 포스트를 보여줄지 알려주고,
                                                        prev_label="<<",  # 전 페이지와,
                                                        next_label=">>",  # 후 페이지로 가는 링크의 버튼 모양을 알려주고,
                                                        format_total=True,  # 총 몇 개의 포스트 중 몇 개의 포스트를 보여주고있는지 시각화,
                                                        ),
                                search=True,  # 페이지 검색 기능을 주고,
                                bs_version=5,  # Bootstrap 사용시 이를 활용할 수 있게 버전을 알려줍니다.
                                )
    
# 3. 핫 정보 페이지
@views.route('/hot')
def hot_all():
    # 주차 정보 보여주기
    week = week_no()

    # 페이지네이션 관련
    per_page = 24
    page, _, offset = get_page_args(per_page = per_page)
    
    from . import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select count(*) from KEYWIDB.HotInfo")
    total = cursor.fetchone()[0]
    cursor.execute("select id, concat('[', category, ' ', cont_name, ' ', '와/과 유사한', ']', ' ', show_name) as title, show_url, show_date, img_url from KEYWIDB.HotInfo LIMIT %s OFFSET %s;", (per_page, offset))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    hots = []
    for i in range(len(data)):
        id = data[i][0]
        title = data[i][1]
        url = data[i][2]
        date = data[i][3]
        image = data[i][4]
        hot_info = {
            '_id' : id,
            'title' : title,
            'url' : url,
            'date' : date,
            'image' : image
        }
        hots.append(hot_info)

    # 좋아요 관련
    try:
        if session['u_id']: # 로그인한 이력이 있는 경우
            user_info = session['u_id']

            hots = hot_hot(hots, user_info)

            return render_template('hot.html', 
                                   hot = hots, week = week, user_info = user_info, 
                                   pagination=Pagination(page=page,  # 지금 우리가 보여줄 페이지는 1 또는 2, 3, 4, ... 페이지인데,
                                                        total=total,  # 총 몇 개의 포스트인지를 미리 알려주고,
                                                        per_page=per_page,  # 한 페이지당 몇 개의 포스트를 보여줄지 알려주고,
                                                        prev_label="<",  # 전 페이지와,
                                                        next_label=">",  # 후 페이지로 가는 링크의 버튼 모양을 알려주고,
                                                        format_total=True,  # 총 몇 개의 포스트 중 몇 개의 포스트를 보여주고있는지 시각화,
                                                        ),
                                   search=True,  # 페이지 검색 기능을 주고,
                                   bs_version=5,  # Bootstrap 사용시 이를 활용할 수 있게 버전을 알려줍니다.
                                   )
    except:
        return render_template('hot.html', 
                                hot = hots, week = week,
                                pagination=Pagination(page=page,  # 지금 우리가 보여줄 페이지는 1 또는 2, 3, 4, ... 페이지인데,
                                                    total=total,  # 총 몇 개의 포스트인지를 미리 알려주고,
                                                    per_page=per_page,  # 한 페이지당 몇 개의 포스트를 보여줄지 알려주고,
                                                    prev_label="<",  # 전 페이지와,
                                                    next_label=">",  # 후 페이지로 가는 링크의 버튼 모양을 알려주고,
                                                    format_total=True,  # 총 몇 개의 포스트 중 몇 개의 포스트를 보여주고있는지 시각화,
                                                    ),
                                search=True,  # 페이지 검색 기능을 주고,
                                bs_version=5,  # Bootstrap 사용시 이를 활용할 수 있게 버전을 알려줍니다.
                                )

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

# 11. 키워드 검색 페이지
# 키워드 검색 페이지
@views.route('/keyword1')
def search_page1():
    keyword1 = search_keyword1()
    keyword = uniq_keyword()[0]
    return render_template('keyword1.html', keyword1 = keyword1, keyword = keyword)
@views.route('/keyword2')
def search_page2():
    keyword2 = search_keyword2()
    keyword = uniq_keyword()[1]
    return render_template('keyword2.html', keyword2 = keyword2, keyword = keyword)
@views.route('/keyword3')
def search_page3():
    keyword3 = search_keyword3()
    keyword = uniq_keyword()[2]
    return render_template('keyword3.html', keyword3 = keyword3, keyword = keyword)
@views.route('/keyword4')
def search_page4():
    keyword4 = search_keyword4()
    keyword = uniq_keyword()[3]
    return render_template('keyword4.html', keyword4 = keyword4, keyword = keyword)
@views.route('/keyword5')
def search_page5():
    keyword5 = search_keyword5()
    keyword = uniq_keyword()[4]
    return render_template('keyword5.html', keyword5 = keyword5, keyword = keyword)
@views.route('/keyword6')
def search_page6():
    keyword6= search_keyword6()
    keyword = uniq_keyword()[5]
    return render_template('keyword6.html', keyword6 = keyword6, keyword = keyword)

# 핫플 소개 페이지
@views.route('/map', methods=['GET', 'POST'])
def map_page():
    if request.method == 'POST':
        dat = {'address':str(request.form['address']),
               'place':str(request.form['place'])}
    return render_template('map.html', dat=dat) 
