from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.String, primary_key=True)
    upw = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=True)
    birth = db.Column(db.String, nullable=True)
    profile = db.Column(db.String, nullable=True)

    def serialize(self):
        return {
            'uid': self.uid,
            'upw': self.upw,
            'email': self.email,
            'nickname': self.nickname,
            'gender': self.gender,
            'birth': self.birth,
            'profile': self.profile,
        }