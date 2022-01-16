import os, pygame, socket, threading, time
from pygame.locals import QUIT
from game import RPSgame
from server import Server
from client import Client

quit = False
role = None

class BG():

    def __init__(self, W, H):
        self.width = W
        self.height = H
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Rock-Paper-Scissors!')

    def background(self):
        self.bg = pygame.image.load('./imgs/Bg.jpg')
        self.screen.blit(self.bg, (0, 0))
        pygame.display.update()

    def scissor(self):
        self.img3 = pygame.image.load('./imgs/Scissors.png')
        self.screen.blit(self.img3, (100, 250))

    def Big_scissor(self):
        self.pon1 = pygame.transform.smoothscale(self.img3,(self.img3.get_width()*2, self.img3.get_height()*2))
        self.screen.blit(self.pon1, (200, 250))

    def null(self):
        self.img3 = pygame.image.load('./imgs/question/null.png')
        self.screen.blit(self.img3, (100, 250))


class Player1:
    def __init__(self):
        threading.Thread.__init__(self)
        self.host = '127.0.0.1'
        self.port = 5000

if __name__ == '__main__': 

    clock = pygame.time.Clock()

    back = BG(1200, 650)
    back.background()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        back.scissor()
        time.sleep(1)
        back.Big_scissor()
        time.sleep(1)
        back.background()

        pygame.display.flip()

        clock.tick(60)