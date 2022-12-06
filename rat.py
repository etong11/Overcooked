import random
import decimal
import copy
from cmu_112_graphics import *
from astar import *

class Rat:
    #target is a counter with an ingredient (which is what is the target)
    def __init__(self, app, target):
        self.col, self.row = random.randint(0, PathPlan.cols-1), random.randint(0, PathPlan.rows-1)
        
        self.dead = False
        self.hasFood = False
        
        self.x, self.y = PathPlan.convertToPixels(self.row, self.col)
        self.moveTarget = (-1,-1)
        #Rat images and animation made by friend Amy Xu
        self.image = app.loadImage('rat_rest.png')
        self.isFlipped = False

        self.pathPlanner = PathPlan(app, self.x, self.y, target)
        self.pathPlanner.generatePath(target, self.row, self.col)

        self.image = app.loadImage('rat_rest.png')
        self.animation = []
        self.animationName = ''
        self.animationDict = dict()
        self.counterDict = dict()
        animations = ['up', 'down', 'left', 'right']
        self.facing = ''
        #code for making animations from a sprite sheet modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
        spriteStrip = app.loadImage('rat_animations.png')
        app.hitImage = spriteStrip.crop((16*3, 0, 16*3*2, 16*3))
        for animation in animations:
            isFlipped = False
            sprites = []
            if animation == 'down':
                spriteRange = (3, 5) #top left corner of x coord
            elif animation == 'up':
                spriteRange = (6, 9)
            elif animation in ['left', 'right']:
                spriteRange = (10, 14)
                if animation == 'right':
                    isFlipped = True
                    animation = 'left'
            for i in range(spriteRange[0], spriteRange[1]+1):
                sprite = spriteStrip.crop((16*3*i, 0, 16*3*(i+1), 16*3))
                if isFlipped:
                    sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
                sprites.append(sprite)
            if isFlipped:
                animation = 'right'
            self.animationDict[animation] = sprites
            self.counterDict[animation] = 0

    def setAnimation(self, name):
        self.animation = self.animationDict[name]
        if name != self.animationName:
            self.counterDict[self.animationName] = 0
            self.animationName = name
        else:
            self.counterDict[name] = (1+self.counterDict[name])%len(self.animation)

    def grabFood(self):
        if not self.dead and not self.hasFood:
            self.hasFood = self.pathPlanner.moveToTarget(self)
            if self.facing != '':
                self.setAnimation(self.facing)
