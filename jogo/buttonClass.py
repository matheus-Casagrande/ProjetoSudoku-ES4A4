import pygame

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

    def update(self, mouse):

        # Checka se a posição do mouse está colidindo com o retângulo do botão
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        # Se o botão estiver destacado, preenche com a cor destacada, se não, com a cor padrão
        self.image.fill(self.highlightedColour if self.highlighted else self.colour)

        # Atualiza o botão na janela
        window.blit(self.image, self.pos)
