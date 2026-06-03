from flask import Blueprint, render_template

usuario = Blueprint('usuario', __name__)

@usuario.route('/principal')
def pg_principal():
    return render_template('pg_principal.html')