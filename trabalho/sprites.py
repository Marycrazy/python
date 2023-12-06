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
        self.counter += 1
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
                (self.game_canvas.get_width() / 2 - largura_mesa / 2, self.game_canvas.get_height() / 2), # Posição da mesa do meio
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
        self.is_moving = False
    def aparicao(self):
        # Calcula a diferença na coordenada y entre o centro do sprite e o centro do destino
        dy = self.destino.centery - self.rect.centery
        # Se o sprite não está suficientemente perto do destino (a distância é maior que 2)
        if abs(dy) > 2:  # Usamos abs() para obter o valor absoluto de dy, pois ele pode ser negativo
            # Define que o sprite está se movendo
            self.is_moving = True
            # Muda a imagem do sprite para a imagem de andar
            self.image = self.andando_pe_image

            # Normaliza dy dividindo-o pelo valor absoluto de dy. Isso resulta em um valor de -1 ou 1, indicando a direção do movimento.
            dy /= abs(dy)

            # Move o sprite na direção do destino. O número 5 é a velocidade do movimento.
            self.rect.y += dy * 5
        else:
            # Se o sprite está suficientemente perto do destino, define que o sprite não está se movendo
            self.is_moving = False
            # Muda a imagem do sprite para a imagem de parado
            self.image = self.parado_pe_image


# Criando uma instância da classe Servente
servente = Servente()
Balcao = Balcao(game_canvas)
timer = Timer(0)
destino1 = pygame.Rect(453, 23, 100, 110)
destino2 = pygame.Rect(453, 23, 100, 110)
Cliente1 = Cliente(game_canvas, 'croxo.png', destino1)
Cliente2 = Cliente(game_canvas, 'cazul.png', destino2)

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

    # Desenha o cliente na tela
    if timer.counter >= 2:
        Cliente1.aparicao()
        game_canvas.blit(Cliente1.image, Cliente1.rect)
        if timer.counter >= 4:
            Cliente2.aparicao()
            game_canvas.blit(Cliente2.image, Cliente2.rect)
            if timer.counter >= 6:
                Cliente2.rect.x = Cliente1.rect.x + Cliente1.largura
                game_canvas.blit(Cliente2.image, Cliente2.rect)

    #desenha o tempo na tela
    game_canvas.blit(timer.text, (750, 50))
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
