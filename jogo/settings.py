WIDTH = 600
HEIGHT = 600

# Cores definidas (tupla no padrão RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (96, 216, 232)

# Boards (tabuleiros)
testBoard = [[0 for x in range(9)] for x in range(9)]   # forma uma matriz 9x9 com '0s'

# Posição e tamanho da grade (Positions and sizes)
gridPos = (75, 100)  # grid Position (left, top)px from border
cellSize = 50  # tamanho de uma cada do sudoku (1 quadradinho dos 9x9)
gridSize = cellSize * 9  # tamanho do tabuleiro de sudoku

