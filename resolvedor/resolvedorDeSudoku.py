'''
    Resolvedor de sudoku
    --------------------
    Explicação: esse programa recebe uma matriz 9x9 de um jogo de sudoku possível
    e retorna uma outra matriz 9x9 com uma resposta possível desse mesmo jogo de
    sudoku.

    (in a nutshell)
    resolverSudoku(jogoIncompleto):
        return jogoResolvido
'''

'''
    Essa função imprime uma matriz formatada no console, 
    usada para facilitar o desenvolvimento.
'''


def imprimirMatriz(matriz):
    for linha in matriz:
        print(linha)


'''
    Verifica uma casa da matriz (x, y) para um número n retornando true ou false.
    Onde x é a posição horizontal (de 0 a 8) e y a vertical (de 0 a 8).
    n é um número qualquer que habita a casa de coordenadas (x, y).
    
    Exemplo de aplicação
    possivel(5, 3, 2) -> true
    possivel(1, 6, 4) -> false
'''


def possivel(y, x, n):
    global matriz

    # Confere a linha inteira
    for i in range(0, 9):
        if matriz[y][i] == n:
            return False

    # Confere a coluna inteira
    for i in range(0, 9):
        if matriz[i][x] == n:
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
            if matriz[y0 + i][x0 + j] == n:
                return False

    # Se passou por todas as condicionais e não retornou false, retorna True
    return True


'''
    A função que sustenta a lógica principal do algoritmo.
    Ela é uma função recursiva (que chama a si mesma).
    
    A recursividade vai testando vários caminhos possíveis e
    averiguando as respostas plausíveis para o quebra-cabeça.
    
    Os dois underline (__) no começo da função a faz ser privada
    apenas para o módulo resolvedorDeSudoku.
'''
def __resolve():
    global matriz

    for y in range(0, 9):  # Rastreia os valores verticais
        for x in range(0, 9):  # Rastreia os valores horizontais
            # Verifica se a casa do sudoku está vazia
            if matriz[y][x] == 0:
                for i in range(1, 10):  # Números de 1 a 9
                    # Se o número específico é possível para tal casa...
                    if possivel(y, x, i):
                        matriz[y][x] = i  # ... então a matriz recebe ele na casa y,x
                        __resolve()  # A função é chamada recursivamente de novo, para resolver com o novo resultado
                        '''
                            Caso o programa chegue na linha abaixo é porque ele não retornou, dessa forma,
                            algo deu errado e toda recursividade deve começar do ponto inicial e tentar
                            outra possibilidade. 
                        '''
                        matriz[y][x] = 0
                return  # O return só é alcançado quando a matriz estiver completa, e tal só acontece se todos
                # resultados estão corretos.


def resolverSudoku(jogoIncompleto):
    global matriz
    matriz = jogoIncompleto
    __resolve()
    jogoResolvido = matriz
    return jogoResolvido
