'''
Este teste serve para conferir se a matriz que está em sudoku.txt é uma matriz válida
como um jogo de sudoku. Para isso a lógica adotamos para um jogo sudoku é uma matriz 9x9 numérica, como:

matrizSudoku: [[5, 3, 4, 6, 7, 8, 9, 1, 2]
               [6, 7, 2, 1, 9, 5, 3, 4, 8]
               [1, 9, 8, 3, 4, 2, 5, 6, 7]
               [8, 5, 9, 7, 6, 1, 4, 2, 3]
               [4, 2, 6, 8, 5, 3, 7, 9, 1]
               [7, 1, 3, 4, 2, 9, 8, 5, 6]
               [9, 6, 1, 5, 3, 7, 2, 8, 4]
               [2, 8, 7, 9, 1, 4, 6, 3, 5]
               [3, 4, 5, 2, 8, 6, 1, 7, 9]]
'''

path = 'sudoku.txt'

'''
Função responsável por ler o 'sudoku.txt'
'''
def txtToString():
    try:
        global path
        f = open('sudoku.txt', 'r')
        string = f.read()
        f.close()
        return string
    except:
        return False

'''
Função responsável por formatar aquilo que foi recebido do sudoku.txt via string em uma matriz númerica
'''
def formatarMatriz(tabuleiroString):
    try:
        matrizFormatada = []

        # Divide a string de leitura do tabuleiro em uma lista de strings
        matrizString = tabuleiroString.split('\n')

        for linhaString in matrizString:

            # Exemplo de linha de matrizString: [5, 3, 4, 6, 7, 8, 9, 1, 2]
            # Esse comando abaixo formata a string para: 5, 3, 4, 6, 7, 8, 9, 1, 2
            linhaString = linhaString[1:-1]

            # Quebra a string em uma lista
            linhaLista = linhaString.split(', ')

            # Adiciona a linha formatada na matrizFormatada
            matrizFormatada.append(linhaLista)

        # Passa cada célula/casa da matriz para inteiro
        for i in range(len(matrizFormatada)):
            for j in range(len(matrizFormatada[i])):
                matrizFormatada[i][j] = int(matrizFormatada[i][j])

        # Confere o tamanho do tabuleiro
        # Compara o tamanho de linhas, compara o tamanho de colunas
        if len(matrizFormatada) != 9 or len(matrizFormatada[0]) != 9:
            return False

        return matrizFormatada
    except:
        return False


def testarFormatoMatriz():
    # Lê o arquivo 'sudoku.txt'
    tabuleiroSudoku = txtToString()

    # Se o existe uma string aí dentro, é pq existe um arquivo 'sudoku.txt', se não, existe "False"
    if tabuleiroSudoku:
        matrizSudoku = formatarMatriz(tabuleiroSudoku)
        if matrizSudoku:
            return matrizSudoku
    return False


print(f'\033[;33;40m"Teste 1: formato do tabuleiro" passado?\033[m {testarFormatoMatriz() != False}')

if testarFormatoMatriz():
    print('--- MATRIZ DO TABULEIRO SUDOKU ---')
    for linha in testarFormatoMatriz():
        print(linha)
