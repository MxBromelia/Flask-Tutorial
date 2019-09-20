from . import DB

class Usuario(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    login = DB.Column(DB.String, nullable=False)
    senha = DB.Column(DB.String(255), nullable=False)
    instituicao = DB.Column(DB.String(255))
    autor_id = DB.Column(DB.Integer, DB.ForeignKey('autor.id'))
    tipo = DB.Column(DB.String(50))

    artigos_enviados = DB.relationship('Artigo', lazy=True)
    info = DB.relationship('Autor')

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': 'tipo'
    }

    def admin(self):
        if self.tipo == 'professor' and self.admin is True:
            return True
        else:
            return False

    def __repr__(self):
        return '< Usuario %s >' % self.login

    def __str__(self):
        return self.login
