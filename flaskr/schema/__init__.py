"""DB Package"""
from flask_sqlalchemy import SQLAlchemy
# from . import *

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
