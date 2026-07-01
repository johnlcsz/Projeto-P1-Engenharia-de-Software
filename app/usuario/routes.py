from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.services.csv_service import ler_csv, adicionar_linha, gerar_id, escrever_csv
from app.services.user_service import ARQUIVOS_JOGOS, ARQUIVO_REVIEWS, COLUNAS_REVIEWS
from app.services.reviews_service import calcular_nota, usuario_ja_avaliou, usuario_pode_editar

usuario = Blueprint('usuario', __name__)

def _get_stats(usuario_id: str) -> dict:
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

def _get_generos(jogos: list[dict]) -> set:
    generos = set()
    for jogo in jogos:
        for g in jogo['genre'].split('|'):
            generos.add(g.strip())
    return sorted(generos)

def _get_populares(jogos: list[dict], limite=5) -> list[dict]:
    ordenados = sorted(jogos, key=lambda j: float(j['nota_usuarios']) if j['nota_usuarios'] is not None else 0, reverse=True)
    return ordenados[:limite]

@usuario.route('/principal')
def pg_principal():
    if not session.get('usuario_id'):
        return redirect(url_for('main.index'))

    jogos = ler_csv(ARQUIVOS_JOGOS)
    generos = _get_generos(jogos)
    stats = _get_stats(session['usuario_id'])

    for jogo in jogos:
        jogo['nota_usuarios'] = calcular_nota(jogo['id'])
    populares = _get_populares(jogos)

    genero_ativo = request.args.get('genero', '').strip()
    # Filtra os jogos se um gênero foi selecionado
    if genero_ativo:
        jogos_filtrados = [
            j for j in jogos
            if genero_ativo in [g.strip() for g in j['genre'].split('|')]
        ]
    else:
        jogos_filtrados = jogos

    return render_template(
        'pg_principal.html',
        valores=jogos_filtrados,
        generos=generos,
        populares=populares,
        genero_ativo=genero_ativo,
        stats=stats
    )


@usuario.route('/jogo/<int:jogo_id>')
def detalhes(jogo_id):
    
    # Se existir, indica qual avaliação deve ser exibida em modo de edição
    review_id = request.args.get('editar')

    jogos = ler_csv(ARQUIVOS_JOGOS)
    jogo = next((j for j in jogos if int(j['id']) == jogo_id), None)
    if not jogo:
        return redirect(url_for('usuario.pg_principal'))
    try:
        reviews = ler_csv(ARQUIVO_REVIEWS)
        reviews_jogo = [r for r in reviews if r['id_jogo'] == str(jogo_id)]
    except FileNotFoundError:
        reviews_jogo = []

    jogo['nota_usuarios'] = calcular_nota(jogo['id'])

    ja_avaliou = usuario_ja_avaliou(session.get('usuario_id'), jogo_id)
    review_editando = None

    if review_id:
        review_editando = next((r for r in reviews_jogo if review_id == r['id']), None)
        if review_editando:
            if not usuario_pode_editar(session.get('usuario_id'), review_editando):
                flash('Você não tem permissão para editar essa avaliação.', 'geral')
                return redirect(url_for('usuario.detalhes', jogo_id=jogo_id))
        else:
            flash('Essa avaliação não existe.', 'geral')
            return redirect(url_for('usuario.detalhes', jogo_id=jogo_id))
        
    return render_template('detalhes.html', jogo=jogo, reviews=reviews_jogo, review_id=review_id, ja_avaliou=ja_avaliou, review_editando=review_editando)

@usuario.route('/avaliar/<int:jogo_id>', methods=['POST'])
def avaliar(jogo_id):

    if not session.get('usuario_id'):
        return redirect(url_for('main.index', modal='register'))
    
    if usuario_ja_avaliou(session['usuario_id'], jogo_id):
        flash('Você já avaliou esse jogo.', 'geral')
        return redirect(url_for('usuario.detalhes', jogo_id=jogo_id))

    nota = request.form.get('nota', '0')
    comentario = request.form.get('comentario', '').strip()

    if not nota or int(nota) == 0:
        flash('Selecione uma nota antes de salvar!', 'geral')
        return redirect(url_for('usuario.detalhes', jogo_id=jogo_id))
    
    nova_review = {
        'id': gerar_id(ARQUIVO_REVIEWS),
        'id_usuario': session['usuario_id'],
        'autor': session['usuario_nome'],
        'id_jogo': str(jogo_id),
        'nota': nota,
        'comentario': comentario
    }

    adicionar_linha(ARQUIVO_REVIEWS, COLUNAS_REVIEWS, nova_review)
    flash('Avaliação publicada com sucesso!', 'geral')
    return redirect(url_for('usuario.detalhes', jogo_id=jogo_id))

