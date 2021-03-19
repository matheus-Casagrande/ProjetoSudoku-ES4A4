import pygame
from settings import *

class Button:

    def __init__(self, x, y, width, height, text=None, colour=(73,73,73),
                 highlightedColour=(189,189,189), function=None, params=None):
        # Seta a imagem do botão
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()  # Seta a lógica do retângulo do botão
        self.rect.topleft = self.pos

        # Seta o estado do botão
        self.highlighted = False

        # Seta os outros parâmetros
        self.text = text
        self.colour = colour
        self.highlightedColour = highlightedColour
        self.function = function
        self.params = params
        self.width = width
        self.height = height

    def update(self, mouse):

        # Checka se a posição do mouse está colidindo com o retângulo do botão
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        # Se o botão estiver destacado, preenche com a cor destacada, se não, com a cor padrão
        self.image.fill(self.highlightedColour if self.highlighted else self.colour)

        # Desenha o texto do botão
        if self.text:
            self.drawText(self.text)

        # Atualiza o botão na janela
        window.blit(self.image, self.pos)

    def click(self):
        if self.params:
            self.function(self.params)
        else:
            self.function()

    def drawText(self, text):
        # Configurando a fonte do botão
        font = pygame.font.SysFont("arial", 20, bold=1)

        # Renderizando o texto do botão pra uma imagem
        text = font.render(text, False, BLACK)

        # Pegando o tamanho da imagem do texto
        width, height = text.get_size()

        x = (self.width-width) // 2
        y = (self.height - height) // 2

        # Atualiza a imagem do botão com o texto
        self.image.blit(text, (x, y))