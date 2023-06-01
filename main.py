import pygame
import random

winX = 1280
winY = 1024
fps = 75
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class pelotaP:
    def __init__(self, fichero_imagen):
        self.imagen = pygame.image.load(fichero_imagen).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = winX / 2 - self.ancho / 2
        self.y = winY / 2 - self.alto / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])
        self.score1 = 0
        self.score2 = 0

    def movimiento(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def reiniciar(self):
        self.x = winX / 2 - self.ancho / 2
        self.y = winY / 2 - self.alto / 2
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-5, 5])

    def rebotar(self):
        if self.x <= -self.ancho:
            self.reiniciar()
            self.score2 += 1
        if self.x >= winX:
            self.reiniciar()
            self.score1 += 1
        if self.y <= 0:
            self.dir_y = -self.dir_y
        if self.y + self.alto >= winY:
            self.dir_y = -self.dir_y


class raqueta:
    def __init__(self):
        self.imagen = pygame.image.load("Raqueta.png").convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = 0
        self.y = winY / 2 - self.alto / 2
        self.dir_y = 0

    def movimiento(self):
        self.y = self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= winY:
            self.y = winY - self.alto

    def movimiento_bot(self, pelota):
        if self.y > pelota.y:
            self.dir_y = -3
        elif self.y < pelota.y:
            self.dir_y = 3
        else:
            self.dir_y = 0
        self.y += self.dir_y

    def bit(self, pelota):
        if (
                self.x + self.ancho > pelota.x > self.x
                and pelota.y + pelota.alto > self.y
                and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho

    def bit_bot(self, pelota):
        if (
                pelota.x + self.ancho > self.x
                and pelota.x < self.x + self.ancho
                and pelota.y + pelota.alto > self.y
                and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x - self.ancho


def main():
    pygame.init()
    win = pygame.display.set_mode((winX, winY))
    pygame.display.set_caption("Game Ping Pong")
    pelota = pelotaP("Ball.gif")
    fuente = pygame.font.Font(None, 60)
    raqueta_1 = raqueta()
    raqueta_1.x = 60
    raqueta_2 = raqueta()
    raqueta_2.x = winX - 60 - raqueta_2.ancho

    jugando = True
    while jugando:
        pelota.movimiento()
        pelota.rebotar()
        raqueta_1.movimiento()
        raqueta_2.movimiento_bot(pelota)
        raqueta_1.bit(pelota)
        raqueta_2.bit_bot(pelota)

        win.fill(WHITE)
        win.blit(pelota.imagen, (pelota.x, pelota.y))
        win.blit(raqueta_1.imagen, (raqueta_1.x, raqueta_1.y))
        win.blit(raqueta_2.imagen, (raqueta_2.x, raqueta_2.y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = -5
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = 0
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 0

        text = f"{pelota.score1} : {pelota.score2}"
        letrero = fuente.render(text, False, BLACK)
        win.blit(letrero, (winX / 2 - fuente.size(text)[0] / 2, 50))
        pygame.display.flip()
        pygame.time.Clock().tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()
