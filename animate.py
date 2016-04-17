import pygame
from pygame.locals import *
import sys
import time
import pyganim

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        #self = pygame.transform.scale(self, (640,480))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0, 0]

pygame.init()

# set up the window
window_x = 1024
window_y = 768
windowSurface = pygame.display.set_mode((window_x, window_y), 0, 32)
pygame.display.set_caption('Pyganim Test 1')


# ANIMATION Setup

# Example using separate Images
#navi_combo = pyganim.PygAnimation([('sprites/navi_c1.png', 0.1),
#                                   ('sprites/navi_c2.png', 0.3),
#                                   ('sprites/navi_c3.png', 0.5)])
# This one is using a single gridded image
i = pyganim.getImagesFromSpriteSheet("sprites/full_image/navinew.png", rows = 7, cols = 7, rects = [(0,0,490,490)])
i = [ pygame.transform.scale(x, (window_x/3, window_x/3)) for x in i ]
# Combo Swipe
frames = list(zip(
                 [i[30],i[24],i[17], i[4],i[43],i[36],i[29],i[22],i[15], i[8],i[38],i[31],i[30]], 
                 [ 800,  200,  200,  200,  100,  100,  100,  100,  100,  200,  200,  200, 200]))
navi_combo = pyganim.PygAnimation(frames)
navi_combo.play()


mainClock = pygame.time.Clock()

bg = pygame.image.load("sprites/fight_scene2.jpg").convert()
bg = pygame.transform.scale(bg, (window_x,window_y))

while True:
    #BackGround = Background('sprites/fight_scene1.png')
    #BackGround = pygame.transform.scale(BackGround, (640,480))
    windowSurface.fill([50, 50, 50])
    #windowSurface.blit(BackGround.image, BackGround.rect)
    windowSurface.blit(bg, [0,0])
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_l:
            # press "L" key to stop looping
            navi_combo.loop = False

    navi_combo.blit(windowSurface, (window_x/8, window_y/2))
    #navi_combo.stop()

    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.
