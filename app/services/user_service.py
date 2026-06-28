from app.services.csv_service import *
from werkzeug.security import generate_password_hash, check_password_hash

#Constantes do caminho dos arquivos CSV
ARQUIVO_USUARIOS = 'data/usuarios.csv'
ARQUIVOS_JOGOS = 'data/jogos.csv'
ARQUIVO_REVIEWS = 'data/reviews.csv'

#Constantes dos cabeçalhos dos arquivos CSV
COLUNAS_USUARIOS = ['id', 'nome', 'email', 'senha_hash']
COLUNAS_REVIEWS = ['id', 'id_usuario', 'autor' , 'id_jogo', 'nota', 'comentario']

def busca_usuario_email(email:str) -> dict:
    usuarios = ler_csv(ARQUIVO_USUARIOS)
    for usuario in usuarios:
        if usuario['email'] == email:
            return usuario

#Validação
def email_existe(email):
    '''
    Verifica se o email já está sendo usado.
    '''
    for usuario in ler_csv(ARQUIVO_USUARIOS):
        if usuario['email'] == email:
            return True
    return False

def validar_nome(nome):
    '''
    Verifica se o nome atende aos requisitos.
    '''
    return len(nome) >= 3 and len(nome) <= 20

def nome_existe(nome):
    '''
    Verifica se o nome está diponível pra ser usado.
    '''
    for usuario in ler_csv(ARQUIVO_USUARIOS):
        if usuario['nome'] == nome:
            return True
    return False

def validar_senha(senha):
    '''
    Verifica se a senha atende aos requisitos.
    '''
    tem_letra = tem_numero = False
    if len(senha) < 6 or len(senha) > 20:
        return False
    for caractere in senha:
        if caractere.isalpha():
            tem_letra = True
        elif caractere.isdigit():
            tem_numero = True
        if tem_letra and tem_numero:
            return True
    return False

def senha_correta(usuario:dict, senha:str) -> bool:
    '''
    Verifica se a senha informada pelo usuário corresponde ao hash salvo.
    '''
    return check_password_hash(usuario['senha_hash'], senha)

    
#Ação
def criar_usuario(nome: str, email: str, senha: str) -> str:
    '''
    Gera id do usuário, hash da senha e salva as informações no arquivo CSV.
    '''
    #Gera id
    novo_id = gerar_id(ARQUIVO_USUARIOS)

    #Gera hash
    senha_hash = generate_password_hash(senha)

    #Salva informações
    usuario = {
        'id': novo_id,
        'nome': nome,
        'email': email,
        'senha_hash': senha_hash
    }
    adicionar_linha(ARQUIVO_USUARIOS, COLUNAS_USUARIOS, usuario)

    return novo_id