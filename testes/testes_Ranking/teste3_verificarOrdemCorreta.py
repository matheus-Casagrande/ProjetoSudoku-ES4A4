'''
Este teste serve para testar a posição do placar.
    - O placar armazenará os tempos de conclusão de cada participante
    - Uma posição tem o tempo que o participante demorou para resolver o sudoku
    - O placar deve manter na primeira posição o menor tempo e estar organizado nessa ordem
    de menor tempo para maior tempo

Um exemplo de ranking válido abaixo:
1 321 Gabriel
2 400 Any
3 445 Matheus
4 470 Fulano
5 503 Ciclano
'''

from teste2_conferirLogicaDeLinha import testarLogicaDeLinha
from copy import copy


def testarOrdemCorreta():
    ranking = testarLogicaDeLinha()

    if ranking is False:
        return False
    else:
        arrayPosicoes = []
        arrayTempos = []

        # Popula o arrayPosicoes com os números das posições do ranking
        for i in range(len(ranking)):
            arrayPosicoes.append(ranking[i][0])

        # Popula o arrayPosicoes com os números dos tempos do ranking
        for i in range(len(ranking)):
            arrayTempos.append(ranking[i][1])

        # Cria um array posições arrumado e o arruma
        arrayPosicoesArrumado = copy(arrayPosicoes)  # copy -> previne que o objeto seja declarado como uma referência
        arrayPosicoesArrumado.sort()

        # Cria um array tempos arrumado e o arruma
        arrayTemposArrumado = copy(arrayTempos)
        arrayTemposArrumado.sort()

        # Confere se os arrays anteriores são iguais às versões arrumadas deles
        if arrayPosicoes == arrayPosicoesArrumado and arrayTempos == arrayTemposArrumado:
            # Confere se as posições são uma ordem crescente de incremento 1 (1, 2, 3, 4, 5...)
            for i in range(0, len(arrayPosicoes)):
                if arrayPosicoes[i] != str(i+1):
                    return False
            return True
        else:
            return False


print(f'\n\033[;33;40m"Teste 3: verificar Ordem Correta" passado?\033[m {testarOrdemCorreta() is not False}')