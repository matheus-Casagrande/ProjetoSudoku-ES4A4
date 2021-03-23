'''
Este teste serve para testar a existência do arquivo 'ranking.txt' no diretório 'jogo'

Neste módulo, importa-se o módulo "posiciona_amostra" que vai tentar copiar o arquivo
se o mesmo existir na pasta 'jogo'. Se não for criado um 'ranking.txt' dentro dessa
pasta de testes, é porque o ranking.txt original não existe.

Este módulo é importante também porque ele dará um "refresh" e vai excluir o ranking.txt
antigo, se o mesmo estiver aqui. Atualizando com o 'ranking.txt' da pasta 'jogo'
'''

from posiciona_amostra import copiarRankingTxt
import os


def testarExistenciaArquivo():
    # Remove o arquivo 'ranking.txt' do diretório 'testes_Ranking' se o mesmo existir
    try:
        os.remove('ranking.txt')
    except:
        pass

    # Copia o ranking.txt do diretório 'jogo' para o diretório 'testes_Ranking', se este existir
    copiarRankingTxt()

    try:
        f = open('ranking.txt', 'r')
        string = f.read()
        f.close()

        # Envia para frente a string do conteúdo de "ranking.txt"
        return string
    except:
        return False


print(f'\n\033[;33;40m"Teste 1: confere existência do arquivo ranking" passado?\033[m {testarExistenciaArquivo() is not False}')
if testarExistenciaArquivo():
    print('--- Conteúdo do arquivo ---')
    print(testarExistenciaArquivo())
    print('--- Fim do arquivo ---')
