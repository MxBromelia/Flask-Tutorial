from . import DB

class PalavraChave(DB.Model):
    __tablename__ = 'palavra_chave'
    id = DB.Column(DB.Integer, primary_key=True)
    palavra = DB.Column(DB.String(50), nullable=False)

    def __repr__(self):
        return '<Palavra-Chave %s>' % self.palavra

    def __str__(self):
        return self.palavra
