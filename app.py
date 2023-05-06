from flask import Flask

from flask_migrate import Migrate
from controllers.usercontroller import user
from controllers.medicinecontroller import medicine
from controllers.chatcontroller import chat
from controllers.barcodecontroller import barcode
import secret_key.config as config
from models import db

app = Flask(__name__)

#  DB 설정
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='postgresql://{user}:{pw}@{url}:{port}/{db}'.format(
    user=config.DB_USER,
    pw=config.DB_PASS,
    url=config.DB_HOST,
    port=config.DB_PORT,
    db=config.DB_NAME),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLAlchemy_ECHO=True
)

db.init_app(app)
Migrate(app,db)

@app.route("/") # localhost:5000/ 을 잡는 라우터
def hello():
    return "Hello World!"

app.register_blueprint(user, url_prefix="/user")    # localhost:5000/ 뒤에 user 가 붙으면 전부 userController로 보냄
app.register_blueprint(medicine, url_prefix="/medicine") 
app.register_blueprint(chat, url_prefix="/chat") 
app.register_blueprint(barcode, url_prefix="/barcode") 

# if __name__ == "__main__":
# 	app.run(host='0.0.0.0', port=8080)


# model import 밑에 안하면 터져서 여기다가 import함
import models