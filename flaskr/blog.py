from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.schema import DB, Post, User

# Como não há url_prefix definido, a view 'index' será adicionada em '/',
# 'create' em 'create', e assim sucessivamente.
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    """Página inicial, onde há uma listagem de todas as postagens"""
    posts = DB.session.query(Post).order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)

# @login_reuired -> Chama função login_required que encapsula view e checa a
# autenticação do usuário
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Criar novo post"""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            author = DB.session.query(User).get(g.user.id)
            new_post = Post(title=title, body=body, author=author)
            DB.session.add(new_post)
            DB.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@bp.route('/<int:post_id>', methods=('GET',))
def read(post_id):
    """Visualizar um post"""
    post = get_post(post_id, check_author=False)

    return render_template('blog/read.html', post=post)

@bp.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    """Atualizar um post"""
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            DB.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    """Remover uma postagem"""
    post = get_post(post_id)
    DB.session.delete(post)
    DB.session.commit()
    return redirect(url_for('blog.index'))

# Uma vez que ambos 'update' e 'delete' precisarão procurar pela postagem
# Definir numa função separada para evitar repetição de código
# check_author: Checa se usuário é o autor do post.
#   Verdadeiro para update/delete
#   False para show
def get_post(post_id, check_author=True):
    """Busca pelo post pelo seu id."""
    post = DB.session.query(Post).get(post_id)

    # Caso não exista um post com este ID, Erro 404
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(post_id))

    # Caso o usuário não é o mesmo que publicou originalmente o post, Erro 403
    if check_author and post.author != g.user:
        abort(403)
    # abort -> levanta uma exceção especial que retorna um código de status HTTP.
    # É necessário um argumento opcional para vir com o erro, senão vem uma mensagem
    # padrão
    # mais em: https://flask.palletsprojects.com/en/1.1.x/api/#flask.abort

    return post
