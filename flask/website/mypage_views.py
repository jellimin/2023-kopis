from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify, session
from flask_login import login_required, current_user
# from .models import Note, User
# from . import db
import os
from werkzeug.utils import secure_filename
import re
from func.mypage_open import open_like, open_like_all

mypage_views = Blueprint('mypage_views', __name__)

# 나의 정보 페이지
@mypage_views.route('/mypage', methods=['GET','POST'])
def mypage():
    user_info = session['u_id']
    op_like = open_like(user_info)

    return render_template('mypage.html', op_like = op_like)

# 프로필 이미지 확장자 목록
ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif']

# 확장자 확인
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 나의 정보 수정 페이지
@mypage_views.route('/mypage/update', methods=['GET','POST'])
def mypage_update():

    # 나의 정보 수정 요청 확인
    if request.method == 'POST':
        changed = False # 변경 여부가 있는 지 확인

        # 이미지 파일 정보가 있는 지 확인
        if 'imageFile' in request.files:
            image_file = request.files['imageFile']  # 디버그 모드로 확인

            # 파일이 존재하는지 확인
            if image_file.filename:
                # 허용된 파일인지 확인
                if allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    filetype = filename.rsplit('.', 1)[1].lower()
                    image_path = f'{os.path.dirname(__file__)}/static/'  # ../website/static/


                    # user id로 프로필 명 저장
                    image_file.save('{}{}.{}'.format(image_path, session['u_id'], filetype))

                    # DB user.image_path에 반영
                    id = session['u_id']
                    sql = "UPDATE UserInfo SET image_url = '%s' WHERE u_id = '%s'" % (str(id)+'.'+filetype, id)

                    from . import mysql
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    session['image_url'] = '{}.{}'.format(session['u_id'], filetype)

                    return redirect(url_for('mypage_views.mypage'))
                else:
                    # 확장자가 허용되지 않음
                    flash('이미지 파일은 png jpg jepg gif 만 지원합니다.', category = "error")
                    return redirect(request.url)
                
        # 변경여부 확인
        password1 = request.form.get('password1')
        nickname = request.form.get('nickname')
        birth = request.form.get('birth')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        address3 = request.form.get('address3')

        # 패스워드 입력 여부 및 유효성 검사
        if password1:
            if re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password1) == None:
                flash("비밀번호 입력 형식이 잘못 되었습니다.", category="error")
                return redirect(request.url)
            else:
                id = session['u_id']
                sql = "UPDATE UserInfo SET user_password = '%s' WHERE u_id = '%s'" % (password1, id)
                from . import mysql
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                changed = True

        # 닉네임 입력 여부
        if nickname:
            if len(nickname) < 2:
                flash("닉네임은 2자 이상입니다.", category="error")
                return redirect(request.url)
            else:
                id = session['u_id']
                sql = "UPDATE UserInfo SET nickname = '%s' WHERE u_id = '%s'" % (nickname, id)
                from . import mysql
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                changed = True

        # 생년월일 입력 여부
        if birth:
            id = session['u_id']
            sql = "UPDATE UserInfo SET birthday = '%s' WHERE u_id = '%s'" % (birth, id)
            from . import mysql
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            changed = True

        # 주소1, 주소2, 주소3 모두 입력된 경우
        if address1 and address2 and address3:
            id = session['u_id']
            sql = "UPDATE UserInfo SET address1 = '%s', address2 = '%s', address3 = '%s' WHERE u_id = '%s'" % (address1, address2, address3, id)
            from . import mysql
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            changed = True

        # 주소1, 주소2 모두 입력된 경우 -> 세종특별자치시 경우, 주소3 없음
        if address1 and address2:
            id = session['u_id']
            sql = "UPDATE UserInfo SET address1 = '%s', address2 = '%s', address3 = NULL WHERE u_id = '%s'" % (address1, address2, id)
            from . import mysql
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            changed = True

        # 변경사항이 있다면 redirect
        if changed:
            flash('정보가 변경 되었습니다', category = "success")
            return redirect(url_for('mypage_views.mypage'))
        else :
            flash('변경 사항이 없습니다.', category = "error")
            return redirect(request.url)

    return render_template('mypage_update.html')

# 좋아하는 공연 더보기
@mypage_views.route('/mypage/pre_shows')
def pre_shows():
    user_info = session['u_id']
    op_like = open_like_all(user_info)

    return render_template('pre_shows.html', op_like = op_like)

# 좋아하는 공연 삭제하기
@mypage_views.route('/mypage/pre_shows/delete/<int:show_id>')
def delete(show_id):
    user_info = session['u_id']
    sql = "DELETE FROM OpenLiked WHERE u_id = '%s' AND show_id = '%s'" % (user_info, show_id)
    from . import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('mypage_views.pre_shows'))