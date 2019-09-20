from . import DB
from .relacionamentos import palavra_chave_evento

class Evento(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    nome = DB.Column(DB.Text, nullable=False)
    sigla = DB.Column(DB.String(10))
    evento_inicio = DB.Column(DB.Date, nullable=False)
    evento_fim = DB.Column(DB.Date, nullable=False)
    submissao_inicio = DB.Column(DB.Date, nullable=False)
    submissao_fim = DB.Column(DB.Date, nullable=False)
    area_concentracao_id = DB.Column(
        DB.Integer, DB.ForeignKey('area_concentracao.id'), nullable=False
    )

    area = DB.relationship('AreaConcentracao', lazy=False, uselist=False)
    palavras_chave = DB.relationship(
        'PalavraChave', secondary=palavra_chave_evento, lazy=False
    )
    artigos = DB.relationship('Artigo', lazy=True)
