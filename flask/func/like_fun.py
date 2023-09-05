### 좋아요 기능 관련 함수

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

### 좋아요 정보 가져오기
# 메인페이지 각 오픈공연별 좋아요 정보 가져오는 함수
def main_open(main_open_id, opens, user_info):
    from website import mysql

    # 좋아요 DB 정보 가져오기
    sql = "SELECT * FROM OpenLiked WHERE show_id IN ('%s', '%s', '%s', '%s', '%s', '%s')" %(main_open_id[0],main_open_id[1],main_open_id[2],
                                                                                main_open_id[3],main_open_id[4],main_open_id[5])
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    all_likes_tmp = cursor.fetchall()
    cursor.close()
    conn.close()
    like_count = {}
    like_by_me = {}

    all_likes = []
    for i in range(len(all_likes_tmp)):
        u_id = all_likes_tmp[i][1]
        show_id = all_likes_tmp[i][2]
        like_info = {
            'u_id' : u_id,
            'show_id' : show_id
        }
        all_likes.append(like_info)

    # 좋아요 DB에서 좋아요 수 count하기
    for like in all_likes:
        like_user_id = like["u_id"]
        if user_info == like_user_id:
            like_by_me[like["show_id"]] = True
        try:
            like_count[like["show_id"]] += 1
        except:
            like_count[like["show_id"]] = 1

    for open in opens:
        # 현재 해당글의 좋아요 수가 몇개인지 적어라
        open["count_heart"] = like_count[open["_id"]] if open["_id"] in like_count else 0
        # 내가 좋아요를 누른지의 유무
        open["heart_by_me"] = True if open["_id"] in like_by_me else False

    return opens

# 메인페이지 각 핫공연별 좋아요 정보 가져오는 함수
def main_hot(main_hot_id, hots, user_info):
    from website import mysql

    # 좋아요 DB 정보 가져오기
    sql = "SELECT * FROM NewLiked WHERE show_id IN ('%s', '%s', '%s', '%s', '%s', '%s')" %(main_hot_id[0],main_hot_id[1],main_hot_id[2],
                                                                                           main_hot_id[3],main_hot_id[4],main_hot_id[5])
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    all_likes_tmp = cursor.fetchall()
    cursor.close()
    conn.close()
    like_count = {}
    like_by_me = {}

    all_likes = []
    for i in range(len(all_likes_tmp)):
        u_id = all_likes_tmp[i][1]
        show_id = all_likes_tmp[i][2]
        like_info = {
            'u_id' : u_id,
            'show_id' : show_id
        }
        all_likes.append(like_info)

    # 좋아요 DB에서 좋아요 수 count하기
    for like in all_likes:
        like_user_id = like["u_id"]
        if user_info == like_user_id:
            like_by_me[like["show_id"]] = True
        try:
            like_count[like["show_id"]] += 1
        except:
            like_count[like["show_id"]] = 1

    for hot in hots:
        # 현재 해당글의 좋아요 수가 몇개인지 적어라
        hot["count_heart"] = like_count[hot["_id"]] if hot["_id"] in like_count else 0
        # 내가 좋아요를 누른지의 유무
        hot["heart_by_me"] = True if hot["_id"] in like_by_me else False

    return hots

# 메인페이지 각 핫공연별 좋아요 정보 가져오는 함수
def main_key(main_key_id, keys, user_info):
    from website import mysql

    # 좋아요 DB 정보 가져오기
    sql = "SELECT * FROM NewLiked WHERE show_id IN ('%s', '%s', '%s', '%s', '%s', '%s')" %(main_key_id[0],main_key_id[1],main_key_id[2],
                                                                                               main_key_id[3],main_key_id[4],main_key_id[5])
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    all_likes_tmp = cursor.fetchall()
    cursor.close()
    conn.close()
    like_count = {}
    like_by_me = {}

    all_likes = []
    for i in range(len(all_likes_tmp)):
        u_id = all_likes_tmp[i][1]
        show_id = all_likes_tmp[i][2]
        like_info = {
            'u_id' : u_id,
            'show_id' : show_id
        }
        all_likes.append(like_info)

    # 좋아요 DB에서 좋아요 수 count하기
    for like in all_likes:
        like_user_id = like["u_id"]
        if user_info == like_user_id:
            like_by_me[like["show_id"]] = True
        try:
            like_count[like["show_id"]] += 1
        except:
            like_count[like["show_id"]] = 1

    for key in keys:
        # 현재 해당글의 좋아요 수가 몇개인지 적어라
        key["count_heart"] = like_count[key["_id"]] if key["_id"] in like_count else 0
        # 내가 좋아요를 누른지의 유무
        key["heart_by_me"] = True if key["_id"] in like_by_me else False

    return keys

# 더보기 오픈페이지 각 오픈공연별 좋아요 정보 가져오는 함수
def open_open(opens, user_info):
    from website import mysql

    # 좋아요 DB 정보 가져오기
    sql = "SELECT * FROM OpenLiked"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    all_likes_tmp = cursor.fetchall()
    cursor.close()
    conn.close()
    like_count = {}
    like_by_me = {}

    all_likes = []
    for i in range(len(all_likes_tmp)):
        u_id = all_likes_tmp[i][1]
        show_id = all_likes_tmp[i][2]
        like_info = {
            'u_id' : u_id,
            'show_id' : show_id
        }
        all_likes.append(like_info)

    # 좋아요 DB에서 좋아요 수 count하기
    for like in all_likes:
        like_user_id = like["u_id"]
        if user_info == like_user_id:
            like_by_me[like["show_id"]] = True
        try:
            like_count[like["show_id"]] += 1
        except:
            like_count[like["show_id"]] = 1

    for open in opens:
        # 현재 해당글의 좋아요 수가 몇개인지 적어라
        open["count_heart"] = like_count[open["_id"]] if open["_id"] in like_count else 0
        # 내가 좋아요를 누른지의 유무
        open["heart_by_me"] = True if open["_id"] in like_by_me else False

    return opens

