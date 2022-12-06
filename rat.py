import random
import decimal
import copy
from cmu_112_graphics import *
from astar import *

#################################################
# Helper functions from 
# https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#RecommendedFunctions
#################################################
def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
#################################################

class Rat:
    #change so that x,y are cells
    def __init__(self, app, target):
        self.bounds = [app.counterX0, app.counterY0, app.counterX1, app.counterY1]
        self.rows, self.cols = 8, 13 #change to not include counters (target is cell in front of food)
        self.x, self.y = random.randint(0, self.cols-1), random.randint(0, self.rows-1)
        
        self.dead = False
        self.hasFood = False
        # print('target', self.targetX, self.targetY)
        # print('rat', self.x, self.y)
        
        self.moveTarget = (-1,-1)
        #Rat image credit: from https://www.pixilart.com/draw/big-ear-rat-9b1f2c785eb607a
        self.image = app.loadImage('rat.png')
        self.isFlipped = False
        # self.stop = False
        self.target = target #targets a counter with food on it
        self.targetX, self.targetY = Astar.convertToListCoords(target.x0, target.y0)
        self.start = (self.y, self.x)
        self.end = (self.targetY, self.targetX)
        newPath = Astar(self.target, self.y, self.x)

def grabFood(self):
    self.newPath.moveToTarget(self, self.hasFood)
