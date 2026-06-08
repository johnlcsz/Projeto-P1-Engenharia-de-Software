from app.services.user_service import ARQUIVOS_JOGOS
from flask import Blueprint, render_template
from app.services.csv_service import ler_csv    

usuario = Blueprint('usuario', __name__)

@usuario.route('/principal')
def pg_principal():
    valores = ler_csv(ARQUIVOS_JOGOS)
    return render_template('pg_principal.html', valores=valores)