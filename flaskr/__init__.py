"""Factory da Aplicação"""
import os
from flask import Flask

def create_app(test_config=None):
    """Criar e Configurar App"""
    # instance_relative_config=True -> arquivos de configuracao são
    # referenciados relativamente ao diretório de instâncias
    # diretório de instâncias(instance folders) ->
    #   https://flask.palletsprojects.com/en/1.1.x/config/#instance-folders
    app = Flask(__name__, instance_relative_config=True)
    # Define configurações padrões usada pelo App
    app.config.from_mapping(
        # Usado para manter dados seguros, em produção deve conter uma string
        # aleatória
        # mais: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
        SECRET_KEY='dev',
        # Caminho em que o DB SQLite será salvo
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # app.config.from_pyfile() -> Sobrescreve as configurações padrões com
    # valores de config.py presente no diretório de instância, caso esteja
    # presente.
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Garantir que o diretório de instância existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app