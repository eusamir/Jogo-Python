import pygame
from pygame import mixer
pygame.init()

#musica 
mixer.music.load('background.wav')
mixer.music.play(-1)
#confgs tela
tela_larg = 600
tela_alt = 700
tela = pygame.display.set_mode((tela_larg, tela_alt))
#nome do projeto
pygame.display.set_caption('Projeto Pygame')
# fonte
fonte = pygame.font.SysFont("arial", 30)
#start
start_img=pygame.image.load('menunovo.png')
nova_img=pygame.transform.scale(start_img,(tela_larg,tela_alt))
# definir as cores
background = (0, 0, 0)

# cor dos blocos
block_1 = (255, 255, 255)
block_2 = (175, 175, 175)
block_3 = (100, 100, 100)
# cor da base
base_col = (142, 135, 123)
base_outline = (100, 100, 100)
# cor do texto
texto_cor = (255, 255, 255)
# variaveis do jog - filas, colunas, fps
cols = 7
fils = 7
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0
start_game=False

# gerar texto na tela
def draw_text(text, fonte, texto_cor, x, y):
    img = fonte.render(text, True,texto_cor,background)
    tela.blit(img, (x, y))


class wall:
    def __init__(self):
        self.blocks = []
        self.width = tela_larg // cols
        self.height = 50

    def create_wall(self):
        global strength
        for fil in range(fils):
            block_fil = []

            for col in range(cols):
                # criando o retangulo a partir de x e y
                block_x = col * self.width
                block_y = fil * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # definir força do bloco
                if fil < 2:
                    strength = 3
                elif fil < 4:
                    strength = 2
                elif fil < 6:
                    strength = 1

                block_individual = [rect, strength]
                block_fil.append(block_individual)
            self.blocks.append(block_fil)

    def draw_wall(self):
        global block_col
        for fil in self.blocks:
            for block in fil:
                # definindo cor do bloco baseado na força
                if block[1] == 3:
                    block_col = block_3
                elif block[1] == 2:
                    block_col = block_2
                elif block[1] == 1:
                    block_col = block_1
                pygame.draw.rect(tela, block_col, block[0])
                pygame.draw.rect(tela, background, (block[0]), 2)


class paddle:
    def __init__(self):
        self.reset()

    def move(self):
        # resetar direção do movimento
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < tela_larg:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(tela, base_col, self.rect)
        pygame.draw.rect(tela, base_outline, self.rect, 3)

    def reset(self):
        self.height = 20
        self.width = int(tela_larg / cols)
        self.x = int((tela_larg / 2) - (self.width / 2))
        self.y = tela_alt - (self.height * 2)
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0


class game_ball:
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):

        colisao = 5

        # supondo que a parede foi totalmente destruída
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    block_sound=mixer.Sound('block.wav')
                    block_sound.play()
                    # colisao em cima
                    if abs(self.rect.bottom -
                           item[0].top) < colisao and self.speed_y > 0:
                        self.speed_y *= -1
                    # colisao abaixo
                    if abs(self.rect.top -
                           item[0].bottom) < colisao and self.speed_y < 0:
                        self.speed_y *= -1
                        # colisao a esquerda
                    if abs(self.rect.right -
                           item[0].left) < colisao and self.speed_x > 0:
                        self.speed_x *= -1
                    # colisao a direita
                    if abs(self.rect.left -
                           item[0].right) < colisao and self.speed_x < 0:
                        self.speed_x *= -1
                    # reduzir a força do bloco dps de tocado
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                item_count += 1
            row_count += 1
        # dps de destruir todos os blocos
        if wall_destroyed == 1:
            self.game_over = 1

        # colisão com as paredes
        if self.rect.left < 0 or self.rect.right > tela_larg:
            self.speed_x *= -1

        # colisao com o topo da tela e game over
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > tela_alt:
            self.game_over = -1

        # colisão com a base
        if self.rect.colliderect(player_base):
            # colisão com o topo
            if abs(self.rect.bottom -
                   player_base.rect.top) < colisao and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_base.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(
            tela, base_col,
            (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
            self.ball_rad)
        pygame.draw.circle(
            tela, base_outline,
            (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
            self.ball_rad, 3)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.ball_rad * 2,
                                self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#posição do mouse
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#desenhando menu na tela
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

# criando a wall
wall = wall()
wall.create_wall()

# criando a base
player_base = paddle()

# criando a bola
ball = game_ball(player_base.x + (player_base.width // 2),
                 player_base.y - player_base.height)
#criar start
start_button=Button(tela_larg//5-115,tela_alt//5-141,nova_img,1)
run = True
while run:
    clock.tick(fps)
    if start_game== False:
        if start_button.draw(tela):
            start_game = True
    else:
        tela.fill(background)
        wall.draw_wall()
        player_base.draw()
        ball.draw()

        if live_ball:
            player_base.move()
            game_over = ball.move()
            if game_over != 0:
                live_ball = False

        #instruções ao jogador
        if not live_ball:
            if game_over == 0:
                draw_text("clique para começar", fonte, texto_cor, 160,
                        tela_alt // 2 + 80)
            elif game_over == 1:
                draw_text("PARABÉNS, VOCÊ GANHOU", fonte, texto_cor, 240,
                        tela_alt // 2 + 50)
                draw_text("CLIQUE PARA RECOMEÇAR", fonte, texto_cor, 110,
                        tela_alt // 2 + 100)
            elif game_over == -1:
                draw_text("VOCÊ PERDEU :/", fonte, texto_cor, 180,
                        tela_alt // 2 + 50)
                draw_text("CLIQUE PARA RECOMEÇAR", fonte, texto_cor, 110,
                        tela_alt // 2 + 100)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False
        if evento.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_base.x + (player_base.width // 2),
                       player_base.y - player_base.height)
            player_base.reset()
            wall.create_wall()
    pygame.display.update()

pygame.quit()