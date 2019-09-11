"""Configurações de Banco de Dados"""
# Biblioteca de SQLITE
import sqlite3

import click
# Objeto especial que aponta para o objeto Flask que lida com a requisição.
# Como a aplicação é gerada a partir de uma fábrica, não há objeto de
# aplicação a ser referenciado dentro do código, porém 'get_db' será chamada
# quando a aplicação já existir e está lidando com uma requisição, então
# esta pode ser usada
# mais em: https://flask.palletsprojects.com/en/1.1.x/api/#flask.current_app
from flask import current_app
# Objeto especial único para cada requisição. É usado para armazenar dados que
# podem vir a ser usados por múltiplas funções durante uma consulta. A conexão
# é armazenada e reusada ao invés de criar uma nova conexão se 'get_db' é
# chamada uma segunda vez na mesma requisição
# mais em: https://flask.palletsprojects.com/en/1.1.x/api/#flask.g
from flask import g
from flask.cli import with_appcontext

def init_app(app):
    # Diz ao Flask para que chame aquela função quando limpando após retornar
    # a resposta. mais em:
    # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.teardown_appcontext
    app.teardown_appcontext(close_db)

    # Adiciona um novo comando que pode ser chamado junto de 'flask'. mais em:
    # https://click.palletsprojects.com/en/7.x/api/#click.Group.add_command
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()

    # open_resource -> Abre um arquivo relativo ao package 'flaskr', que é útil
    # pois você não necessariamente sabe onde ele estará quando "deployar" a
    # aplicação depois. Mais em:
    # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.open_resource
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# define um comando na CLI chamado 'init-db' que chamad 'init_db' e mostra
# mensagem de sucesso ao usuário.
# mais em: https://click.palletsprojects.com/en/7.x/api/#click.command
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def get_db():
    if 'db' not in g:
        # Estabelece uma conexão com o arquivo apontado pela chave de
        # de configuração DATABASE.
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Pede à conexão que retorne  linhas que se comportem feito Dicts.
        # Isto permite acesso a colunas pelo seu nome
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Checa se uma conexão foi criada checando se g.db foi definida.
    Se a conexão existir, ela é fechada"""
    db = g.pop('db', None)

    if db is not None:
        db.close()
