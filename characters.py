import pyganim
import pygame
from pygame.locals import *

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
        self.mapKeys()

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
        self.mapKeys()

    def buildMoves(self):
        pass

    def setCharDimensions(self):
        pass

    def mapKeys(self):
        if not self.player_two:
            self.keys = {
                K_1         : 'stand'                        ,
                K_2         : 'attack_damage'                ,
                K_3         : 'fight_start'                  ,
                K_4         : 'attack_defended'              ,
                K_q         : 'attack_both_damage'           ,
                K_w         : 'attack_while_comboed'         ,
                K_e         : 'defends'                      ,
                K_r         : 'defends_blocks'               ,
                K_a         : 'defends_while_comboed'        ,
                K_s         : 'combo_initiate'               ,
                K_d         : 'combo_init_and_damaged'       ,
                K_f         : 'combo_init_while_comboed'     ,
                K_z         : 'execute_combo'                ,
                K_x         : 'execute_combo_while_defended' ,
                K_c         : 'failed_combo'                 ,
                K_v         : 'failed_combo_and_damaged'     ,
                K_t         : 'failed_combo_while_comboed'   ,
                K_g         : 'interrupted'                  ,
                K_b         : 'KO'
            }
        else:
            self.keys = {
                K_7         : 'stand'                        ,
                K_8         : 'attack_damage'                ,
                K_9         : 'fight_start'                  ,
                K_0         : 'attack_defended'              ,
                K_u         : 'attack_both_damage'           ,
                K_i         : 'attack_while_comboed'         ,
                K_o         : 'defends'                      ,
                K_p         : 'defends_blocks'               ,
                K_j         : 'defends_while_comboed'        ,
                K_k         : 'combo_initiate'               ,
                K_l         : 'combo_init_and_damaged'       ,
                K_SEMICOLON : 'combo_init_while_comboed'     ,
                K_m         : 'execute_combo'                ,
                K_COMMA     : 'execute_combo_while_defended' ,
                K_PERIOD    : 'failed_combo'                 ,
                K_SLASH     : 'failed_combo_and_damaged'     ,
                K_y         : 'failed_combo_while_comboed'   ,
                K_h         : 'interrupted'                  ,
                K_n         : 'KO'                           
            }

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

        # This is the hard part, unfortunately.
        # This part matches each attack to a sequence of frames and a time for each.
        move_list = {
                'fight_start'                  : zip([  49,   9,  16,  23,  30 ],
                                                     [ 200, 200, 200, 200, 200 ]),
                'stand'                        : zip([  30,  32 ], 
                                                     [ 900, 100 ]),
                'attack_damage'                : zip([  37,  44,   3,  10 ], 
                                                     [ 300, 200, 200, 200 ]),
                'attack_defended'              : zip([  37,  44,   3,  10,   2 ], 
                                                     [ 300, 200, 200, 700, 200 ]),
                'attack_both_damage'           : zip([  37,  44,   3,  10,  23 ], 
                                                     [ 300, 200, 200, 600, 300 ]),
                'attack_while_comboed'         : zip([  49,   9,  16,  23,  30,   2 ],
                                                     [ 200, 200, 200, 200, 200, 300 ]),
                'defends'                      : zip([  24, 45,  4,  5, 12, 19, 12, 19, 12, 19, 12, 19, 12,  5,  4  ],
                                                     [  75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75  ]),
                'defends_blocks'               : zip([  24, 45,  4,  5, 12, 19, 12, 19, 12, 19, 12, 19, 12,  5,  4  ],
                                                     [  75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75  ]),
                'defends_while_comboed'        : zip([  24, 45,  4,  5, 12, 19, 12, 19, 12, 19, 12, 19,   2 ],
                                                     [  75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 250 ]),
                'combo_initiate'               : zip([   31,  38,  45,   4 ],
                                                     [  200, 200, 200, 900 ]),
                'combo_init_and_damaged'       : zip([   31,  38,  45,   4,   2 ],
                                                     [  200, 200, 200, 500, 500 ]),
                'combo_init_while_comboed'     : zip([   31,  38,  45,   4,   2 ],
                                                     [  200, 200, 200, 500, 500 ]),
                'execute_combo'                : zip([   4,   5,  43,  36,  29,  22,  15,   8,  38,  31 ], 
                                                     [  75,  75,  75,  75,  75,  75,  75, 200, 300, 500 ]),
                'execute_combo_while_defended' : zip([   4,   5,  43,  36,  29,  22,  15,   8,  38,  31,   2 ], 
                                                     [  75,  75,  75,  75,  75,  75,  75, 200, 200, 100, 500 ]),
                'failed_combo'                 : zip([   4,   5,   4,   5,   4,  17,   4,  17,  30,  23 ], 
                                                     [  75,  75,  75,  75,  75,  75,  75, 200, 300, 100 ]),
                'failed_combo_and_damaged'     : zip([   4,   5,   4,   5,   4,  17,   4,  17,  30,  23,   2 ], 
                                                     [  75,  75,  75,  75,  75,  75,  75, 200, 300, 100, 500 ]),
                'failed_combo_while_comboed'   : zip([   4,   5,   4,   5,   4,  17,   4,  17,  30,  23,   2 ], 
                                                     [  75,  75,  75,  75,  75,  75,  75, 200, 300, 100, 500 ]),
                'interrupted'                  : zip([  30,  23 ],
                                                     [ 100, 100 ]),
                'KO'                           : zip([  30,  23,  16,   9,  49,   9,  49 ],
                                                     [ 200, 200, 200, 200, 200, 200, 200 ])
                }

        #move_list['interrupted'] = zip([  26,  33,  40,  47,  48 ], 
        #                               [ 500, 500, 500, 500, 500 ])
        for k, v in move_list.iteritems():
            # Here I take that first row and actually make them the image objects
            v = [(i[t[0]],t[1]) for t in list(v)] #wol
            if k in [ "stand", "interrupted" ]:
                self.moves[k] = pyganim.PygAnimation(v)
            else:
                self.moves[k] = pyganim.PygAnimation(v, loop=False)


    def setCharDimensions(self):
        self.width =  70 * self.char_y_fraction
        self.height =  70 * self.char_y_fraction

