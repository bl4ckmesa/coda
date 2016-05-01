#import lib.pyganim as pyganim
import pyganim
import pygame

#for i, rect in enumerate(rects):
#    print "i:", i, "rects", rect
#    assert len(rect) == 4, 'rect at index %s is not a sequence of four ints: (left, top, width, height)' % (i)
#    assert (type(rect[0]), type(rect[1]), type(rect[2]), type(rect[3])) == (int, int, int, int), 'rect '

#rects = [ pygame.image.load("sprites/full_image/navinew.png").get_rect() ]
#for i, rect in enumerate(rects):
#    print "i:", i, "rect:", rect
#    assert len(rect) == 4, 'rect at index %s is not a sequence of four ints: (left, top, width, height)' % (i)
#    assert (type(rect[0]), type(rect[1]), type(rect[2]), type(rect[3])) == (int, int, int, int), 'rect '
#print rects

#images = pyganim.getImagesFromSpriteSheet("sprites/full_image/navinew.png", rects = rects)
images = pyganim.getImagesFromSpriteSheet("sprites/full_image/navinew.png", rects = [(0,0,490,490)])
frames = list(zip(images, [200, 200, 600]))
animObj = pyganim.PygAnimation(frames)
animObj.play()
