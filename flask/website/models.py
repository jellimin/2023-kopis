# from . import db  # from website import db
# from flask_login import UserMixin
# from sqlalchemy.sql import func
# from datetime import datetime

# # 데이터베이스에 저장될 데이터에 대해 class를 선언
# # 즉, 유저와 메모장에 대한 데이터를 정의할 예정

# # define User Model
# # flask_login의 UserMixin 클래스를 상속
# # UserMixin : 사용자 개체가 가질 것으로 기대하는 메서드에 대한 기본 구현 제공
# # 첫번째 인자는 name (생략가능, DB에서 컬럼명)
# # 두번째 인자는 데이터 타입
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     nickname = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(200))
#     # 두 클래스 간의 관계를 제공하기 위해서 사용, 대소문자 동일하게 작성하기
#     notes = db.relationship('Note')
#     # 유저의 이미지 파일 경로
#     image_path = db.Column(db.String(255), unique=True, nullable=True)

# # define Openinfo Model
# class Openinfo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200))
#     url = db.Column(db.String(500))
#     image = db.Column(db.String(500))

# # define Preshow Model
# class Preshow(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     open_id = db.Column(db.Integer, db.ForeignKey('openinfo.id'))

# # define Note Model
# # onupdate는 해당 정보가 수정될 때마다 업데이트 되도록 하는 인수
# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(50))
#     content = db.Column(db.String(2000))
#     datetime = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
#     # 참조할 모델의 클래스와 속성을 모두 소문자로 표기
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))