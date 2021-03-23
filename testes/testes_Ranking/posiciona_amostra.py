'''
Este módulo serve para capturar da aplicação o objeto a ser analisado pelos testes.

Para este teste de aceitação, esse algoritmo vai copiar da pasta "jogo" o arquivo "ranking.txt" para
dentro de um outro txt nesta pasta, para que este ranking seja posto a experimento.
'''

import sys
sys.path.append('..')  # faz o interpretador do python conhecer a pasta anterior
sys.path.append('...')


def copiarRankingTxt():
    try:
        # Este endereço é relativo ao módulo "posiciona_amostra.py" dentro da pasta 'testes_Ranking'
        f = open('../../jogo/ranking.txt', 'r')
        string = f.read()
        f.close()
        f2 = open('ranking.txt', 'w')
        f2.write(string)
        f2.close()
    except:
        pass
