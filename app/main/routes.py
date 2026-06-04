from flask import Blueprint, render_template, redirect, url_for, session

main = Blueprint('main', __name__)

@main.route('/')
def index():

    if session.get('usuario'):
        return redirect(url_for('usuario.pg_principal'))

    return render_template('index.html')