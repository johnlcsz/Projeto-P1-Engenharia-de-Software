from flask import Blueprint, render_template, session, redirect, url_for
from app.services.csv_service import ler_csv
from app.services.user_service import ARQUIVOS_JOGOS, ARQUIVO_REVIEWS

usuario = Blueprint('usuario', __name__)

def _get_stats(usuario_id):
    try:
        reviews = ler_csv(ARQUIVO_REVIEWS)
        reviews_usuario = [r for r in reviews if r['id_usuario'] == str(usuario_id)]
    except FileNotFoundError:
        reviews_usuario = []
    return {
        'jogados': 0,
        'quero_jogar': 0,
        'reviews': len(reviews_usuario)
    }

def _get_generos(jogos):
    generos = set()
    for jogo in jogos:
        for g in jogo['genre'].split('|'):
            generos.add(g.strip())
    return sorted(generos)

def _get_populares(jogos, limite=5):
    ordenados = sorted(jogos, key=lambda j: float(j['rating']), reverse=True)
    return ordenados[:limite]

@usuario.route('/principal')
def pg_principal():
    if not session.get('usuario_id'):
        return redirect(url_for('main.index'))
    jogos = ler_csv(ARQUIVOS_JOGOS)
    generos = _get_generos(jogos)
    populares = _get_populares(jogos)
    genero_ativo = None
    stats = _get_stats(session['usuario_id'])
    return render_template(
        'pg_principal.html',
        valores=jogos,
        generos=generos,
        populares=populares,
        genero_ativo=genero_ativo,
        stats=stats
    )

@usuario.route('/biblioteca')
def biblioteca():
    if not session.get('usuario_id'):
        return redirect(url_for('main.index'))
    return render_template('biblioteca.html')

@usuario.route('/watchlist')
def watchlist():
    if not session.get('usuario_id'):
        return redirect(url_for('main.index'))
    return render_template('watchlist.html')

@usuario.route('/reviews')
def reviews():
    if not session.get('usuario_id'):
        return redirect(url_for('main.index'))
    return render_template('reviews.html')