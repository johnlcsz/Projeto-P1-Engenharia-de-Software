from app.services.csv_service import ler_csv
from app.services.user_service import ARQUIVO_REVIEWS

def calcular_nota(id_jogo: str):
    '''
    Calcula a nota de um jogo a partir das notas do arquivo de reviews.
    '''
    reviews = ler_csv(ARQUIVO_REVIEWS)
    soma = cont = 0
    for r in reviews:
        if r['id_jogo'] == str(id_jogo):
            soma += int(r['nota'])
            cont += 1
    if cont != 0:
        return round(soma / cont, 1)
    return None

def usuario_ja_avaliou(id_usuario: str, id_jogo:str) -> bool:
    '''
    Verifica se o usuário já avaliou um jogo.
    '''
    reviews = ler_csv(ARQUIVO_REVIEWS)
    for r in reviews:
        if id_usuario == r['id_usuario'] and str(id_jogo) == r['id_jogo']:
            return True
    return False

def usuario_pode_editar(id_usuario:str, review: dict) -> bool:
    '''
    Verifica se a avaliação pertece ao usuário.
    '''
    return id_usuario == review['id_usuario']