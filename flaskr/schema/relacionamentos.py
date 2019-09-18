from . import DB

autor_artigo = DB.Table(
    'autor_artigo',
    DB.Column('autor_id', DB.Integer, DB.ForeignKey('autor.id'), primary_key=True),
    DB.Column('artigo_id', DB.Integer, DB.ForeignKey('artigo.id'), primary_key=True)
)

palavra_chave_evento = DB.Table(
    'palavra_chave_evento',
    DB.Column('palavra_chave_id', DB.Integer, DB.ForeignKey('palavra_chave.id'), primary_key=True),
    DB.Column('evento_id', DB.Integer, DB.ForeignKey('evento.id'), primary_key=True)
)
