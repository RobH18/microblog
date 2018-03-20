from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic') # 'Post' is name of model class
    # posts is a high-level view of relationship between users and posts
    # one-to-many relationship, the db.relationship field is normally define on 'one' side
    # i.e. if user stored in u, u.posts will run query returning all posts written by that user
    # backref is field added to objects of 'many' class pointing back to 'one' object, adding post.author returning user given post
    # lazy defines how database query for relationship will be issued

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

# def __tablename__(self):
#     return 'tablename'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) # indexed - useful to retrieve posts in chronological order
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 'user' is name of database table for model

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
@login.user_loader
def load_user(id): # id passed as string, hence converted to int
    return User.query.get(int(id))