# 더보기 핫페이지 각 오픈공연별 좋아요 정보 가져오는 함수
def hot_hot(hots, user_info):
    from website import mysql

    # 좋아요 DB 정보 가져오기
    sql = "SELECT * FROM NewLiked"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    all_likes_tmp = cursor.fetchall()
    cursor.close()
    conn.close()
    like_count = {}
    like_by_me = {}

    all_likes = []
    for i in range(len(all_likes_tmp)):
        u_id = all_likes_tmp[i][1]
        show_id = all_likes_tmp[i][2]
        like_info = {
            'u_id' : u_id,
            'show_id' : show_id
        }
        all_likes.append(like_info)

    # 좋아요 DB에서 좋아요 수 count하기
    for like in all_likes:
        like_user_id = like["u_id"]
        if user_info == like_user_id:
            like_by_me[like["show_id"]] = True
        try:
            like_count[like["show_id"]] += 1
        except:
            like_count[like["show_id"]] = 1

    for hot in hots:
        # 현재 해당글의 좋아요 수가 몇개인지 적어라
        hot["count_heart"] = like_count[hot["_id"]] if hot["_id"] in like_count else 0
        # 내가 좋아요를 누른지의 유무
        hot["heart_by_me"] = True if hot["_id"] in like_by_me else False

    return hots

# 더보기 키워드 각 오픈공연별 좋아요 정보 가져오는 함수
def key_key(keys, user_info):
    from website import mysql

    # 좋아요 DB 정보 가져오기
    sql = "SELECT * FROM NewLiked"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    all_likes_tmp = cursor.fetchall()
    cursor.close()
    conn.close()
    like_count = {}
    like_by_me = {}

    all_likes = []
    for i in range(len(all_likes_tmp)):
        u_id = all_likes_tmp[i][1]
        show_id = all_likes_tmp[i][2]
        like_info = {
            'u_id' : u_id,
            'show_id' : show_id
        }
        all_likes.append(like_info)

    # 좋아요 DB에서 좋아요 수 count하기
    for like in all_likes:
        like_user_id = like["u_id"]
        if user_info == like_user_id:
            like_by_me[like["show_id"]] = True
        try:
            like_count[like["show_id"]] += 1
        except:
            like_count[like["show_id"]] = 1

    for key in keys:
        # 현재 해당글의 좋아요 수가 몇개인지 적어라
        key["count_heart"] = like_count[key["_id"]] if key["_id"] in like_count else 0
        # 내가 좋아요를 누른지의 유무
        key["heart_by_me"] = True if key["_id"] in like_by_me else False

    return keys

# 오픈 정보 좋아요 버튼 눌렀을 때 DB 업데이트 함수
def update_like_in():
    # 현재 로그인한 유저 id
    user_info = session['u_id']
    # 게시글의 id
    show_id_receive = request.form["show_id_give"]
    # 행위
    action_receive = request.form["action_give"]
    # 좋아요가 눌려져 있는 상태라면
    if action_receive == "like":
        sql = "INSERT INTO OpenLiked (u_id, show_id) VALUES ('%s', '%s')" % (user_info, show_id_receive)
        from website import mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    # 좋아요가 눌러져 있지 않은 상태라면
    else:
        sql = "DELETE FROM OpenLiked WHERE u_id = '%s' AND show_id = '%s'" % (user_info, show_id_receive)
        from website import mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    sql = "SELECT COUNT(IF(show_id = '%s', show_id, NULL)) FROM OpenLiked" % (show_id_receive)
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    count = data[0][0]

    return count

# 핫 정보 좋아요 버튼 눌렀을 때 DB 업데이트 함수
def update_like_in_hot():
    # 현재 로그인한 유저 id
    user_info = session['u_id']
    # 게시글의 id
    show_id_receive = request.form["show_id_give"]
    # 행위
    action_receive = request.form["action_give"]
    # 좋아요가 눌려져 있는 상태라면
    if action_receive == "like":
        sql = "INSERT INTO NewLiked (u_id, show_id) VALUES ('%s', '%s')" % (user_info, show_id_receive)
        from website import mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    # 좋아요가 눌러져 있지 않은 상태라면
    else:
        sql = "DELETE FROM NewLiked WHERE u_id = '%s' AND show_id = '%s'" % (user_info, show_id_receive)
        from website import mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    sql = "SELECT COUNT(IF(show_id = '%s', show_id, NULL)) FROM NewLiked" % (show_id_receive)
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    count = data[0][0]

    return count

# 키워드 정보 좋아요 버튼 눌렀을 때 DB 업데이트 함수
def update_like_in_key():
    # 현재 로그인한 유저 id
    user_info = session['u_id']
    # 게시글의 id
    show_id_receive = request.form["show_id_give"]
    # 행위
    action_receive = request.form["action_give"]
    # 좋아요가 눌려져 있는 상태라면
    if action_receive == "like":
        sql = "INSERT INTO NewLiked (u_id, show_id) VALUES ('%s', '%s')" % (user_info, show_id_receive)
        from website import mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    # 좋아요가 눌러져 있지 않은 상태라면
    else:
        sql = "DELETE FROM NewLiked WHERE u_id = '%s' AND show_id = '%s'" % (user_info, show_id_receive)
        from website import mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    sql = "SELECT COUNT(IF(show_id = '%s', show_id, NULL)) FROM NewLiked" % (show_id_receive)
    from website import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    count = data[0][0]

    return count