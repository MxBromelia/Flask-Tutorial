from . import DB

# Association Object Pattern
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
class Revisao(DB.Model):
    artigo_id = DB.Column(DB.Integer, DB.ForeignKey('artigo.id'), primary_key=True)
    professor_id = DB.Column(DB.Integer, DB.ForeignKey('professor.id'), primary_key=True)
    # Valores: AGR, EMR, APR, REP
    situacao = DB.Column(DB.String(3), nullable=False, default='AGR')

    artigo = DB.relationship('Artigo', lazy=True)
    revisor = DB.relationship('Professor', lazy=True)
