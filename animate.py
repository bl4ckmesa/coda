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
char_y_fraction = 2.5 # Character height per the screen
windowSurface = pygame.display.set_mode((window_x, window_y), 0, 32)
pygame.display.set_caption('Combo Defends Attack!')


# ANIMATION Setup

# Example using separate Images
#navi_combo = pyganim.PygAnimation([('sprites/navi_c1.png', 0.1),
#                                   ('sprites/navi_c2.png', 0.3),
#                                   ('sprites/navi_c3.png', 0.5)])

class Navi:
    """ The character Navi and his moves. """
    width =  70 * char_y_fraction
    height =  70 * char_y_fraction
    def __init__(self):
        # I learned I need this __init__ so that my variables don't get shared between instances of Navi
        # Even the moves I don't want shared so I can reverse the animation but not for both players
        self.action_checked = ""
        self.player_two = False
        self.moves = {}
        self.buildMoves()

    def action(self,move):
        for m in self.moves.keys():
            self.moves[m].stop()
        self.moves[move].play()

    def blit(self,windowSurface, loc):
        for m in self.moves.keys():
            self.moves[m].blit(windowSurface, loc)

    def location(self):
        if self.player_two == False:
            return (window_x/8, window_y/char_y_fraction)
        else:
            return ((window_x - window_x/4 - self.width), window_y/char_y_fraction)

    def buildMoves(self):
        i = pyganim.getImagesFromSpriteSheet("sprites/full_image/navinew.png", rows = 7, cols = 7, rects = [(0,0,490,490)])
        if self.player_two:
            i = [ pygame.transform.flip(x, True, False) for x in i ]
        # Resize images to make sense in environment.  All players should be some fraction of height of screen
        i = [ pygame.transform.scale(x, (int(window_y/char_y_fraction), int(window_x/char_y_fraction))) for x in i ]

        # MOVES

        # Standing
        standing = list(zip(
                         [i[30],i[30],i[30]], 
                         [  100,  100, 100]))
        self.moves["stand"] = pyganim.PygAnimation(standing)
        
        # Combo Swipe
        frames = list(zip(
                         [i[24],i[17], i[4],i[43],i[36],i[29],i[22],i[15], i[8],i[38],i[31]], 
                         [  100,  100,  100,  100,  100,  100,  100,  100,  200,  300,  500]))
        self.moves["combo"] = pyganim.PygAnimation(frames, loop=False)
        

    def setPlayerTwo(self):
        self.player_two = True
        self.buildMoves()

player1 = Navi()
player1.action("stand")

player2 = Navi()
player2.setPlayerTwo()
player2.action("stand")

mainClock = pygame.time.Clock()

bg = pygame.image.load("sprites/fight_scene2.jpg").convert()
bg = pygame.transform.scale(bg, (window_x,window_y))

while True:
    windowSurface.fill([50, 50, 50])
    windowSurface.blit(bg, [0,0])

    # Keycodes (for testing right now)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_l:
            player1.action_checked = "combo"
            player1.action(player1.action_checked)
        if event.type == KEYDOWN and event.key == K_k:
            player2.action_checked = "combo"
            player2.action(player2.action_checked)

    # Player action finished checks
    if player1.action_checked and player1.moves[player1.action_checked].isFinished():
        player1.action("stand")
        player1.action_checked = ""

    if player2.action_checked and player2.moves[player2.action_checked].isFinished():
        player2.action("stand")
        player2.action_checked = ""

    # Push out animations for each object
    player1.blit(windowSurface, player1.location())
    player2.blit(windowSurface, player2.location())

    #pygame.display.update() # for just updating parts of the screen?
    pygame.display.flip() # For updating the whole screen
    mainClock.tick(10) # Feel free to experiment with any FPS setting.
