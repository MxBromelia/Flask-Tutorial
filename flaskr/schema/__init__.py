"""DB Package"""
from flask_sqlalchemy import SQLAlchemy
__all__ = (
    'aluno', 'area_concentracao', 'artigo', 'autor', 'evento', 'palavra_chave',
    'professor', 'relacionamentos', 'revisao', 'usuario'
)

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
