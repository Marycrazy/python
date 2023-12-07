import pygame
from pygame.locals import *

# Inicializando o pygame
pygame.init()

# Configurando a janela do jogo
GAME_LOGIC_SIZE, SCREEN_SIZE = (800, 600), (1280 , 720 ) # A resolução do jogo
game_canvas = pygame.Surface(GAME_LOGIC_SIZE) # superfície onde o jogo será desenhado
screen = pygame.display.set_mode(SCREEN_SIZE) # A tela do usuário


class Timer():
    def __init__(self, counter):
        super().__init__()
        self.counter = counter
        # Cria um objeto de fonte para renderizar o texto
        self.font = pygame.font.SysFont(None, 50)
        # Define o tempo de atraso para o evento do temporizador
        self.time_delay = 1000
        # Cria um evento personalizado de temporizador
        self.timer_event = pygame.USEREVENT+1
        # Define o temporizador para disparar o evento após o tempo de atraso
        pygame.time.set_timer(self.timer_event, self.time_delay)
        self.text = self.font.render(str(self.counter), True, (0, 128, 0))
    
    # Atualiza o contador e recria o texto
    def update(self):
        self.counter -= 1
        self.text = self.font.render(str(self.counter), True, (0, 128, 0))

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
        # Definindo a largura e altura de cada mesa
        largura_mesa = 180
        altura_mesa = 130
        # Desenhando cada mesa na tela
        posicoes = [(self.game_canvas.get_width()- self.game_canvas.get_height()-altura_mesa, Balcao.desenha_passadeira()+20), # Posição da primeira mesa
                (self.game_canvas.get_width() - largura_mesa - altura_mesa, Balcao.desenha_passadeira()+20), # Posição da última mesa
                (self.game_canvas.get_width()- self.game_canvas.get_height()-altura_mesa, self.game_canvas.get_height() - altura_mesa - self.nova_altura-20), # Posição da mesa mais abaixo
                (self.game_canvas.get_width() - largura_mesa - altura_mesa, self.game_canvas.get_height() - altura_mesa - self.nova_altura-20)]# Posição da mesa mais abaixo e mais à direita
        for pos in posicoes:
            # Redimensionando a imagem da mesa para a largura e altura desejadas
            mesa_redimensionada = pygame.transform.scale(mesa_imagem, (largura_mesa, altura_mesa))
            # Desenhando a mesa na tela
            self.game_canvas.blit(mesa_redimensionada, pos)

class Servente():
    def __init__(self):
        super().__init__()
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

class Cliente():
    posicoes_livres = [False, True, True, True]
    def __init__(self, game_canvas,sprite, destino):
        super().__init__()
        # Carregando a imagem do yoshi roxo
        self.original_image = pygame.image.load(sprite)
        self.andando_pe_image = self.original_image.subsurface((77, 11, 56, 112))
        self.parado_pe_image = self.original_image.subsurface((12, 8, 56, 112))
        self.parado_sentado_image = self.original_image.subsurface((8, 138, 56, 112))
        self.andando_esquerda_image = self.original_image.subsurface((111, 138, 56, 112))

        # Aumentando o tamanho da imagem do cliente
        nova_largura = self.original_image.get_width() / 5  # Duplicando a largura
        nova_altura = self.original_image.get_height() / 4   # Duplicando a altura
        self.parado_pe_image = pygame.transform.scale(self.parado_pe_image, (nova_largura, nova_altura))
        self.andando_pe_image = pygame.transform.scale(self.andando_pe_image, (nova_largura, nova_altura))
        self.parado_sentado_image = pygame.transform.scale(self.parado_sentado_image, (nova_largura, nova_altura))
        self.andando_esquerda_image = pygame.transform.scale(self.andando_esquerda_image, (nova_largura, nova_altura))

        # Define a imagem inicial
        self.image = self.andando_pe_image

        # Obtendo o retângulo da imagem
        self.rect = self.image.get_rect()

        # Definindo a posição inicial do retângulo
        self.rect.x = 380
        self.rect.y = 0

        # Definindo a largura do cliente
        self.largura = self.rect.width

        self.destino=destino

        # Definindo se o servente está se movendo
        self.is_moving = True

        self.pos_final = [(300, 200), (400, 400)]
        self.posicao_atual = 0
        self.move_down = True
        self.move_side = False

    def aparicao(self):
        dy = self.destino.centery - self.rect.centery
        if abs(dy) > 2 and self.is_moving:
            print("ESTOU PRESO")
        
            self.image = self.andando_pe_image
            dy /= abs(dy)
            self.rect.y += dy * 5
        else:
            self.is_moving = False
            self.image = self.parado_pe_image
            if not self.is_moving and self.pos_final:
                self.ir_mesa()

    def ir_mesa(self):
        #print(f"Posição atual: ({self.rect.x}, {self.rect.y}), Bottom: {self.rect.bottom}, Right: {self.rect.right}")
        if self.move_down:
            self.rect.move_ip(0, 5)
            if(self.rect.bottom >= 260):
                self.move_down = False
                self.move_side = True
            if not self.posicoes_livres[0] and not self.posicoes_livres[1]:
                self.move_down = True
                self.rect.move_ip(0, 5)
                print("hi")
                if(self.rect.bottom > 500):
                    print("here")
                    self.move_down = False
                    self.move_side = True

        if self.posicoes_livres[0]:
            if self.move_side:
                self.rect.move_ip(5, 0)
                if(self.rect.right > 650):
                    self.image = self.parado_sentado_image
                    self.move_side = False
                    self.posicoes_livres[0] = False

        elif self.posicoes_livres[1]:
            if self.move_side:
                self.rect.move_ip(-5, 0)
                self.image = self.andando_esquerda_image
                if(self.rect.right < 190):
                    self.move_side = False
                    self.posicoes_livres[1] = False
            
            
        #print(f"Nova posição: ({self.rect.x}, {self.rect.y}), Bottom: {self.rect.bottom}, Right: {self.rect.right}")  
        

# Criando uma instância da classe Servente
servente = Servente()
Balcao = Balcao(game_canvas)
timer = Timer(10)
destino1 = pygame.Rect(350, 23, 100, 110)
destino2 = pygame.Rect(360, 23, 100, 110)
Cliente1 = Cliente(game_canvas, 'croxo.png', destino1)
Cliente2 = Cliente(game_canvas, 'cazul.png', destino2)
start_time = pygame.time.get_ticks()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer.timer_event:# Se o evento for o evento do temporizador, incrementa o contador e recria o texto
            timer.update()
        
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
    
    if (pygame.time.get_ticks() - start_time) >= 2000:
        Cliente1.aparicao()
        game_canvas.blit(Cliente1.image, Cliente1.rect)
        if (pygame.time.get_ticks() - start_time) >= 8000:
            Cliente2.aparicao()
            game_canvas.blit(Cliente2.image, Cliente2.rect)

    #desenha o tempo na tela
    game_canvas.blit(timer.text, (750, 50))
    # Redimensiona a superfície de design para a resolução da tela do usuário
    screen.blit(pygame.transform.scale(game_canvas, SCREEN_SIZE), (0, 0))
    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
