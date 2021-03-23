'''
Teste de aceitação da funcionalidade 'Resolver Sudoku': confere se todos os testes de Resolvedor estão corretos
'''

from teste2_sudokuResolvido import testarSudokuResolvido

if testarSudokuResolvido():
    print('\033[;32mTESTE DE ACEITAÇÃO DE RESOLVEDOR DE SUDOKU PASSADO\033[m')
else:
    print('\033[;31mTESTE DE ACEITAÇÃO DE RESOLVEDOR DE SUDOKU FALHADO\033[m')