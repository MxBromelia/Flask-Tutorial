from . import DB


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(50), unique=True, nullable=False)
    password = DB.Column(DB.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
