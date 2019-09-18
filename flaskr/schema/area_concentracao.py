from . import DB

class AreaConcentracao(DB.Model):
    __tablename__ = 'area_concentracao'
    id = DB.Column(DB.Integer, primary_key=True)
    area = DB.Column(DB.String(50), nullable=False)

    def __repr__(self):
        return '<Área de Concentração %s>' % self.area

    def __str__(self):
        return self.area
