from flask import Flask

from flask_migrate import Migrate
from controllers.usercontroller import user
from controllers.medicinecontroller import medicine
from controllers.chatcontroller import chat
import secret_key.config as config
from models import db

app = Flask(__name__)


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
import models