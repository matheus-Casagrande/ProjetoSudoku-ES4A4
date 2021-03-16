import pygame, sys
from settings import *


class App:
    def __init__(self):
        pygame.init()

        # Configura a janela do jogo
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

        # Seta o estado de 'rodando' ao programa
        self.running = True

    def run(self):

        # Enquanto o programa estiver rodando, executar os métodos:
        while self.running:
            self.events()
            self.update()
            self.draw()

        # Quando sair do while, chama os métodos de saída
        pygame.quit()
        sys.exit()


    def events(self):
        for event in pygame.event.get():

            # Captura o evento de saída do programa
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.window.fill(WHITE)
        pygame.display.update()
