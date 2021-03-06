# IMPORTS DE DEPENDÊNCIA

import pygame, sys
import requests
from bs4 import BeautifulSoup
from settings import *
from buttonClass import *
sys.path.append('..')
from resolvedor.resolvedorDeSudoku import resolverSudoku
import time

# IMPORTS DE TESTE
from testes.testes_Resolvedor.posiciona_amostra import sudokuToTxt as importarTabuleiro


class App:
    def __init__(self, testes=False, tabuleiroTerminado=False):
        self.testes = testes
        pygame.init()

        # Configura a janela do jogo
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

        # Seta o estado de 'rodando' ao programa
        self.running = True

        # Armazena a informação do botão selecionado atualmente
        self.selected = None

        # Rastreia a posição do mouse
        self.mousePos = None

        # Guarda o estado do jogo
        self.state = "playing"

        # Verifica se o jogo acabou ou não
        self.finished = False

        # Rastreia se uma casa do sudoku foi alterada pelo jogador
        self.cellChanged = False

        # Botões
        self.playingButtons = []

        # Define uma fonte para o jogo (fonte, tamanho)
        self.font = pygame.font.SysFont("arial", cellSize//2)

        # Rastreia as celulas (casas) originais do puzzle de sudoku
        self.lockedCells = []

        # Guarda as casas que o jogador digitou incorretamente
        self.incorrectCells = []

        # Para lógica do timer
        self.timerIsOn = False  # Embora esteja em false, a função "getPuzzle" altera pra True
        self.startTime = time.time()
        self.time = time.time()

        # Guarda a matriz do tabuleiro de sudoku
        # self.grid = finishedBoard # Para debug
        self.grid = []
        self.getPuzzle("1")  # getPuzzle(1 = easy, 2 = medium, and so on)
        if self.testes and tabuleiroTerminado:
            self.grid = finishedBoard  # todo seta um tabuleiro terminado pro sudoku
            # todo remove a casa (0, 0) de "locked" para garantir a lógica de testagem
            try:
                self.lockedCells.remove([0,0])
            except:
                pass

        # Para indicar quando criar um ranking
        self.rankingMode = False

        # Para indicar quando o usuário acabou o jogo e vai colocar o nome dele
        self.finalScreen = False

        # Parâmetros da caixa de digitação do final
        self.input_rect = pygame.Rect(250, 250, 140, 32)
        self.input_color_active = pygame.Color('lightskyblue3')
        self.input_color_passive = pygame.Color('gray15')
        self.input_color = self.input_color_passive
        self.input_active = False
        self.input_texto = ''
        # self.clock = pygame.time.Clock()


    def run(self):

        # Enquanto o programa estiver rodando, executar os métodos:
        while self.running:
            if self.state == "playing":
                # Função que detecta os eventos do jogo
                self.events()

                # Função que realiza os updates do jogo
                self.update()

                # Função que se responsabiliza por desenhar a GUI
                self.draw()

        # Quando sair do while, chama os métodos de saída
        pygame.quit()
        sys.exit()

    ##### FUNÇÕES DO ESTADO "JOGANDO" #####

    def events(self):
        for event in pygame.event.get():

            # Captura o evento de saída do programa
            if event.type == pygame.QUIT:
                self.running = False

            # Eventos de clique
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()

                # selected pode ser False ou uma tupla com a casa do jogo que foi selecionada
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playingButtons:
                        if button.highlighted:
                            button.click()

                # Lógica para o botão de input no final do jogo (para inserir o nome)
                if self.finalScreen:
                    if self.input_rect.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False

            # Eventos de digitação (user types a key)
            if event.type == pygame.KEYDOWN:

                # Coloca o número que o usuário digitou na casa
                if self.selected is not None and list(self.selected) not in self.lockedCells:
                    if self.isInt(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)

                        # Notifica que a casa sofreu uma alteração
                        self.cellChanged = True

                # Lógica para o botão de input no final do jogo (para inserir o nome)
                if self.finalScreen:
                    if self.input_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.input_texto = self.input_texto[:-1]
                        # Caso o usuário digite enter e não escreva um nome vazio
                        elif (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN) and self.input_texto != '':
                            # Esse comando abaixo define a última finalização do jogo
                            self.finishGame(winner=True, write=True)
                        else:
                            self.input_texto += event.unicode

    def update(self):
        # Atualiza a posição do mouse
        self.mousePos = pygame.mouse.get_pos()

        # Lógica de verificar se um botão está pressionado ou não
        for button in self.playingButtons:
            button.update(self.mousePos)

        # Se houve uma alteração de casa
        if self.cellChanged:

            # Reseta as células incorretas
            self.incorrectCells = []

            # Verifica se o tabuleiro está correto
            if self.allCellsDone():
                self.checkAllCells()
                # print(self.incorrectCells)

                if len(self.incorrectCells) == 0:
                    # print('congratulations!')
                    self.finishGame(winner=True)


    def draw(self):

        # Seta a cor a ser preenchida como branca
        self.window.fill(WHITE)

        # Desenha os botões
        for button in self.playingButtons:
            button.draw(self.window)

        # Desenha o timer
        self.drawTimer()

        if not self.rankingMode and not self.finalScreen:
            # Desenha a casa selecionada
            if self.selected:
                self.drawSelection(self.window, self.selected)

            # Desenha a sombra dos números bloqueados (originais do puzzle)
            self.shadeLockedCells(self.window, self.lockedCells)

            # Desenha a sobra dos números incorretos
            self.shadeIncorrectCells(self.window, self.incorrectCells)

            # Desenha os números a partir de uma matriz
            self.drawNumbers(self.window)

            # Desenha a grade (grid) do sudoku enviando o "palco" self.window como parâmetro
            self.drawGrid(self.window)


        elif self.finalScreen:
            ### Texto de parabéns ###

            # Define a fonte para o texto de "Parabéns!!!"
            self.font = pygame.font.SysFont("arial", 70)

            # Renderiza o texto "Parabéns"
            self.textToScreen(self.window, 'PARABÉNS!!!', [280, 150], colour=LIGHTGREEN)
            # Desenha um retângulo vermelho embaixo do timer
            # pygame.draw.rect(self.window, (206, 68, 68), (500, 40, WIDTH // 7, 40))

            # Volta para a fonte padrão
            self.font = pygame.font.SysFont("arial", cellSize // 2)

            ### Texto "Nome: " ###

            # Define a fonte para o texto de "Nome: "
            self.font = pygame.font.SysFont("arial", cellSize // 2)

            # Renderiza o texto "Nome: "
            self.textToScreen(self.window, 'Nome: ', [180, 240], colour=BLACK)

            ### Caixa de input ###

            # Configura a fonte da digitação
            base_font = pygame.font.Font(None, 32)

            # Configura a cor de acordo com o que está ativo
            if self.input_active:
                self.input_color = self.input_color_active
            else:
                self.input_color = self.input_color_passive

            # Desenha o retângulo
            pygame.draw.rect(self.window, self.input_color, self.input_rect, 2)

            # Texto a ser renderizado
            text_surface = base_font.render(self.input_texto, True, BLACK)

            # Atualiza a tela com o texto
            self.window.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

            # Ajusta o tamanho do retângulo dinâmicamente
            self.input_rect.w = max(100, text_surface.get_width() + 10)

            ### Texto "Pontuação: [____] " ###

            # Define a fonte para o texto de "Pontuação: [____]"
            self.font = pygame.font.SysFont("arial", cellSize // 2)

            # Renderiza o texto "Pontuação: [____]"
            self.textToScreen(self.window, f'Tempo p/ fazer: {self.time}s', [260, 280], colour=pygame.Color('purple'))

            ### Texto "(Insira um nome para continuar)" ###

            # Define a fonte para o texto de "(Insira um nome para continuar)"
            self.font = pygame.font.SysFont("arial", cellSize // 3)

            # Renderiza o texto "Pontuação: [____]"
            self.textToScreen(self.window, '(Insira um nome para continuar)', [250, 320])

            # Define a fonte padrão "
            self.font = pygame.font.SysFont("arial", cellSize // 2)

        else:
            # Pinta um quadrado grande com borda preta
            pygame.draw.rect(self.window, WHITE, (gridPos[0], gridPos[1], WIDTH - 150, HEIGHT - 150), 2)

            # Desenha o ranking na tela
            self.drawRanking()

        # Atualiza o display
        pygame.display.update()

        # Modifica para falso depois de desenhar a casa alterada
        self.cellChanged = False


    ##### FUNÇÕES DE CHECAGEM DO TABULEIRO #####
    '''
    Comentário da função mouseOnGrid():
        Confere se o tabuleiro está feito
    '''
    def allCellsDone(self):
        # Se existir alguma célula (ou casa) em branco, retorna False
        # Caso contrário, retorna true
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True

    def checkAllCells(self):

        self.checkRows()
        self.checkCols()
        self.checkSmallGrid()

    def checkSmallGrid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for i in range(3):
                    for j in range(3):
                        xidx = x*3 + i
                        yidx = y*3 + j
                        if self.grid[yidx][xidx] in possibles or self.grid[yidx][xidx] == 0:
                            # Esse try é pq se o valor for zero, ele não vai conseguir ser retirado da lista, dando um Value Error
                            try:
                                possibles.remove(self.grid[yidx][xidx])
                            except ValueError:
                                pass
                        else:
                            if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                                self.incorrectCells.append([xidx, yidx])

                            # Explicação do if abaixo na função similar "checkRows()"
                            if [xidx, yidx] in self.lockedCells:
                                for k in range(3):
                                    for l in range(3):
                                        xidx2 = x * 3 + k
                                        yidx2 = y * 3 + l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2, yidx2] not in self.lockedCells:
                                            self.incorrectCells.append([xidx2, yidx2])

    def checkRows(self):
        # Passa pelo tabuleiro inteiro e adiciona na lista "self.incorrectCells"
        # toda casa que estiver errada segundo às regras de negócio de linha.
        for yidx, row in enumerate(self.grid):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for xidx in range(9):
                if self.grid[yidx][xidx] in possibles or self.grid[yidx][xidx] == 0:
                    # Esse try é pq se o valor for zero, ele não vai conseguir ser retirado da lista, dando um Value Error
                    try:
                        possibles.remove(self.grid[yidx][xidx])
                    except ValueError:
                        pass
                else:
                    if [xidx, yidx] not in self.lockedCells not in self.incorrectCells:
                        self.incorrectCells.append([xidx, yidx])

                    # Se for uma casa do puzzle original (lockedCell), confere novamente, pois mesmo que
                    # uma casa tenha sido dada como possível, por ela estar mais à esquerda, ela pode estar falsa
                    # pois no começo da leitura, só tinha ela. Então o programa lê uma segunda vez para casas
                    # trancadas. Pois as casas trancadas têm prioridade, independente da ordem de leitura. Então
                    # um erro como: >5< 1 2 3 4 5 6 7 8, que indicaria a primeira casa como possível, mesmo sendo
                    # óbvio que a única casa possível aí tenha que ser 9, não irá acontecer com essa "recheckagem"
                    if [xidx, yidx] in self.lockedCells:
                        for k in range(9):
                            # explicação do "and [k, yidx] not in self.lockedCells":
                            #   Caso não tivesse esse "and", o programa ia ler de novo quando a casa fosse exatamente
                            #   a mesma self.lockedCell que está sendo conferida. Ou seja: [7][1] == [7][1]. E é óbvio
                            #   que o valor é igual, pois está se lendo a mesma posição. A única comparação que queremos
                            #   são as diferentes para x, como [7][3] == [7][1]. Caso não existisse esse and, as próprias
                            #   casas trancadas ficariam marcadas.
                            if self.grid[yidx][k] == self.grid[yidx][xidx] and [k, yidx] not in self.lockedCells:
                                self.incorrectCells.append([k, yidx])

    def checkCols(self):
        # Passa pelo tabuleiro inteiro e adiciona na lista "self.incorrectCells"
        # toda casa que estiver errada segundo às regras de negócio de coluna.
        for xidx in range(9):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possibles or self.grid[yidx][xidx] == 0:
                    # Esse try é pq se o valor for zero, ele não vai conseguir ser retirado da lista, dando um Value Error
                    try:
                        possibles.remove(self.grid[yidx][xidx])
                    except ValueError:
                        pass
                else:
                    if [xidx, yidx] not in self.lockedCells not in self.incorrectCells:
                        self.incorrectCells.append([xidx, yidx])
                    # Explicação do if abaixo na função similar "checkRows()"
                    if [xidx, yidx] in self.lockedCells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx, k] not in self.lockedCells:
                                self.incorrectCells.append([xidx, k])


    ##### FUNÇÕES AUXILIARES #####

    def getPuzzle(self, difficulty):
        # A dificuldade é passada como um número de 1-4 (1 = easy, 2 = medium, and so on)

        # Pega o conteúdo de uma request à página html do sudoku
        html_doc = requests.get(f"https://nine.websudoku.com/?level={difficulty}").content
        # Faz esse conteúdo (string de página html) passar por um "embelezamento"
        soup = BeautifulSoup(html_doc)

        # Cria um arrays com ids: [f00, f01, f02, ... f57 f58 f60 f61 ... f87 f88]
        ids = []
        for i in range(9):
            for j in range(9):
                ids.append(f"f{i}{j}")

        # Cria uma lista "data" e a faz filtrar a parte que interessa do html pela lista de ids
        data = []
        for cid in ids:
            data.append(soup.find('input', id=cid))

        # Cria uma matriz 9x9 cheia de 0s
        board = [[0 for x in range(9)] for x in range(9)]

        # Dentro da lógica do html, pega o valor da célula e joga dentro da matriz "board"
        for index, cell in enumerate(data):
            try:
                board[index//9][index%9] = int(cell['value'])
            except:
                pass

        self.grid = board  # Recarrega o tabuleiro
        self.load()  # # Carrega alguns elementos do aplicativo

    def shadeIncorrectCells(self, window, incorrect):
        # Pinta de outra cor as casas a serem bloqueadas
        for cell in incorrect:
            # Pinta um retângulo na posição da casa original do puzzle
            pygame.draw.rect(window, INCORRECTCELLCOLOUR,
                             (cell[0]*cellSize + gridPos[0], cell[1]*cellSize + gridPos[1], cellSize, cellSize))

    def shadeLockedCells(self, window, lockedCells):
        # Pinta de outra cor as casas a serem bloqueadas
        for cell in lockedCells:
            # Pinta um retângulo na posição da casa original do puzzle
            pygame.draw.rect(window, LOCKEDCELLCOLOUR,
                             (cell[0]*cellSize + gridPos[0], cell[1]*cellSize + gridPos[1], cellSize, cellSize))

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
        self.playingButtons.append(Button(20, 40, WIDTH // 7, 40,
                                          function=self.checkAllCells,
                                          colour=(27, 142, 207),
                                          text="Check"))

        self.playingButtons.append(Button(140, 40, WIDTH // 7, 40,
                                          function=self.getPuzzle,
                                          colour=(117, 172, 112),
                                          params="1",
                                          text="New"))

        self.playingButtons.append(Button(WIDTH//2-(WIDTH//7)//2, 40, WIDTH//7, 40,
                                          function=self.solvePuzzle,
                                          colour=(204, 197, 110),
                                          text="Solve"))

        self.playingButtons.append(Button(380, 40, WIDTH//7, 40,
                                          function=self.turnRankingMode,
                                          colour=(199, 129, 48),
                                          text="Ranking"))

    def textToScreen(self, window, text, pos, colour=BLACK):
        # Cria uma imagem com um texto (texto, antialias, cor)
        font = self.font.render(str(text), False, colour)

        # Reajusta a posição para ficar no centro da casa
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth) // 2
        pos[1] += (cellSize - fontHeight) // 2

        # Coloca o objeto font na janela
        window.blit(font, pos)

    def load(self):
        # Limpa os botões para que não fiquem vestígios de botões, carregando vários puzzles de uma
        # vez e causando lentidão desnecessária ao app.
        self.playingButtons = []

        # Carrega os botões de cada estado
        self.loadButtons()

        # Reinicia o jogo
        self.incorrectCells = []
        self.lockedCells = []
        self.finished = False
        self.state = "playing"

        # Reajusta o timer
        self.timerIsOn = True
        self.startTime = time.time()
        self.time = time.time()

        # Carrega as casas que são originais do puzzle
        # yidx = y index, xidx = x index
        for yidx, row in enumerate(self.grid):
            for xidx, number in enumerate(row):
                if number != 0:
                    # lockedCells = array que rastreia as casas a serem bloqueadas
                    self.lockedCells.append([xidx, yidx])

    def isInt(self, string):
        # Informa se &string é um inteiro
        # Tenta passar a string para int, se falhar, retorna False, se não, retorna True
        try:
            int(string)
            return True
        except:
            return False

    '''
    Explicação da turnRankingMode():
        É uma função conectada com um botão, que serve para alterar a variável "drawRanking"
        para que assim, na função playing_draw haja a devida alteração
    '''
    def turnRankingMode(self):
        if self.rankingMode:
            self.rankingMode = False
        else:
            self.rankingMode = True

    def drawRanking(self):
        # Altera a fonte para 1.33x maior, para o título
        self.font = pygame.font.SysFont("arial", cellSize * 2 // 3, bold=1)

        # Imprime o título
        self.textToScreen(self.window, "Ranking", [(WIDTH // 2) - 25, 100], colour=DARKRED)

        # Volta à fonte padrão
        self.font = pygame.font.SysFont("arial", cellSize // 2)

        # Imprime o ranking
        if self.readRanking()[0] != '':
            for index, row in enumerate(self.readRanking()):
                infos = row.split(' ')
                text = f'Top {infos[0]} - {infos[2]} - Tempo: {infos[1]}s'
                self.textToScreen(self.window, text, [(WIDTH // 2) - 25, 160+index*50])

    def readRanking(self):
        f = open('ranking.txt', 'r')
        ranking = f.read()
        f.close()
        return ranking.split('\n')

    def writeRanking(self):
        # Lê o arquivo e guarda cada linha dele em uma string de uma lista
        posicoes = self.readRanking()

        # Adiciona a posição atual do jogador
        posicaoAtual = f'{len(posicoes)+1} {self.time} {self.input_texto.capitalize().strip()}'
        if posicoes[0].strip() == '':  # Se "ranking.txt" estiver vazio
            posicoes[0] = posicaoAtual  # posicoes[0] antes de receber posicao atual contém '' se for o ranking está vazio
        else:  # Caso "ranking.txt" não esteja vazio
            posicoes.append(posicaoAtual)

        # Quebra cada string da lista em outras listas, tornando "posicoes" uma lista de listas
        for i in range(len(posicoes)):
            # split: corta a string no caractere 'espaço' e joga os elementos em uma nova lista
            posicoes[i] = posicoes[i].split(' ')

        posicoesArrumadas = []

        # Organiza as posições em "posicoesArrumadas"
        for i in range(len(posicoes)):
            # Exemplo: ['1', '321', 'Gabriel']
            # n é '321', ou seja, o tempo que foi concluído o sudoku
            n = posicoes[i][1]
            # Se a lista posicoesArrumadas está vazia
            if len(posicoesArrumadas) == 0:
                posicoesArrumadas.append(posicoes[i])
            else:
                # Se o valor cabe no final
                if n > posicoesArrumadas[-1][1]:
                    posicoesArrumadas.append(posicoes[i])

                # Se o valor não cabe no final, ler a lista até caber e inserir na posição q dá
                else:
                    pos = 0
                    while pos < len(posicoesArrumadas):
                        if n <= posicoesArrumadas[pos][1]:
                            posicoesArrumadas.insert(pos, posicoes[i])
                            break
                        pos += 1

        # Arruma posicoesArrumadas para forma de lista de strings, com as devidas alterações já feitas
        for i in range(len(posicoesArrumadas)):
            # Exemplo -> posicoesArrumadas[i] = ['6', '1.02', 'A']
            # Arruma o '6' pra '1'
            posicoesArrumadas[i][0] = f'{i+1}'

            # Cria uma quebra de linha para cada posição
            posicoesArrumadas[i][2] = f'{posicoesArrumadas[i][2]}\n'

            # Cria uma string com as informações da lista
            # Exemplo -> '1 1.02 A'
            posicoesArrumadas[i] = ' '.join(posicoesArrumadas[i])

        # Retira a última posição de posicoesArrumadas caso tenha passado de 5, pra manter sempre 5 no ranking sempre
        if len(posicoesArrumadas) > 5:
            posicoesArrumadas.pop()

        # Tira a quebra de linha da última posição de "posicoesArrumadas"
        posicoesArrumadas[-1] = posicoesArrumadas[-1][0:-1]

        # Escreve no arquivo as novas posições
        f = open('ranking.txt', 'w')
        f.writelines(posicoesArrumadas)
        f.close()

    def solvePuzzle(self):
        for y in range(9):
            for x in range(9):
                if [x, y] not in self.lockedCells:
                    self.grid[y][x] = 0
        resolverSudoku(self.grid)

        self.finishGame(winner=False)

        if self.testes:
            # Manda uma cópia do tabuleiro para a pasta testes/testes_Resolsovedor
            importarTabuleiro(self.grid)  # todo criada para teste
        # print(self.lockedCells)

    def drawTimer(self):
        # Desenha um retângulo vermelho embaixo do timer
        pygame.draw.rect(self.window, (206, 68, 68), (500, 40, WIDTH // 7, 40))

        if self.timerIsOn:
            # Seta a fonte do timer
            self.font = pygame.font.SysFont("comicsans", 70 // 2, bold=1)

            # Ajusta o tempo
            self.time = (time.time() - self.startTime).__round__(2)

            # Coloca o timer
            self.textToScreen(self.window, self.time, [525, 35], colour=DARKRED)

            # Volta à fonte padrão
            self.font = pygame.font.SysFont("arial", cellSize // 2)

    def finishGame(self, winner=True, write=False):
        self.timerIsOn = False
        if winner:
            # Começa a tela de finalização
            self.finalScreen = True
            if write:
                # Escreve no ranking
                self.writeRanking()
                # Sai da tela de finalização
                self.finalScreen = False