from datetime import datetime

def registrar_log(mensagem):
    with open('data/logs.txt', 'a', encoding='utf-8') as f:
        horario = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        f.write(f'[{horario}] {mensagem}\n')