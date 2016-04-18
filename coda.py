#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## CODA ## 
##########
##
##  CODA is a game that lets you pick 5 moves to pit against your opponent, and then see who wins.
##    - All 5 moves are chosen ahead of time, making it more like Rock Paper Scissors than anything
##    - Most moves can be vocalized as a word, making it a potentially possible road trip game
##    - Hilarious combinations of attacks would make this much more enjoyable
## 
##  Ultimately this would look like a street fighter-type game where each move is
##  played out in a "round" fashion.  This script will:
##    - Play out the game in text fashion
##    - Run multiple simulations to help balance the game 
## 

# -- Available Moves --
#    A  - Attack (1 Damage)
#    D  - Defend
#    CO - Combo (3 Damage)
#
# Rules
#    - If an Attack (A) is blocked by Defend (D), the attacking player's next move
#      is 'interrupted'.  Thus the next attack or defense would not work.
#    - The Combo (CO) takes TWO (2) moves to complete, and requires player to have ALL THREE (3) 
#      of their Hit points. (The logic there is you actually have two guys in a tag team, one with 
#      2HP and one with 1HP.  The first attack always KO's your 1HP guy, and the combo attack 
#      cannot work without him.)
#    - The Combo does 3 Damage, which is enough to win the round outright.  If the opposing player 
#      was attacking as well, their 1 damage is still calculated, but it will not break the combo.
#      If they were defending, then the total damage of the Combo is reduced to 2.  It does not, 
#      however, interrupt their next move.
#    - If neither player has caused 3 damage by the end of the round, it is a draw.
#    - If both players simultaneously striked a winning blow, they are Double KO'ed and the round
#      is a draw.
#
# -- States I want to cover --
#   Deal   |   Recv
# DMG  Int | Int  DMG  Desc
#  1       |           Attack, deal damage
#       √  |           Attack but miss/blocked
#  1       |       1   Attack, deal damage and take damage
#  1       |       3   Attack, deal damage and take combo damage
#          |           Defend, no action
#          |  √        Defend against attack (causes interrupt)
#          |       2   Defend against CO (still takes some damage)
#          |           Initiate Combo
#          |       1   Initiate Combo, receive damage
#          |       3   Initiate Combo, receive damage
#  3       |           Execute Combo, deal damage
#  2       |           Execute Combo, deal reduced damage
#          |           Fail Combo
#          |       1   Fail Combo, receive damage
#          |       3   Fail Combo, receive damage
#          |           Final KO Animation
# -- Potentially different attack types (melee, ranged, magic)
#    - Would affect blocking mostly.  Block might be dodge, for example.
# -- All turns should negate the interrupt.  Except for those two.
#

from random import choice
import sys
import time

# Describes a player
class PlayerText:
    hit_points = 3
    name = "Default Player"
    coda = ""
    move = ""
    interrupted = False
    actions = {
                'A' : { 
                  'attack_damage'        : ' attacks and deals 1 damage!',
                  'attack_defended'      : ' attacks but is rebuffed!',
                  'attack_both_damage'   : ' attacks and deals and takes damage!',
                  'attack_while_comboed' : ' deals damage as he gets totally stomped!'
                },
                'D' : {
                  'defends'               : ' blocks... nothing!',
                  'defends_blocks'        : ' blocks the attack!',
                  'defends_while_comboed' : ' blocks part of the attack!'
                },
                'C' : {
                  'combo_initiate'           : ' prepares for combo!',
                  'combo_init_and_damaged'   : ' initiates combo and loses his wingman!',
                  'combo_init_while_comboed' : ' gets totally stomped on as he starts his combo!'
                },
                'O' : {
                  'execute_combo'                : ' comes down with a crushing blow!',
                  'execute_combo_while_defended' : ' smashes through your defenses!',
                  'failed_combo'                 : ' can\'t find his combo tag team!',
                  'failed_combo_and_damaged'     : ' takes damage while looking for his fallen teammate!',
                  'failed_combo_while_comboed'   : ' gets totally stomped on as he looks for nothing!'
                },
                'KO' : 'Your heroes have fallen...'
              }

# Generate a CODA move set
def random_coda():
    moves = [ "A", "D", "CO" ]
    coda = ""
    while len(coda) < 5:
        if len(coda) == 4:
            # 5th move can only be 1 move long
            lastmove = [ x for x in moves if len(x) == 1 ]
            coda += choice(lastmove)
        else:
            coda += choice(moves)
    return coda

