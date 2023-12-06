import pygame
from pygame.locals import *
import math


# Inicializando o pygame
pygame.init()

# Configurando a janela do jogo
GAME_LOGIC_SIZE, SCREEN_SIZE = (800, 600), (1334 , 750 ) # A resolução do jogo
game_canvas = pygame.Surface(GAME_LOGIC_SIZE) # superfície onde o jogo será desenhado
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN) # A tela do usuário

class Balcao():
    def __init__(self, design_surface):
        super().__init__()
        self.game_canvas = design_surface
        imagem = pygame.image.load('balcao.png')
        # Definindo a nova largura e altura
        nova_largura = self.game_canvas.get_width()  # Largura total da janela
        self.nova_altura = (self.game_canvas.get_width()-self.game_canvas.get_height())/4  # Altura específica que você deseja em pixels
        self.imagem_redimensionada = pygame.transform.scale(imagem, (nova_largura, self.nova_altura))# Redimensionando a imagem
        #defenir fundo
        # Definindo o fundo
        self.fundo = pygame.image.load('fundo.png')
        self.fundo_redimensionado = pygame.transform.scale(self.fundo, (self.game_canvas.get_width(), self.game_canvas.get_height()))

    def desenha_passadeira(self):
        altura_passadeira = 110
        largura_passadeira = (self.game_canvas.get_width()-self.game_canvas.get_height()) /2
        x_passadeira = (self.game_canvas.get_width() - largura_passadeira) / 2
        vermelho = (255, 0, 0)
        pygame.draw.rect(self.game_canvas, vermelho, (x_passadeira, 0, largura_passadeira, altura_passadeira))
        return altura_passadeira
    
    def posicao_mesa(self):
        # Carregando a imagem da mesa
        mesa_imagem = pygame.image.load('mesa.png')
        # Definindo o número de mesas que você quer na tela
        numero_mesas = 5
        # Definindo a largura e altura de cada mesa
        largura_mesa = 180
        altura_mesa = 130
        # Criando uma lista de mesas
        mesas = []
        # Desenhando cada mesa na tela
        posicoes = [(self.game_canvas.get_width()- self.game_canvas.get_height()-altura_mesa, Balcao.desenha_passadeira()+20), # Posição da primeira mesa
                (self.game_canvas.get_width() - largura_mesa - altura_mesa, Balcao.desenha_passadeira()+20), # Posição da última mesa
                (self.game_canvas.get_width() / 2 - largura_mesa / 2, self.game_canvas.get_height() / 2), # Posição da mesa do meio
                (self.game_canvas.get_width()- self.game_canvas.get_height()-altura_mesa, self.game_canvas.get_height() - altura_mesa - self.nova_altura-20), # Posição da mesa mais abaixo
                (self.game_canvas.get_width() - largura_mesa - altura_mesa, self.game_canvas.get_height() - altura_mesa - self.nova_altura-20)]# Posição da mesa mais abaixo e mais à direita
        for pos in posicoes:
            # Redimensionando a imagem da mesa para a largura e altura desejadas
            mesa_redimensionada = pygame.transform.scale(mesa_imagem, (largura_mesa, altura_mesa))
            # Desenhando a mesa na tela
            self.game_canvas.blit(mesa_redimensionada, pos)

class Servente(pygame.sprite.Sprite):
    def __init__(self, design_surface):
        super().__init__()
        self.screen = design_surface
        # Carregando a imagem do servente parado
        self.original_image = pygame.image.load('servente.png')
        self.andando_image = self.original_image.subsurface((55, 0, 50, 66))
        self.parado_image = self.original_image.subsurface((0, 0, 54, 73))
        
        # Aumentando o tamanho das imagem yoshi
        nova_largura = self.original_image.get_width() *2 / 4  # Duplicando a largura
        nova_altura = self.original_image.get_height() * 2 / 4  # Duplicando a altura
        self.parado_image = pygame.transform.scale(self.parado_image, (nova_largura, nova_altura))
        self.andando_image = pygame.transform.scale(self.andando_image, (nova_largura, nova_altura))

        # Define a imagem inicial
        self.image = self.parado_image

        # Obtendo o retângulo da imagem
        self.rect = self.image.get_rect()

        # Definindo a posição inicial do retângulo
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP] or pressed_keys[K_DOWN] or pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]:
            self.image=self.andando_image
            if pressed_keys[K_UP] and self.rect.top > 0:
                self.rect.move_ip(0, -5)
            if pressed_keys[K_DOWN] and self.rect.bottom < GAME_LOGIC_SIZE[1]-Balcao.desenha_passadeira()+70:
                self.rect.move_ip(0, 5)

            if pressed_keys[K_LEFT] and self.rect.left > 0:
                self.rect.move_ip(-5, 0)

            if pressed_keys[K_RIGHT] and self.rect.right < GAME_LOGIC_SIZE[0]:
                self.rect.move_ip(5, 0)
                self.image = pygame.transform.flip(self.image, True, False)
                

        else:
            self.image=self.parado_image


# Criando uma instância da classe Servente
servente = Servente(game_canvas)
Balcao = Balcao(game_canvas)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # Atualiza a posição do servente
    servente.update()

    # Limpa a tela
    game_canvas.fill((0, 0, 0))
    # Desenha tudo na superfície de design...
    game_canvas.blit(Balcao.fundo_redimensionado, (0, 0))
    y_position = game_canvas.get_height() - Balcao.nova_altura
    game_canvas.blit(Balcao.imagem_redimensionada, (0, y_position))
    # Desenhando a passadeira na tela
    Balcao.desenha_passadeira()
    # Desenhando as mesas na tela
    Balcao.posicao_mesa()
    # Desenha o servente na tela
    game_canvas.blit(servente.image, servente.rect)
    # Redimensiona a superfície de design para a resolução da tela do usuário
    screen.blit(pygame.transform.scale(game_canvas, SCREEN_SIZE), (0, 0))
    # Atualiza a tela
    pygame.display.flip()

pygame.quit()



"""Na linha screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN), você está passando dois argumentos para a função pygame.display.set_mode().

O primeiro argumento é SCREEN_SIZE, que é uma tupla contendo dois valores: a largura e a altura da tela.

O segundo argumento é pygame.FULLSCREEN, que é uma constante que indica à função para abrir a janela em modo de tela cheia.

Então, embora pareça que você está passando três valores, você está realmente passando dois: uma tupla (que conta como um único argumento) e uma constante.

A função pygame.display.set_mode() pode aceitar um segundo argumento opcional que é usado para definir várias opções de exibição. Neste caso, você está usando para definir a opção de tela cheia."""
