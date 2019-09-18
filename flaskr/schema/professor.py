from . import DB
from .usuario import Usuario

class Professor(Usuario):
    id = DB.Column(DB.Integer, DB.ForeignKey('usuario.id'), primary_key=True)
    titulacao = DB.Column(DB.String, nullable=False)
    area_concetracao_id = DB.Column(
        DB.Integer, DB.ForeignKey('area_concentracao.id'), nullable=False
    )
    admin = DB.Column(DB.Boolean, nullable=False, default=False)

    area = DB.relationship('AreaConcetracao')
    artigos = DB.relationship('Revisao', lazy=False)

    __mapper_args__ = {
        'polymorphic_identity': 'professor'
    }