import pygame
from pygame.locals import *
import sys
import time
import lib.pyganim as pyganim

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0, 0]

pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Pyganim Test 1')

navi_combo = pyganim.PygAnimation([('sprites/navi_c1.png', 0.1),
                                   ('sprites/navi_c2.png', 0.1),
                                   ('sprites/navi_c3.png', 0.1),
                                   ('sprites/navi_c4.png', 0.1),
                                   ('sprites/navi_c5.png', 0.1),
                                   ('sprites/navi_c6.png', 0.1),
                                   ('sprites/navi_c7.png', 0.1),
                                   ('sprites/navi_c8.png', 0.3),
                                   ('sprites/navi_c1.png', 0.5)])
navi_combo.play()

mainClock = pygame.time.Clock()
while True:
    #background = pygame.image.load("sprites/fight_scene1.png").convert()
    BackGround = Background('sprites/fight_scene1.png')
    windowSurface.fill([50, 50, 50])
    windowSurface.blit(BackGround.image, BackGround.rect)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_l:
            # press "L" key to stop looping
            navi_combo.loop = False

    navi_combo.blit(windowSurface, (100, 300))
    #navi_combo.stop()

    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.