def prnt(p,t, log_level = "Normal"):
    log("        " + p.name + p.actions[p.move][t], log_level)

def conflict(p1, p2, log_level = "Normal"):
    if not p1.interrupted:
        if p2.interrupted:
            log("        " + p2.name + " is interrupted!", log_level)
            if p1.move == "A":
                prnt(p1,'attack_damage', log_level)
                p2.hit_points -= 1
            elif p1.move == "D":
                prnt(p1,'defends', log_level)
            elif p1.move == "C":
                prnt(p1,'combo_initiate', log_level)
            elif p1.move == "O":
                if p1.hit_points >= 3:
                    prnt(p1,'execute_combo', log_level)
                    p2.hit_points -= 3
                else:
                    prnt(p1,'failed_combo', log_level)
            p2.interrupted = False
        else:
            if p1.move == "A":
                if p2.move  == "A":
                    prnt(p1,'attack_both_damage', log_level)
                    prnt(p2,'attack_both_damage', log_level)
                    p1.hit_points -= 1
                    p2.hit_points -= 1
                elif p2.move == "D":
                    prnt(p1,'attack_defended', log_level)
                    prnt(p2,'defends_blocks', log_level)
                    p1.interrupted = True
                elif p2.move == "C":
                    prnt(p1,'attack_damage', log_level)
                    prnt(p2,'combo_init_and_damaged', log_level)
                    p2.hit_points -= 1
                elif p2.move == "O":
                    if p2.hit_points >= 3:
                        prnt(p1,'attack_while_comboed', log_level)
                        prnt(p2,'execute_combo', log_level)
                        p1.hit_points -= 3
                        p2.hit_points -= 1
                    else:
                        prnt(p1,'attack_damage', log_level)
                        prnt(p2,'failed_combo_and_damaged', log_level)
                        p2.hit_points -= 1
            elif p1.move == "D":
                if p2.move == "A":
                    prnt(p1,'defends_blocks', log_level)
                    prnt(p2,'attack_defended', log_level)
                    p2.interrupted = True
                elif p2.move  == "D":
                    prnt(p1,'defends', log_level)
                    prnt(p2,'defends', log_level)
                elif p2.move == "C":
                    prnt(p1,'defends', log_level)
                    prnt(p2,'combo_initiate', log_level)
                elif p2.move == "O":
                    if p2.hit_points >= 3:
                        prnt(p1,'defends_while_comboed', log_level)
                        prnt(p2,'execute_combo_while_defended', log_level)
                        p1.hit_points -= 2
                    else:
                        prnt(p1,'defends', log_level)
                        prnt(p2,'failed_combo', log_level)
            elif p1.move == "C":
                if p2.move == "A":
                    prnt(p1,'combo_init_and_damaged', log_level)
                    prnt(p2,'attack_damage', log_level)
                    p1.hit_points -= 1
                elif p2.move == "D":
                    prnt(p1,'combo_initiate', log_level)
                    prnt(p2,'defends', log_level)
                elif p2.move == "C":
                    prnt(p1,'combo_initiate', log_level)
                    prnt(p2,'combo_initiate', log_level)
                elif p2.move == "O":
                    if p2.hit_points >= 3:
                        prnt(p1,'combo_init_while_comboed', log_level)
                        prnt(p2,'execute_combo', log_level)
                        p1.hit_points -= 3
                    else:
                        prnt(p1,'combo_initiate', log_level)
                        prnt(p2,'failed_combo', log_level)
            elif p1.move == "O":
                if p1.hit_points == 3:
                    if not p2.interrupted:
                        if p2.move == "A":
                            prnt(p1,'execute_combo', log_level)
                            prnt(p2,'attack_while_comboed', log_level)
                            p2.hit_points -= 3
                            p1.hit_points -= 1
                        elif p2.move == "D":
                            prnt(p1,'execute_combo_while_defended', log_level)
                            prnt(p2,'defends_while_comboed', log_level)
                            p2.hit_points -= 2
                        elif p2.move == "C":
                            prnt(p1,'execute_combo', log_level)
                            prnt(p2,'combo_init_while_comboed', log_level)
                            p2.hit_points -= 3
                        elif p2.move == "O":
                            if p1.hit_points >= 3 and p2.hit_points >= 3:
                                prnt(p1,'execute_combo', log_level)
                                prnt(p2,'execute_combo', log_level)
                                p2.hit_points -= 3
                                p1.hit_points -= 3
                            elif p1.hit_points >= 3 and p2.hit_points < 3:
                                prnt(p1,'execute_combo', log_level)
                                prnt(p2,'failed_combo_while_comboed', log_level)
                                p2.hit_points -= 3
                            elif p1.hit_points < 3 and p2.hit_points >= 3:
                                prnt(p1,'failed_combo_while_comboed', log_level)
                                prnt(p2,'execute_combo', log_level)
                                p1.hit_points -= 3
                    else:
                        log("        " + p2.name + " is interrupted!", log_level)
                        prnt(p1,'execute_combo', log_level)
                        p2.hit_points -= 3
                        p2.interrupted = False
                else:
                    if not p2.interrupted:
                        if p2.move == "A":
                            prnt(p1,'failed_combo_and_damaged', log_level)
                            p1.hit_points -= 1
                        elif p2.move == "D":
                            prnt(p1,'failed_combo', log_level)
                            prnt(p2,'defends', log_level)
                        elif p2.move == "C":
                            prnt(p1,'failed_combo', log_level)
                            prnt(p2,'combo_initiate', log_level)
                        elif p2.move == "O":
                            if p2.hit_points >= 3:
                                prnt(p1,'failed_combo_while_comboed', log_level)
                                prnt(p2,'execute_combo', log_level)
                                p1.hit_points -= 3
                            else:
                                prnt(p1,'failed_combo', log_level)
                                prnt(p2,'failed_combo', log_level)
    else:
        log("        " + p1.name + " is interrupted!", log_level)
        if p2.interrupted:
            log("        " + p2.name + " is interrupted!", log_level)
            p2.interrupted = False
        else:
            if p2.move == "A":
                prnt(p2,'attack_damage', log_level)
                p1.hit_points -= 1
            elif p2.move == "D":
                prnt(p2,'defends', log_level)
            elif p2.move == "C":
                prnt(p2,'combo_initiate', log_level)
            elif p2.move == "O":
                if p2.hit_points == 3:
                    prnt(p2,'execute_combo', log_level)
                    p1.hit_points -= 3
                else:
                    prnt(p2,'failed_combo', log_level)
        p1.interrupted = False

