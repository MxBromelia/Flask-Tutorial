from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

# from flaskr.auth import login_required
from flaskr.schema import DB
# from flaskr.schema.post import Post
from flaskr.schema.user import User

bp = Blueprint('author', __name__, url_prefix='/author')

@bp.route('/', methods=('GET',))
def index():
    """Listagem de todos os usuários"""
    authors = DB.session.query(User).all()
    return render_template('author/index.html.jinja', authors=authors)

@bp.route('/<int:author_id>', methods=('GET',))
def read(author_id):
    """Mostra as informações de um usuário"""
    author = DB.session.query(User).get(author_id)

    if(author is None):
        abort(404, "This author does not exist")

    return render_template('author/read.html.jinja', author=author)
