import pygame, sys
from settings import *
from buttonClass import *


class App:
    def __init__(self):
        pygame.init()

        # Configura a janela do jogo
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

        # Seta o estado de 'rodando' ao programa
        self.running = True

        # Guarda a matriz do tabuleiro de sudoku
        self.grid = testBoard2

        # Armazena a informação do botão selecionado atualmente
        self.selected = None

        # Rastreia a posição do mouse
        self.mousePos = None

        # Guarda o estado do jogo
        self.state = "playing"

        # Botões para cada estado do jogo
        self.playingButtons = []
        self.menuButtons = []
        self.endButtons = []

        # Carrega os botões de cada estado
        self.loadButtons()

        # Define uma fonte para o jogo (fonte, tamanho)
        self.font = pygame.font.SysFont("arial", cellSize//2)


    def run(self):

        # Enquanto o programa estiver rodando, executar os métodos:
        while self.running:
            if self.state == "playing":
                # Função que detecta os eventos do jogo
                self.playing_events()

                # Função que realiza os updates do jogo
                self.playing_update()

                # Função que se responsabiliza por desenhar a GUI
                self.playing_draw()

        # Quando sair do while, chama os métodos de saída
        pygame.quit()
        sys.exit()

    ##### FUNÇÕES DO ESTADO "JOGANDO" #####

    def playing_events(self):
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

    def playing_update(self):
        # Atualiza a posição do mouse
        self.mousePos = pygame.mouse.get_pos()

        # Lógica de verificar se um botão está pressionado ou não
        for button in self.playingButtons:
            button.update(self.mousePos)

    def playing_draw(self):

        # Seta a cor a ser preenchida como branca
        self.window.fill(WHITE)

        # Desenha os botões
        for button in self.playingButtons:
            button.draw(self.window)

        # Desenha a casa selecionada
        if self.selected:
            self.drawSelection(self.window, self.selected)

        # Desenha os números a partir de uma matriz
        self.drawNumbers(self.window)

        # Desenha a grade (grid) do sudoku enviando o "palco" self.window como parâmetro
        self.drawGrid(self.window)

        # Atualiza o display
        pygame.display.update()

    ##### FUNÇÕES AUXILIARES #####

    def drawNumbers(self, window):
        # yidx = index y, row = linha, xidx = index x
        for yidx, row in enumerate(self.grid):
            for xidx, number in enumerate(row):
                # Se o número da grade estiver como 0, ele será vazio
                if number != 0:
                    # Seta a posição para a casa que o loop for está lendo
                    pos = [(xidx*cellSize) + gridPos[0], (yidx*cellSize) + gridPos[1]]

                    # Imprime o número com essa posição (janela, texto, posição)
                    self.textToScreen(window, str(number), pos)


    def drawSelection(self, window, pos):
        # Desenha um retângulo com os seguintes parâmetros:
        # (A janela onde vai desenhar, a cor do retângulo, a posição (left, top, tamanho pra direita, tamanho pra esquerda))
        pygame.draw.rect(window, LIGHTBLUE,
                         ((pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))

    def drawGrid(self, window):

        # Desenha um retângulo com os seguintes parâmetros:
        # (A janela onde vai desenhar, a cor do retângulo, a posição (left, top, tamanho pra direita, tamanho pra baixo), o tamanho da borda)
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH - 150, HEIGHT - 150), 2)

        # Desenha os traços do tabuleiro
        for x in range(9):

            # Para que a cada três linhas o programa desenhe uma linha mais grossa
            if x % 3 != 0:
                '''Desenha a coluna'''
                # Desenha uma linha com os seguintes parâmetros:
                # (A janela onde vai desenhar, a cor da linha, a posição do ponto inicial, a posição do ponto final)
                # (gridPos[0] + (x* cellSize)) se refere a posição x (horizontal) na janela, gridPos à borda esquerda do tabuleiro e cellSize o tamanho da casa
                # (gridPos[1]) se refere a posição y (vertical) na janela. Então temos (x, y) para definir a posição do ponto.
                pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellSize), gridPos[1]),
                                 (gridPos[0] + (x * cellSize), gridPos[1] + 450))

                '''Desenha a linha'''
                # Faz a mesma coisa que o comando anterior, mas adaptando pra que seja uma linha horizontal
                pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x * cellSize)),
                                 (gridPos[0] + 450, gridPos[1] + (x * cellSize)))
            else:
                '''Desenha a coluna'''
                # Faz o mesmo que o comando anterior, mas no final o parâmetro 2 engrossa a linha para 2px, em vez do padrão 1px
                pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellSize), gridPos[1]),
                                 (gridPos[0] + (x * cellSize), gridPos[1] + 450), 2)

                '''Desenha a linha'''
                # Repete o comando da linha, engrossando 2px
                pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x * cellSize)),
                                 (gridPos[0] + 450, gridPos[1] + (x * cellSize)), 2)

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
        return ((self.mousePos[0] - gridPos[0]) // cellSize, (self.mousePos[1] - gridPos[1]) // cellSize)

    def loadButtons(self):
        # Adiciona um botão
        # Parâmetros: (posLeft, posTop, width, height)
        self.playingButtons.append(Button(20, 40, 100, 40))

    def textToScreen(self, window, text, pos):
        # Cria uma imagem com um texto (texto, antialias, cor)
        font = self.font.render(text, False, BLACK)

        # Reajusta a posição para ficar no centro da casa
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth) // 2
        pos[1] += (cellSize - fontHeight) // 2

        # Coloca o objeto font na janela
        window.blit(font, pos)
