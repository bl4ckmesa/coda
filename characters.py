import pyganim
import pygame

class DefaultPlayer:
    def __init__(self,info_pack):
        # I learned I need this __init__ so that my variables don't get shared between instances of Navi
        # Even the moves I don't want shared so I can reverse the animation but not for both players
        self.windowSurface = info_pack[0]
        self.window_x = info_pack[1]
        self.window_y = info_pack[2]
        self.char_y_fraction = info_pack[3]
        self.width = ""
        self.height = ""
        self.action_checked = ""
        self.player_two = False
        self.moves = {}
        self.buildMoves()
        self.setCharDimensions()

    def action(self,move):
        for m in self.moves.keys():
            self.moves[m].stop()
        self.moves[move].play()

    def blit(self,windowSurface, loc):
        for m in self.moves.keys():
            self.moves[m].blit(self.windowSurface, loc)

    def location(self):
        if self.player_two == False:
            return (self.window_x/8, self.window_y/self.char_y_fraction)
        else:
            return ((self.window_x - self.window_x/4 - self.width), self.window_y/self.char_y_fraction)
        
    def setPlayerTwo(self):
        self.player_two = True
        self.buildMoves()

    def buildMoves(self):
        pass

    def setCharDimensions(self):
        pass

class Navi(DefaultPlayer):
    """ The character Navi and his moves. """

    def buildMoves(self):
        # Pull in the imagesheet
        i = pyganim.getImagesFromSpriteSheet("sprites/full_image/navinew.png", rows = 7, cols = 7, rects = [(0,0,490,490)])
        # Player 2 faces the opposite direction
        if self.player_two:
            i = [ pygame.transform.flip(x, True, False) for x in i ]
        # Resize images to make sense in environment.  All players should be some fraction of height of screen
        i = [ pygame.transform.scale(x, (int(self.window_y/self.char_y_fraction), int(self.window_x/self.char_y_fraction))) for x in i ]

        move_list = {
                'stand'                        : list(zip(
                                                         [i[30],i[30],i[30]], 
                                                         [  100,  100, 100])),
                'attack_damage'                : list(zip(
                                                         [i[24],i[17], i[4],i[43],i[36],i[29],i[22],i[15], i[8],i[38],i[31]], 
                                                         [  100,  100,  100,  100,  100,  100,  100,  100,  200,  300,  500])),
                'attack_defended'              : list(zip([i[30]],[100])),
                'attack_both_damage'           : list(zip([i[30]],[100])),
                'attack_while_comboed'         : list(zip([i[30]],[100])),
                'defends'                      : list(zip([i[30]],[100])),
                'defends_blocks'               : list(zip([i[30]],[100])),
                'defends_while_comboed'        : list(zip([i[30]],[100])),
                'combo_initiate'               : list(zip([i[30]],[100])),
                'combo_init_and_damaged'       : list(zip([i[30]],[100])),
                'combo_init_while_comboed'     : list(zip([i[30]],[100])),
                'execute_combo'                : list(zip([i[30]],[100])),
                'execute_combo_while_defended' : list(zip([i[30]],[100])),
                'failed_combo'                 : list(zip([i[30]],[100])),
                'failed_combo_and_damaged'     : list(zip([i[30]],[100])),
                'failed_combo_while_comboed'   : list(zip([i[30]],[100])),
                'KO'                           : list(zip([i[30]],[100]))
                }
        for k, v in move_list.iteritems():
            if k in [ "stand" ]:
                self.moves[k] = pyganim.PygAnimation(v)
            else:
                self.moves[k] = pyganim.PygAnimation(v, loop=False)


    def setCharDimensions(self):
        self.width =  70 * self.char_y_fraction
        self.height =  70 * self.char_y_fraction

