from datetime import datetime
from . import DB

class Post(DB.Model):
    """Post Class"""
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(200), nullable=False)
    body = DB.Column(DB.Text, nullable=False)
    created = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
    author_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    author = DB.relationship('User', backref=DB.backref('posts', lazy=True))
