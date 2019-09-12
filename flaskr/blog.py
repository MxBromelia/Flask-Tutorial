from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# Como não há url_prefix definido, a view 'index' será adicionada em '/',
# 'create' em 'create', e assim sucessivamente.
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    """Página inicial, onde há uma listagem de todas as postagens"""
    database = get_db()
    posts = database.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
# Chama função login_required que encapsula view e checa a autenticação do
# usuário
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
            database = get_db()
            database.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            database.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@bp.route('/<int:user_id>/update', methods=('GET', 'POST'))
@login_required
def update(user_id):
    """Atualizar um post"""
    post = get_post(user_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            database = get_db()
            database.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, user_id)
            )
            database.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:user_id>/delete', methods=('POST',))
@login_required
def delete(user_id):
    """Remover uma postagem"""
    get_post(user_id)
    database = get_db()
    database.execute('DELETE FROM post WHERE id = ?', (user_id,))
    database.commit()
    return redirect(url_for('blog.index'))

# Uma vez que ambos 'update' e 'delete' precisarão procurar pela postagem
# Definir numa função separada para evitar repetição de código
# check_author: Checa se usuário é o autor do post.
#   Verdadeiro para update/delete
#   False para show
def get_post(user_id, check_author=True):
    """Busca pelo post pelo seu id."""
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (user_id,)
    ).fetchone()

    # Caso não exista um post com este ID, Erro 404
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(user_id))

    # Caso o usuário não é o mesmo que publicou originalmente o post, Erro 403
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    # abort -> levanta uma exceção especial que retorna um código de status HTTP.
    # É necessário um argumento opcional para vir com o erro, senão vem uma mensagem
    # padrão
    # mais em: https://flask.palletsprojects.com/en/1.1.x/api/#flask.abort

    return post
