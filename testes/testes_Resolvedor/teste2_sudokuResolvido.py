'''
OBS inicial: Esse teste só irá passar se o aplicativo passou no teste anterior.

A ideia desse módulo de teste python é conferir se o tabuleiro resolvido
pelo algoritmo escrito em "resolvedor/resolvedorDeSudoku.py" está cumprindo o seu
papel e resolvendo o puzzle de Sudoku adequadamente.
'''

from teste1_FormatoMatriz import testarFormatoMatriz


def possivel(y, x, n):
    global matriz
    posicao = [y, x]  # Guarda a posição analisada

    # Confere a linha inteira
    for i in range(0, 9):
        # O 'and' serve para garantir que o comparador não está comparando a própria célula
        if matriz[y][i] == n and [y, i] != [y, x]:
            return False

    # Confere a coluna inteira
    for i in range(0, 9):
        if matriz[i][x] == n and [i, x] != [y, x]:
            return False

    # Confere um quadrado 3x3
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    '''
        x0 e y0 se referem à primeira casa do quadrado 3x3 da matriz
        ou seja:
        x 0 0
        0 0 0
        0 0 0
        Tal casa é definida a partir da posição (x, y) que 'n' está. 
        Há 9 quadrados 3x3 no tabuleiro de sudoku.
    '''

    for i in range(0, 3):
        for j in range(0, 3):
            if matriz[y0 + i][x0 + j] == n and [y0 + i, x0 + j] != [y, x]:
                return False

    # Se passou por todas as condicionais e não retornou false, retorna True
    return True

def testarSudokuResolvido():
    # Recebe o resultado do teste anterior
    tabuleiroSudoku = testarFormatoMatriz()

    # Se esse resultado é false, quer dizer que não passou, então:
    if tabuleiroSudoku is False:
        return False

    # Se esse resultado é uma matriz, quer dizer que passou
    else:
        # Define uma variável "matriz" como global para passar na lógica da função "possível"
        global matriz
        matriz = tabuleiroSudoku

        for y in range(9):
            for x in range(9):
                if possivel(y, x, matriz[y][x]) is False:
                    print(matriz[3][5])
                    return False
        return True


print(f'\n\033[;33;40m"Teste 2: sudoku resolvido" passado?\033[m {testarSudokuResolvido() is not False}')
