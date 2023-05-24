import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import secret_key.config as config
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.String, primary_key=True)
    upw = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)
    birth = db.Column(db.String, nullable=True)
    profile = db.Column(db.String, nullable=True, default=config.IMAGE_URL+"default/default_profile.jpg")

    def serialize(self):
        return {
            'uid': self.uid,
            'email': self.email,
            'nickname': self.nickname,
            'gender': self.gender,
            'birth': self.birth,
            'profile': self.profile,
        }
    
class BookMark(db.Model):
    __tablename__ = "bookmarks"
    uid = db.Column(db.String,db.ForeignKey('users.uid'), primary_key=True)
    itemSeq = db.Column(db.String, primary_key=True)
    itemName = db.Column(db.String, nullable=False)
    itemImage = db.Column(db.String, nullable=True, default=config.IMAGE_URL+"default/medicine_default.jpg")
    updateDe = db.Column(db.String, nullable=True)

    def serialize(self):
        return {
            'uid': self.uid,
            'itemSeq': self.itemSeq,
            'itemName': self.itemName,
            'itemImage': self.itemImage,
            'updateDe': self.updateDe,
        }

