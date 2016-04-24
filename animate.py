import pygame
from pygame.locals import *
import sys
import time
import pyganim
from characters import *
from coda import *

# Set up the window
DEBUG = False
#DEBUG = True
manual = False
pygame.init()
window_x = 1024
window_y = 768
char_y_fraction = 2.5 # Character height per the screen
windowSurface = pygame.display.set_mode((window_x, window_y), 0, 32)
pygame.display.set_caption('Combo Defends Attack!')
info_pack = [ windowSurface, window_x, window_y, char_y_fraction ]
projectile = False
mainClock = pygame.time.Clock()
rnd = 0


def playerSetup(p1,p2):
    global player1
    player1 = p1(info_pack)
    player1.action("fight_start")
    player1.action_checked="fight_start"
    global p1proj
    p1proj = p1(info_pack)
    p1proj.buildMoves()
    
    global player2
    player2 = p2(info_pack)
    player2.setPlayerTwo()
    player2.action("fight_start")
    player2.action_checked="fight_start"
    global p2proj
    p2proj = p2(info_pack)
    p2proj.setPlayerTwo()
    p2proj.buildMoves()

# Pick your character type here
p1 = Navi
p2 = Navi
playerSetup(p1,p2)

def reset_round():
    # Reset hit points
    global p1text
    global p2text
    p1text = PlayerText()
    p2text = PlayerText()
    argv = sys.argv
    if len(argv) == 2:
        p1text.coda = argv[1]
        p2text.coda = random_coda()
    elif len(argv) == 3:
        p1text.coda = argv[1]
        p2text.coda = argv[2]
    else:
        p1text.coda = random_coda()
        p2text.coda = random_coda()
    p1text.hit_points = 3
    p2text.hit_points = 3
    p1text.name = "Allen"
    p2text.name = "Dad"
    global log_level
    log_level = "Normal"
    log(" <<< " + p1text.name + ": " + p1text.coda + " | " + p2text.name + ": " + p2text.coda + " >>> \n", log_level)

reset_round()
    
# ANIMATION Setup
#bg = pygame.image.load("sprites/fight_scene2.jpg").convert()
bg = Background(info_pack, sprite = "sprites/background_sf.png")

while True:
    windowSurface.fill([50, 50, 50]) # Get a fresh frame every time
    bg.blit(windowSurface)
    if DEBUG:
        # Debug mode doesn't run the game; it just maps a bunch of keys to player actions for testing the animations.
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_6:
                projectile = True
                p1proj.fire('p1')
            if event.type == KEYDOWN and event.key == K_5:
                projectile = False
                p1proj.fire('stop')
                p1proj.locOffset = 0
            if event.type == KEYDOWN and event.key in player1.keys.keys():
                player1.action_checked = player1.keys[event.key]
                player1.action(player1.action_checked)
                print "Player1, action:", player1.action_checked
            if event.type == KEYDOWN and event.key in player2.keys.keys():
                player2.action_checked = player2.keys[event.key]
                player2.action(player2.action_checked)
                print "Player2, action:", player2.action_checked

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

        # Push out animations for each projectile
        if projectile:
            p1proj.updateProjLoc()
        p1proj.blit(windowSurface,p1proj.location())

    else:
        # Go back to standing
        p1a = player1.moves[player1.action_checked]
        p2a = player2.moves[player2.action_checked]
        if player1.action_checked and p1a.isFinished():
            player1.action_checked = "stand"
            player1.action(player1.action_checked)
        if player2.action_checked and p2a.isFinished():
            player2.action_checked = "stand"
            player2.action(player2.action_checked)

        # Time to go to the next round (animations are finished and manual 'm' is pressed)
        if player1.action_checked and (p1a.isFinished() or p1a.loop == True) and player2.action_checked and (p2a.isFinished() or p2a.loop == True) and manual:
            if p1text.hit_points > 0 and p2text.hit_points > 0 and rnd <= 4:
                log("    -- Round %d --" % (rnd + 1), log_level)
                p1text.move = p1text.coda[rnd]
                p2text.move = p2text.coda[rnd]
                roundResult(p1text,p2text, log_level)
                # Set animations of players on screen
                print "Current moves: p1text:", p1text.current_action, ", p2text:", p2text.current_action
                player1.action_checked = p1text.current_action
                player1.action(player1.action_checked)
                player2.action_checked = p2text.current_action
                player2.action(player2.action_checked)
                rnd += 1
                if p1text.hit_points <= 0 or p2text.hit_points <= 0 or rnd > 4:
                    continue
            if p1text.hit_points <= 0 or p2text.hit_points <= 0 or rnd > 4:
                log("\nAll rounds are over. (P1: %d), (P2: %d)" % (p1text.hit_points, p2text.hit_points), log_level)
                if p1text.hit_points <= 0:
                    log(p1text.name + ", " + p1text.actions['KO'], log_level)
                    player1.action_checked = "KO"
                    player1.action(player1.action_checked)
                if p2text.hit_points <= 0:
                    log(p2text.name + ", " + p2text.actions['KO'], log_level)
                    player2.action_checked = "KO"
                    player2.action(player2.action_checked)
                if p2text.hit_points > 0 and p1text.hit_points <= 0:
                    log(p2text.name + " wins!", log_level)
                    player2.action_checked = "defends"
                    player2.action(player2.action_checked)
                elif p1text.hit_points > 0 and p2text.hit_points <= 0:
                    log(p1text.name + " wins!", log_level)
                    player1.action_checked = "defends"
                    player1.action(player1.action_checked)
                else:
                    log("Game ended in a draw.", log_level)
                #reset_round() # Doesn't quite work anyway ;)
                manual = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_m:
                manual = True
        for obj in (player1, p1proj, player2, p2proj):
            obj.blit(windowSurface,obj.location())

        
    #pygame.display.update() # for just updating parts of the screen?
    pygame.display.flip() # For updating the whole screen
    mainClock.tick(30) # Feel free to experiment with any FPS setting.
