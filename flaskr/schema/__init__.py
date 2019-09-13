"""DB Package"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

def init_app(app):
    DB.init_app(app)
    init_db(app)

def init_db(app):
    """Create Schema"""
    with app.app_context():
        DB.create_all()

def destroy_db(app):
    """Drop Schema"""
    with app.app_context():
        DB.drop_all()

# class Post(DB.Model):
#     """Post Class"""
#     id = DB.Column(DB.Integer, primary_key=True)
#     title = DB.Column(DB.String(200), nullable=False)
#     body = DB.Column(DB.Text, nullable=False)
#     created = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
#     author_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
#     author = DB.relationship('User', backref=DB.backref('posts', lazy=True))
# class User(DB.Model):
#     id = DB.Column(DB.Integer, primary_key=True)
#     username = DB.Column(DB.String(50), unique=True, nullable=False)
#     password = DB.Column(DB.String(100), nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username
