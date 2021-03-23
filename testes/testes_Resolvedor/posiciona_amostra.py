'''
Este módulo serve para capturar da aplicação o objeto a ser analisado pelos testes.

Para este teste de aceitação, esse algoritmo vai copiar do programa a matriz do sudoku para
dentro de um txt nesta pasta, para que ela seja posta a experimento.
'''

import sys
sys.path.append('..')  # faz o interpretador do python conhecer a pasta anterior
sys.path.append('...')


def sudokuToTxt(matriz):
    # Este endereço é relativo ao módulo "app_class.py" dentro da pasta jogo no diretório raiz
    f = open('../testes/testes_Resolvedor/sudoku.txt', 'w')
    print('Arquivo sudoku.txt criado em testes/testes_Resolvedor')
    matrizString = []

    # transforma as linhas da matriz em linhas string e passa para matrizString essa informação
    for linha in matriz:
        matrizString.append(f'{str(linha)}\n')

    # retira o último '\n' de matrizString
    matrizString[-1] = matrizString[-1][0:-1]

    f.writelines(matrizString)
    f.close()
