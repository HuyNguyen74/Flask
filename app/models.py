from app import db
from app import login
from flask_login import UserMixin
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.String(24))
    password=db.Column(db.String(128))

    def __repr__(self):
        return '<User> {},{},{}'.format(self.id,self.username,self.email)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post> {},{},{}'.format(self.id,self.body,self.user_id)
class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    bookname=db.Column(db.String(120))
    author=db.Column(db.String(120))
    img=db.Column(db.String(120))
    price=db.Column(db.Integer)
    def __repr__(self) :
        return '<Book> {},{},{},{},{}'.format(self.id,self.bookname,self.author,self.img,self.price)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))