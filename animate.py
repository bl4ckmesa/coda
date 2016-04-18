import pygame
from pygame.locals import *
import sys
import time
import pyganim
from characters import *

# Set up the window
pygame.init()
window_x = 1024
window_y = 768
char_y_fraction = 2.5 # Character height per the screen
windowSurface = pygame.display.set_mode((window_x, window_y), 0, 32)
pygame.display.set_caption('Combo Defends Attack!')
info_pack = [ windowSurface, window_x, window_y, char_y_fraction ]


# ANIMATION Setup

player1 = Navi(info_pack)
player1.action("stand")

player2 = Navi(info_pack)
player2.setPlayerTwo()
player2.action("stand")

mainClock = pygame.time.Clock()

#bg = pygame.image.load("sprites/fight_scene2.jpg").convert()
bg = pygame.image.load("sprites/fight_scene2.jpg")
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
            player1.action_checked = "attack_damage"
            player1.action(player1.action_checked)
        if event.type == KEYDOWN and event.key == K_k:
            player2.action_checked = "attack_damage"
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
