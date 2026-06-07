import csv

def ler_csv(arquivo: str) -> list:
    '''
    Lê os dados do arquivo e retorna os valores de cada linha.
    '''
    valores = []
    with open(arquivo, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for linha in reader:
            valores.append(linha)
    return valores

def escrever_csv(arquivo: str, colunas: list, dados: list[dict]) -> None:
    '''
    Reescreve os dados recebidos no lugar dos dados do arquivo. 
    '''
    with open(arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(dados)

def adicionar_linha(arquivo: str, colunas: list, linha: dict) -> None:
    '''
    Adiciona uma linha no final do arquivo.
    '''
    with open(arquivo, newline='', mode='a',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writerow(linha)

def gerar_id(arquivo: str) -> str:
    '''
    Gera uma id nova para cada nova avaliação ou review.
    '''
    valores = ler_csv(arquivo)
    novo_id = max([int(v['id']) for v in valores], default=0) + 1
    return str(novo_id)