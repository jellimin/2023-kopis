from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash # 비밀번호 해싱
from flask_login import login_user, login_required, logout_user, current_user
import re
from flask import Flask, request
from flaskext.mysql import MySQL
import json
from datetime import datetime
import importlib

auth = Blueprint('auth', __name__)

SECRET_KEY = 'secret_key'

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    # login
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')

        # search User in database & compare password
        from . import mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select u_id from KEYWIDB.UserInfo where user_id='{}' AND user_password ='{}'".format(email, password1))
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if data:
            flash('로그인 완료', category='success')
            session['u_id'] = data[0][0]
            return redirect(url_for('views.home'))
        else:
            flash('해당 이메일 정보가 없습니다.', category='error')

    return render_template('sign_in.html')

@auth.route('/logout')
def logout():
    session.pop('u_id',None)
    session.pop('image_url',None)
    return redirect(url_for('auth.sign_in')) # 로그인할 수 있는 화면으로 돌아감

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # form - input의 name 속성을 기준으로 가져오기
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        nickname = request.form.get('nickname')
        birth = request.form.get('birth')
        gender = request.form.get('gender')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        address3 = request.form.get('address3')

        # 유효성 검사
        from . import mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from KEYWIDB.UserInfo where user_id='{}'".format(email))
        data = cursor.fetchall()
        if data:
            flash("이미 가입된 이메일입니다.", category='error')
        elif re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) == None:
            flash("이메일 입력 형식이 잘못 되었습니다.", category="error")
        elif len(name) < 2:
            flash("이름은 2자 이상입니다.", category="error")
        elif re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password1) == None:
            flash("비밀번호 입력 형식이 잘못 되었습니다.", category="error")
        elif password1 != password2 :
            flash("비밀번호와 비밀번호 재입력이 서로 다릅니다.", category="error")
        elif len(nickname) < 2:
            flash("닉네임은 2자 이상입니다.", category="error")
        else:
            # Create User > DB
            cursor.execute("insert into KEYWIDB.UserInfo (user_id, user_password, name, nickname, birthday, gender, address1, address2, address3) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (email, password1, name, nickname, birth, gender, address1, address2, address3))
            conn.commit()
            flash("회원가입 완료.", category="success")  # Create User -> DB
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')