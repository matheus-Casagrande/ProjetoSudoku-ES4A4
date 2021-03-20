WIDTH = 600
HEIGHT = 600

# Cores definidas (tupla no padrão RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (96, 216, 232)
LOCKEDCELLCOLOUR = (189, 189, 189)
INCORRECTCELLCOLOUR = (195, 121, 121)
DARKRED = (110, 0, 0)
LIGHTGREEN = (117, 172, 112)

# Ranking
RANKING = ["1 321 Gabriel",
            "2 400 Any",
            "3 445 Matheus",
            "4 470 Fulano",
            "5 503 Ciclano"]


# Boards (tabuleiros)
testBoard = [[0 for x in range(9)] for x in range(9)]   # forma uma matriz 9x9 com '0s'
testBoard2 = [[0, 6, 0, 2, 0, 0, 8, 3, 1],
              [0, 0, 0, 0, 8, 4, 0, 0, 0],
              [0, 0, 7, 6, 0, 3, 0, 4, 9],
              [0, 4, 6, 8, 0, 2, 1, 0, 0],
              [0, 0, 3, 0, 9, 6, 0, 0, 0],
              [1, 2, 0, 7, 0, 5, 0, 0, 6],
              [7, 3, 0, 0, 0, 1, 0, 2, 0],
              [8, 1, 5, 0, 2, 9, 7, 0, 0],
              [0, 0, 0, 0, 7, 0, 0, 1, 5]]

finishedBoard = [[0, 3, 4, 6, 7, 8, 9, 1, 2],
                 [6, 7, 2, 1, 9, 5, 3, 4, 8],
                 [1, 9, 8, 3, 4, 2, 5, 6, 7],
                 [8, 5, 9, 7, 6, 1, 4, 2, 3],
                 [4, 2, 6, 8, 5, 3, 7, 9, 1],
                 [7, 1, 3, 9, 2, 4, 8, 5, 6],
                 [9, 6, 1, 5, 3, 7, 2, 8, 4],
                 [2, 8, 7, 4, 1, 9, 6, 3, 5],
                 [3, 4, 5, 2, 8, 6, 1, 7, 9]]

# Posição e tamanho da grade (Positions and sizes)
gridPos = (75, 100)  # grid Position (left, top)px from border
cellSize = 50  # tamanho de uma cada do sudoku (1 quadradinho dos 9x9)
gridSize = cellSize * 9  # tamanho do tabuleiro de sudoku

