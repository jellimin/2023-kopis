### 좋아요 기능 관련 함수

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def main_open(main_open_id, opens, user_info):
    from website import mysql

    # 좋아요 DB 정보 가져오기
    sql = "SELECT * FROM OpenLiked WHERE show_id IN ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(main_open_id[0],main_open_id[1],main_open_id[2],main_open_id[3],
                                                                                                        main_open_id[4],main_open_id[5],main_open_id[6],main_open_id[7])
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