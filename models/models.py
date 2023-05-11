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
    
class BookMark(db.Model):
    __tablename__ = "bookmarks"
    uid = db.Column(db.String,db.ForeignKey('users.uid'), primary_key=True)
    itemSeq = db.Column(db.String, primary_key=True)
    itemName = db.Column(db.String, nullable=False)
    itemImage = db.Column(db.String, nullable=False)
    updateDe = db.Column(db.String, nullable=False)

