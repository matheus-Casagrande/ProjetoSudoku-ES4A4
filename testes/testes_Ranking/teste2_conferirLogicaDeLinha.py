'''
Este teste serve para testar a lógica de criação de uma linha do ranking.
    - Ele retornará "false" se não existir nenhuma linha dentro do ranking.
    - Ele verificará se cada linha do arquivo cumpre tais requisitos:
        (posição, tempo de conclusão, nome)
    - Exemplo de linha:
        1 321 Gabriel
    - Para tal, ele irá conferir se cada linha tem: 1 elemento inteiro, 1 elemento float, 1 elemento string; divindindo
    cada linha em uma lista
'''

from teste1_confereExistenciaArquivo import testarExistenciaArquivo

def testarLogicaDeLinha():
    # Este teste depende do anterior ter passado para passar
    stringArquivo = testarExistenciaArquivo()

    # Se o teste falhou no anterior, stringArquivo recebe um booleano False
    if stringArquivo is False:
        return False
    else:
        try:
            # Divide a string em cada quebra de linha e retorna para o array "matrizString"
            matrizString = stringArquivo.split('\n')
            matrizLista = []

            for linhaString in matrizString:
                # Cada linha de "matrizLista" recebe uma lista dividida de cada linha de "matrizString"
                matrizLista.append(linhaString.split(' '))

            posicao1 = None
            posicao2 = None
            posicao3 = None

            for linhaLista in matrizLista:
                try:

                    posicao1 = int(linhaLista[0])
                    posicao2 = float(linhaLista[1])
                    posicao3 = str(linhaLista[2])
                except:
                    return False

            # print(f'posicao1 = {posicao1} | posicao2 = {posicao2} | posicao3 = {posicao3}')

            # Se passou na lógica anterior, passa a matriz lista do ranking para o teste 3
            return matrizLista
        except:
            return False

print(f'\n\033[;33;40m"Teste 2: confere lógica do arquivo ranking" passado?\033[m {testarLogicaDeLinha() is not False}')
