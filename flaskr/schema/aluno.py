from . import DB
from .usuario import Usuario

class Aluno(Usuario):
    id = DB.Column(DB.Integer, DB.ForeignKey('usuario.id'), primary_key=True)
    matricula = DB.Column(DB.String(30))

    __mapper_args__ = {
        'polymorphic_identity': 'aluno'
    }
