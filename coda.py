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

# Available Moves
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

from random import choice

# Describes a player
class Player:
    hit_points = 3
    name = "Default Player"
    coda = ""
    move = ""
    interrupted = False
    actions = {
                'A' : { 
                  'dmg' : ' attacks and deals 1 damage!',
                  'def' : ' attacks but is rebuffed!',
                  'dtd' : ' attacks and deals and takes damage!',
                  'dts' : ' deals damage as he gets totally stomped!'
                },
                'D' : {
                  'def' : ' blocks... nothing!',
                  'blk' : ' blocks the attack!',
                  'dco' : ' blocks part of the attack!'
                },
                'C' : {
                  'ico' : ' prepares for combo!',
                  'icd' : ' initiates combo and loses his wingman!',
                  'ics' : ' gets totally stomped on as he starts his combo!'
                },
                'O' : {
                  'eco' : ' comes down with a crushing blow!',
                  'ecr' : ' smashes through your defenses!',
                  'fco' : ' can\'t find his combo tag team!',
                  'fcd' : ' takes damage while looking for his fallen teammate!',
                  'fcs' : ' gets totally stomped on as he looks for nothing!'
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

def prnt(p,t):
    print p.name + p.actions[p.move][t]

def conflict(p1, p2):
    if not p1.interrupted:
        if p1.move == "A":
            if p2.move in [ "A", "C", "O" ] or p2.interrupted:
                p2.hit_points -= 1
                if p2.move == "A" and not p2.interrupted:
                    p1.hit_points -= 1
                    prnt(p1,'dtd')
                elif p2.move == "O" and not p2.interrupted:
                    p1.hit_points -= 3
                    prnt(p1,'dts')
                else:
                    prnt(p1,'dmg')
                p2.interrupted = False
            elif p2.move == "D":
                prnt(p1,'def')
                p1.interrupted = True
        elif p1.move == "D":
            if p2.move == "A":
                prnt(p1,'blk')
                p2.interrupted = True
            elif p2.move in [ "D", "C" ]:
                prnt(p1,'def')
            elif p2.move == "O":
                prnt(p1,'dco')
                p1.hit_points -= 2
        elif p1.move == "C":
            if p2.move in [ "D", "C" ]:
                prnt(p1,'ico')
            elif p2.move == "A":
                prnt(p1,'icd')
                p1.hit_points -= 1
            elif p2.move == "O":
                prnt(p1,'ics')
                p1.hit_points -= 3
        elif p1.move == "O":
            if p1.hit_points == 3:
                if p2.move == "C" or p2.interrupted:
                    prnt(p1,'eco')
                    p2.hit_points -= 3
                elif p2.move == "D":
                    prnt(p1,'ecr')
                    p2.hit_points -= 2
            else:
                if p2.move in [ "C", "D" ] or p2.interrupted:
                    prnt(p1,'fco')
                elif p2.move == "A":
                    prnt(p1,'fcd')
                    p1.hit_points -= 1
                elif p2.move == "O" and p2.hit_points == 3:
                    prnt(p1,'fcs')
                    p1.hit_points -= 3
    else:
        print p1.name + " is interrupted!"
        if p2.move == "A" and not p2.interrupted:
            prnt(p2,'dtd')
            p1.hit_points -= 1
        elif p2.move == "O"
            if p2.hit_points == 3:
                prnt(p2,'eco')
                p1.hit_points -= 3
            else
                prnt(p2,'fco')
        elif p2.move == "D":
            prnt(p2,'def')
        elif p2.move == "C":
            prnt(p2,'ico')
        p1.interrupted = False
    

#
# States I want to cover
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

# Compare Moves
def fight(p1, p2, playback = "Normal"):
    print "Ready for %s and %s to fight!" % (p1.name, p2.name)
    print p1.name + ": " + p1.coda
    print p2.name + ": " + p2.coda
    rounds = [0,1,2,3,4]
    for r in rounds:
        print "Round %d.  Fight!" % (r + 1)
        p1.move = p1.coda[r]
        p2.move = p2.coda[r]
        conflict(p1,p2)
        if 0 in [ p1.hit_points, p2.hit_points ]:
            break
    print "All rounds are over."
    print p1.name + "HP: " + str(p1.hit_points)
    print p2.name + "HP: " + str(p2.hit_points)
    if p2.hit_points > p1.hit_points:
        print p2.name + " wins!"
    elif p2.hit_points < p1.hit_points:
        print p1.name + " wins!"
    else:
        print "Game ended in a draw."

if __name__ == "__main__":
    p1 = Player()
    p1.coda = random_coda()
    p1.coda = "AAAAA"
    p1.name = "Player 1"
    p2 = Player()
    p2.coda = random_coda()
    p2.coda = "ADAAA"
    p2.name = "Player 2"
    fight(p1,p2)
