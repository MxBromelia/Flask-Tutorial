from . import DB
from .relacionamentos import autor_artigo

class Artigo(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    titulo = DB.Column(DB.Text, nullable=False)
    resumo = DB.Column(DB.Text, nullable=False)
    texto = DB.Column(DB.Text, nullable=False)
    usuario_id = DB.Column(
        DB.Integer, DB.ForeignKey('usuario.id'), nullable=False
    )
    evento_id = DB.Column(
        DB.Integer, DB.ForeignKey('evento.id'), nullable=False
    )

    usuario_publicador = DB.relationship('Usuario', lazy=True, uselist=False)
    autores = DB.relationship('Autor', secondary=autor_artigo, lazy=True)
    revisao = DB.relationship('Revisao', lazy=False, uselist=False)
    evento = DB.relationship('Evento', lazy=True, uselist=False)

    def __repr__(self):
        return '< Artigo %d >' % self.id

    def __str__(self):
        return self.titulo
