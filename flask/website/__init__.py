from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask      import Flask, request, jsonify, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text
from flaskext.mysql import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    app.config['MYSQL_DATABASE_USER'] = 'hashtag'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'hashtag123'
    app.config['MYSQL_DATABASE_DB'] = 'KEYWIDB'
    app.config['MYSQL_DATABASE_HOST'] = 'admin.ckaurvkcjohj.eu-north-1.rds.amazonaws.com'
    app.secret_key = "ABCDEFG"
    mysql.init_app(app)

    # 블루프린트 인스턴스 가져오기
    from .views import views
    from .auth import auth
    from .mypage_views import mypage_views

    # 플라스크 앱에 등록하기
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(mypage_views, url_prefix='/')

    return app