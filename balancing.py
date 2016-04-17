#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script is for running statistical analysis to make sure the game is balanced
#

from coda import *

res = {
        "CODAA" : { "w" : 4, "l" : 1, "d": 5 },
        "ADADA" : { "w" : 1, "l" : 5, "d": 4 }
      }
res = {}

if __name__ == "__main__":
    for i in xrange(1000):
        p1 = Player()
        p1.coda = random_coda()
        res[p1.coda] = res.get(p1.coda, {"win":0,"lose":0,"draw":0})
        for i in xrange(1000):
            p2 = Player()
            p2.coda = random_coda()
            wld = fight(p1,p2,"quiet")
            res[p1.coda][wld] += 1

    print "CODA	Win	Lose	Draw"
    for coda, r in res.iteritems():
        print "%s	%d	%d	%d" % (coda, r['win'], r['lose'], r['draw'])