@usuario.route('/editar/<review_id>', methods=['POST'])
def editar(review_id):
    if not session.get('usuario_id'):
        return redirect(url_for('main.index', modal='register'))
    
    nota = request.form.get('nota', '0')
    comentario = request.form.get('comentario', '').strip()

    review_encontrada = False
    reviews = ler_csv(ARQUIVO_REVIEWS)
    for r in reviews:
        if r['id'] == review_id:
            review_encontrada = True
            jogo_id = r['id_jogo']

            if not usuario_pode_editar(session.get('usuario_id'), r):
                flash('Você não tem permissão para editar essa avaliação.', 'geral')
                return redirect(url_for('usuario.detalhes', jogo_id=jogo_id))
            
            if not nota or int(nota) == 0:
                flash('Selecione uma nota antes de salvar!', 'geral')
                return redirect(url_for('usuario.detalhes', jogo_id=jogo_id, review_id=review_id))
            
            r['nota'] = nota
            r['comentario'] = comentario
            break
    
    if not review_encontrada:
        flash('Essa avaliação não existe.', 'geral')
        return redirect(url_for('usuario.pg_principal'))

    escrever_csv(ARQUIVO_REVIEWS, COLUNAS_REVIEWS, reviews)
    flash('Avaliação editada com sucesso!', 'geral')
    return redirect(url_for('usuario.detalhes', jogo_id=jogo_id))

@usuario.route('/deletar/<review_id>', methods=['POST'])
def deletar(review_id):
    if not session.get('usuario_id'):
        return redirect(url_for('main.index', modal='register'))

    review_encontrada = False
    reviews = ler_csv(ARQUIVO_REVIEWS)
    novas_reviews = []
    for r in reviews:
        if r['id'] == review_id:
            review_encontrada = True
            jogo_id = r['id_jogo']

            if not usuario_pode_editar(session.get('usuario_id'), r):
                flash('Você não tem permissão para excluir essa avaliação.', 'geral')
                return redirect(url_for('usuario.detalhes', jogo_id=jogo_id))
            
            continue
        novas_reviews.append(r)
    
    if not review_encontrada:
        flash('Essa avaliação não existe.', 'geral')
        return redirect(url_for('usuario.pg_principal'))

    escrever_csv(ARQUIVO_REVIEWS, COLUNAS_REVIEWS, novas_reviews)
    flash('Avaliação excluída com sucesso!', 'geral')
    return redirect(url_for('usuario.detalhes', jogo_id=jogo_id))


    # Rota para o perfil
@usuario.route('/perfil')
def perfil():
    if not session.get('usuario_id'):
        return redirect(url_for('main.index'))

    jogos = ler_csv(ARQUIVOS_JOGOS)
    try:
        reviews_csv = ler_csv(ARQUIVO_REVIEWS)
        reviews_usuario = [r for r in reviews_csv if r['id_usuario'] == str(session['usuario_id'])]
    except FileNotFoundError:
        reviews_usuario = []

    ids_avaliados = {r['id_jogo'] for r in reviews_usuario}
    jogos_avaliados = [j for j in jogos if j['id'] in ids_avaliados]

    reviews_com_jogo = []
    for r in reviews_usuario:
        jogo_da_review = next((j for j in jogos if j['id'] == r['id_jogo']), None)
        if jogo_da_review:
            reviews_com_jogo.append({
                'jogo': jogo_da_review,
                'nota': r['nota'],
                'comentario': r['comentario']
            })

    if reviews_usuario:
        media = sum(float(r['nota']) for r in reviews_usuario) / len(reviews_usuario)
        media_notas = round(media, 1)
    else:
        media_notas = 0

    return render_template(
        'perfil.html',
        jogos_avaliados=jogos_avaliados,
        reviews=reviews_com_jogo,
        media_notas=media_notas
    )