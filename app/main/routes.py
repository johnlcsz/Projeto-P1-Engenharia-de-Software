from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.services.csv_service import gerar_id
from app.services.user_service import validar_senha, validar_nome, email_existe, criar_usuario, nome_existe

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if session.get('usuario'):
        return redirect(url_for('usuario.pg_principal'))
    modal = request.args.get('modal')
    return render_template('index.html', modal=modal)

@main.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    erros = []
    if not validar_nome(nome):
        erros.append('O nome precisa ter entre 3 e 20 caracteres.')
    if nome_existe(nome):
        erros.append('Esse nome já está sendo usado.')
    if email_existe(email):
        erros.append('Esse e-mail já está sendo usado.')
    if not validar_senha(senha):
        erros.append('A senha precisa ter entre 6 e 20 caracteres e conter pelo menos uma letra e um número.')
    if erros:
        for erro in erros:
            flash(erro, 'cadastro')
        return redirect(url_for('main.index', modal='register'))
    else:
        novo_id = criar_usuario(nome, email, senha)
        session['usuario'] = novo_id
        flash('Conta criada com sucesso!', 'geral')
        return redirect(url_for('usuario.pg_principal'))
    
@main.route('/login', methods=['POST'])
def login():
    return redirect(url_for('main.index'))
