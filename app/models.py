from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
) # auxiliary table, hence table not declared as model

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
    followed = db.relationship( 
        'User', secondary=followers,    
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),  lazy='dynamic')
        # "left" side entity is parent class, "right" side is this 'User'
        # 'secondary' configures assocation table
        # indicated condition linking "left" with assoc. table, .c. line refs column of assoc. table
        # indicated condition linking "right" with assoc. table
        # 'backref' defines how relationship accessed from "right"
        # 'lazy' as dynamic sets up query to not run until specifically requested

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
        # MD5 support in Python works on bytes and not on strings, hence string encoded as bytes before passing to hash function
    
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0 # go into the followers column and see, are they following this person??

    def followed_posts(self): # this is within User model, hence 'self' refers to user ID of user I'm interested in
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
        # join makes temporary table, but after query all excess columns are ignored (we only care about posts)

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