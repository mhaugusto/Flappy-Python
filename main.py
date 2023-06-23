import pygame, os, random

WINDOW_WIDHT = 500
WINDOW_HEIGHT = 800

IMG_WALL = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bambu1.png')))
IMGS_PLAYER = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bolinha1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bolinha2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bolinha3.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bolinha4.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bolinha5.png')))
]
IMG_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMG_MENU = pygame.image.load(os.path.join('imgs', 'menu.png'))
IMG_PAUSE = pygame.image.load(os.path.join('imgs', 'pause.png'))
IMG_RESTART = pygame.image.load(os.path.join('imgs', 'restart.png'))
IMG_RETURN = pygame.image.load(os.path.join('imgs', 'return.png'))
IMG_DEATH = pygame.image.load(os.path.join('imgs', 'death.png'))
IMG_PAUSED = pygame.image.load(os.path.join('imgs', 'pausado.png'))
IMG_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'chao.png')))
IMG_CLOSE = pygame.image.load(os.path.join('imgs', 'close.png'))
IMG_PLAY = pygame.image.load(os.path.join('imgs', 'play.png'))

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 30)


class Player:
    IMGS = IMGS_PLAYER
    # animações da rotação
    ROTACAO_MAXIMA = 0
    VELOCIDADE_ROTACAO = 0
    TEMPO_ANIMACAO = 6

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do jogador vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[3]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*5:
            self.imagem = self.IMGS[4]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*5 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o jogador tiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[2]
            #self.contagem_imagem = self.TEMPO_ANIMACAO

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 175
    VELOCIDADE = 8.5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMG_WALL, True, True)
        self.CANO_BASE = IMG_WALL
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(100, 500)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, bola):
        passaro_mask = bola.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - bola.x, self.pos_topo - round(bola.y))
        distancia_base = (self.x - bola.x, self.pos_base - round(bola.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 8.5
    LARGURA = IMG_FLOOR.get_width()
    IMAGEM = IMG_FLOOR

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, bolas, canos, chao, pontos):

    tela.blit(IMG_BG, (0, 0))
    tela.blit(IMG_PAUSE, (0, 0))
    tela.blit(IMG_RESTART, (0, 50))
    tela.blit(IMG_RETURN, (0, 100))
    for bola in bolas:
         bola.desenhar(tela)
    for cano in canos:
         cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (WINDOW_WIDHT - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    # texto2 = FONTE_PONTOS.render(f"Melhor pontuação: {recorde}", 1, (255, 255, 255))
    # tela.blit(texto2, (WINDOW_WIDHT - 10 - texto2.get_width(), 50))
    pygame.display.update()


def reiniciar_jogo():
    play()


def play():
    bolas = [Player(210, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGHT))
    pontos = 0
    relogio = pygame.time.Clock()
    is_paused = False
    is_alive = True
    rodando = True

    while rodando:
            relogio.tick(30)

            # interação com o usuário
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    quit()

                if evento.type == pygame.KEYDOWN: #Tecla 'ESC' para sair do jogo
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                        pygame.quit()
                        quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE: #Tecla 'SPACE' para pular
                        for bola in bolas:
                            bola.pular()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p: #Tecla 'P' para pausar/resumir o jogo
                         is_paused = not is_paused
                         tela.blit(IMG_PAUSED, (45, 300))
                         pygame.display.update()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r: #Tecla 'R' para reiniciar o jogo
                        reiniciar_jogo()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_m:
                        main()


            if not is_paused:
                # mover as coisas
                for bola in bolas:
                    bola.mover()
                chao.mover()

                adicionar_cano = False
                remover_canos = []
                for cano in canos:
                    for i, bola in enumerate(bolas):
                        if cano.colidir(bola):
                            is_alive = not is_alive
                            if not is_alive:
                                bolas.pop(i)

                        if not cano.passou and bola.x > cano.x:
                            cano.passou = True
                            adicionar_cano = True
                    cano.mover()
                    if cano.x + cano.CANO_TOPO.get_width() < 0:
                        remover_canos.append(cano)

                if adicionar_cano:
                    pontos += 1
                    canos.append(Cano(600))
                for cano in remover_canos:
                    canos.remove(cano)

                for i, bola in enumerate(bolas):
                    if (bola.y + bola.imagem.get_height()) > chao.y or bola.y < 0:
                        is_alive = not is_alive
                        if not is_alive:
                            bolas.pop(i)


                desenhar_tela(tela, bolas, canos, chao, pontos)
            if not is_alive:
                tela.blit(IMG_DEATH, (45, 300))
                pygame.display.update()


            # if pontos > recorde:
            #     recorde = pontos
            #     texto2 = FONTE_PONTOS.render(f"Melhor pontuação: {recorde}", 1, (255, 255, 255))
            #     tela.blit(texto2, (WINDOW_WIDHT - 10 - texto2.get_width(), 50))
            #     pygame.display.update()







def main():
    relogio = pygame.time.Clock()
    while True:
        relogio.tick(1)
        tela = pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGHT))
        tela.blit(IMG_MENU, (0, 0))
        tela.blit(IMG_PLAY, (45, 300))
        tela.blit(IMG_CLOSE, (45, 420))
        pygame.display.update()


        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    play()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()



if __name__ == '__main__':
    main()
