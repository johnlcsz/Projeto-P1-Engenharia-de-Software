from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.services.user_service import *
from app.services.csv_service import gerar_id, ler_csv
from app.services.reviews_service import calcular_nota

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if session.get('usuario'):
        return redirect(url_for('usuario.pg_principal'))
    
    #Se o cadastro ou login der erro, o modal reaparece para ele tentar de novo 
    modal = request.args.get('modal')

    valores = ler_csv(ARQUIVOS_JOGOS)[:4]
    for jogo in valores:
        jogo['nota_usuarios'] = calcular_nota(jogo['id'])

    return render_template('index.html', modal=modal, valores=valores)

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
    
    novo_id = criar_usuario(nome, email, senha)
    session['usuario_id'] = novo_id
    session['usuario_nome'] = nome

    flash('Conta criada com sucesso!', 'geral')

    return redirect(url_for('usuario.pg_principal'))
    
@main.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    senha = request.form.get('senha')
    usuario = busca_usuario_email(email)

    if usuario and senha_correta(usuario, senha):
        session['usuario_id'] = usuario['id']
        session['usuario_nome'] = usuario['nome']
        flash('Você fez login com sucesso!', 'geral')

        return redirect(url_for('usuario.pg_principal'))
    
    flash('Email ou senha inválidos.', 'login')

    return redirect(url_for('main.index', modal='login'))

@main.route('/logout')
def logout():
    session.clear()
    flash('Você se desconectou da conta.', 'geral')
    return redirect(url_for('main.index'))