def log(msg, log_level = "Normal"):
    if log_level.lower() == "normal":
        print msg
        time.sleep(0.5)
    elif log_level.lower() == "fast":
        print msg
    elif log_level.lower() == "quiet":
        pass
    
# Compare Moves
def fight(p1, p2, log_level = "Normal"):
    # Reset hit points
    p1.hit_points = 3
    p2.hit_points = 3
    log(" <<< " + p1.name + ": " + p1.coda + " | " + p2.name + ": " + p2.coda + " >>> \n", log_level)
    rounds = [0,1,2,3,4]
    for r in rounds:
        log("    -- Round %d --" % (r + 1), log_level)
        p1.move = p1.coda[r]
        p2.move = p2.coda[r]
        conflict(p1,p2, log_level)
        if p1.hit_points <= 0 or p2.hit_points <= 0:
            break
    log("\nAll rounds are over. (P1: %d), (P2: %d)" % (p1.hit_points, p2.hit_points), log_level)
    if p1.hit_points <= 0:
        log(p1.name + ", " + p1.actions['KO'], log_level)
    if p2.hit_points <= 0:
        log(p2.name + ", " + p2.actions['KO'], log_level)
    if p2.hit_points > 0 and p1.hit_points == 0:
        log(p2.name + " wins!", log_level)
        return "lose"
    elif p1.hit_points > 0 and p2.hit_points == 0:
        log(p1.name + " wins!", log_level)
        return "win"
    else:
        log("Game ended in a draw.", log_level)
        return "draw"

if __name__ == "__main__":
    p1 = PlayerText()
    p2 = PlayerText()
    p1.name = "Allen"
    p2.name = "Dad"
    argv = sys.argv
    if len(argv) == 2:
        p1.coda = argv[1]
        p2.coda = random_coda()
    elif len(argv) == 3:
        p1.coda = argv[1]
        p2.coda = argv[2]
    else:
        p1.coda = random_coda()
        p2.coda = random_coda()
    fight(p1,p2)
