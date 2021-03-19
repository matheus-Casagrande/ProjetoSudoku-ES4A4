import pygame, sys
from settings import *


class App:
    def __init__(self):
        pygame.init()

        # Configura a janela do jogo
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

        # Seta o estado de 'rodando' ao programa
        self.running = True

        # Guarda a matriz do tabuleiro de sudoku
        self.grid = testBoard

        # Armazena a informação do botão selecionado atualmente
        self.selected = None

        # Rastreia a posição do mouse
        self.mousePos = None

    def run(self):

        # Enquanto o programa estiver rodando, executar os métodos:
        while self.running:

            # Função que detecta os eventos do jogo
            self.events()

            # Função que realiza os updates do jogo
            self.update()

            # Função que se responsabiliza por desenhar a GUI
            self.draw()

        # Quando sair do while, chama os métodos de saída
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():

            # Captura o evento de saída do programa
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()

                # selected pode ser False ou uma tupla com a casa do jogo que foi selecionada
                if selected:
                    self.selected = selected
                else:
                    print("Not on board")
                    self.selected = None

    def update(self):
        # Atualiza a posição do mouse
        self.mousePos = pygame.mouse.get_pos()

    def draw(self):

        # Seta a cor a ser preenchida como branca
        self.window.fill(WHITE)

        # Desenha a casa selecionada
        if self.selected:
            self.drawSelection(self.window, self.selected)

        # Desenha a grade (grid) do sudoku enviando o "palco" self.window como parâmetro
        self.drawGrid(self.window)

        # Atualiza o display
        pygame.display.update()

    def drawSelection(self, window, pos):
        # Desenha um retângulo com os seguintes parâmetros:
        # (A janela onde vai desenhar, a cor do retângulo, a posição (left, top, tamanho pra direita, tamanho pra esquerda))
        pygame.draw.rect(window, LIGHTBLUE, ((pos[0]*cellSize) + gridPos[0], (pos[1]*cellSize) + gridPos[1], cellSize, cellSize))

    def drawGrid(self, window):

        # Desenha um retângulo com os seguintes parâmetros:
        # (A janela onde vai desenhar, a cor do retângulo, a posição (left, top, tamanho pra direita, tamanho pra baixo), o tamanho da borda)
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH - 150, HEIGHT - 150), 2)

        for x in range(9):

            # Para que a cada três linhas o programa desenhe uma linha mais grossa
            if x % 3 != 0:
                '''Desenha a coluna'''
                # Desenha uma linha com os seguintes parâmetros:
                # (A janela onde vai desenhar, a cor da linha, a posição do ponto inicial, a posição do ponto final)
                # (gridPos[0] + (x* cellSize)) se refere a posição x (horizontal) na janela, gridPos à borda esquerda do tabuleiro e cellSize o tamanho da casa
                # (gridPos[1]) se refere a posição y (vertical) na janela. Então temos (x, y) para definir a posição do ponto.
                pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellSize), gridPos[1]), (gridPos[0] + (x * cellSize), gridPos[1] + 450))

                '''Desenha a linha'''
                # Faz a mesma coisa que o comando anterior, mas adaptando pra que seja uma linha horizontal
                pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x * cellSize)), (gridPos[0] + 450, gridPos[1] + (x * cellSize)))
            else:
                '''Desenha a coluna'''
                # Faz o mesmo que o comando anterior, mas no final o parâmetro 2 engrossa a linha para 2px, em vez do padrão 1px
                pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellSize), gridPos[1]), (gridPos[0] + (x * cellSize), gridPos[1] + 450), 2)

                '''Desenha a linha'''
                # Repete o comando da linha, engrossando 2px
                pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x * cellSize)), (gridPos[0] + 450, gridPos[1] + (x * cellSize)), 2)

    '''
    Comentário da função mouseOnGrid():
        Se o mouse estiver fora dentro do tabuleiro, ele retornará false,
        mas, se ele estiver dentro, ele retornará a casa que foi clicada.
        Essa função é chamada toda vez que ocorre um evento de click.
    '''
    def mouseOnGrid(self):
        # Confere se a posição do mouse está fora do tabuleiro pra menos
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False

        # Confere se a posição do mouse está fora do tabuleiro pra mais
        if self.mousePos[0] > gridPos[0] + gridSize or self.mousePos[1] > gridPos[1] + gridSize:
            return False

        # Se a função chegou até aqui, é pq a posição do mouse está dentro do tabuleiro, então:
        return ((self.mousePos[0]-gridPos[0])//cellSize, (self.mousePos[1]-gridPos[1])//cellSize)

