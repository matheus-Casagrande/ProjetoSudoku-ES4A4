'''
Teste de aceitação da funcionalidade Ranking: confere se todos os testes de ranking estão corretos
'''

from teste3_verificarOrdemCorreta import testarOrdemCorreta

if testarOrdemCorreta():
    print('\033[;32mTESTE DE ACEITAÇÃO DE RANKING PASSADO\033[m')
else:
    print('\033[;31mTESTE DE ACEITAÇÃO DE RANKING FALHADO\033[m')