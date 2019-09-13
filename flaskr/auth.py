"""Autenticação de Usuário"""
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.schema import DB
from flaskr.schema.user import User

# Blueprint -> um modo de organizar um grupo de views relacionadas e outros
# códigos. Em vez de registrar views o outros códigos diretamente com uma
# aplicação, elas são registradas com uma Blueprint. Esta, então, é registrada
# na aplicação, quando está disponível na função de Factory.
#   url_prefix -> define o caminho que será posto ao início da url.
# mais em: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

# before_app_request -> decorator que registra uma função que é executada antes
# da view, não importa que URL é requisitada.
# mais em:
# https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint.before_app_request
@bp.before_app_request
def load_logged_in_user():
    """Verifica se um id de usuário está armazenado em session e coleta o dado
    deste do banco de dados, armazenando em g.user, que dura por toda a
    requisição. Se não há id de usuário, g.user será None"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = DB.session.query(User).get(user_id)

# route: /auth/register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Cadastro de um novo usuário"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # Validar se username não está vazio
        if not username:
            error = 'Username is required.'
        # Validar se password não está vazio
        elif not password:
            error = 'Password is required.'
        # Validar se login é inédito
        elif DB.session.query(User).filter_by(username=username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        # Insere novo usuário no banco de dados
        # Senhas nunca devem ser armazenadas diretamente pelo banco
        # generate_password_hash -> retorna hash da senha. mais em:
        # https://werkzeug.palletsprojects.com/en/0.15.x/utils/#werkzeug.security.generate_password_hash
        if error is None:
            psd_hash = generate_password_hash(password)
            new_user = User(username=username, password=psd_hash)
            DB.session.add(new_user)

            # Salva as alterações no banco feitas pela função
            # database.commit()
            DB.session.commit()
            # url_for -> gera a url relacionada à rota definida
            # mais em: https://flask.palletsprojects.com/en/1.1.x/api/#flask.url_for
            return redirect(url_for('auth.login'))

        # Se aconteceu algum erro na validação do cadastro, este é mostrado ao
        # usuário.
        # flash -> armazena mensagem que pode ser retornada quando renderizando
        # o template.
        # mais em: https://flask.palletsprojects.com/en/1.1.x/api/#flask.flash
        flash(error)

    # Em Caso de ser uma requisição get ou erro de validação, a página HTML com
    # o formulário de registro deve ser mostrado.
    # render_template -> renderiza o template.
    # mais em: https://flask.palletsprojects.com/en/1.1.x/api/#flask.render_template
    return render_template('auth/register.html')

# route: /auth/login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Autenticação de um usuário existente"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        # procura no banco de dados o username informado
        user = DB.session.query(User).filter_by(username=username).first()

        # Valida se há um usuário com este username
        # if user is None:
        if user is None:
            error = 'Incorrect username.'
        # Valida se a senha informada é a senha de usuário
        # check_password_hash -> compara os hashes de senhas informados.
        # mais em:
        # https://werkzeug.palletsprojects.com/en/0.15.x/utils/#werkzeug.security.check_password_hash

        elif not check_password_hash(user.password, password):
            # elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session -> um tipo especial de dict que se mantém através das
            # requests. mais em:
            # https://flask.palletsprojects.com/en/1.1.x/api/#flask.session
            session.clear()
            # armazena user_id como um cookie
            # session['user_id'] = user['id']
            session['user_id'] = user.id
            return redirect(url_for('index'))

        # Se acontecer algo de errado na autenticação do usuário, informar ao
        # usuário
        flash(error)

    # Se é uma requisição GET ou houve um erro de autenticação, o formulário de
    # autenticação deve ser mostrado
    return render_template('auth/login.html')

# ath: /auth/logout
@bp.route('/logout')
def logout():
    """Encerra a sessão do usuário atual"""
    # Para 'deslogar', deve-se remover o id de usuário de session. Assim,
    # load_logged_in_user não carregará um usuário nas requisições seguintes
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    # Este decorator retorna uma nove função de view que encapsula a view
    # original que é recebida. A nova função verifica se um usuário está
    # autenticado, redirecionando para a página de login caso contrário.
    # Se um usuário está carregado a view é chamada e continua normalmente.
    # Será usado quando escrever as view do blog
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
