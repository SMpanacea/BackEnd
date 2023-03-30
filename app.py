from flask import Flask
from controllers.usercontroller import user
from controllers.medicinecontroller import medicine

app = Flask(__name__)

@app.route("/") # localhost:5000/ 을 잡는 라우터
def hello():
    return "Hello World!"

app.register_blueprint(user, url_prefix="/user")    # localhost:5000/ 뒤에 user 가 붙으면 전부 userController로 보냄
app.register_blueprint(medicine, url_prefix="/medicine") 

