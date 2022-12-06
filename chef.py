import ingredient
from cmu_112_graphics import *

class Chef:
    def __init__(self, player, cx, cy, radius, app):
        #designate as player 0 or 1
        self.player = player
        self.cx, self.cy = cx, cy
        self.r = radius
        self.holding = None #will hold item, can only hold 1 at a time
        
        #Image credit: chef sprites all made by friend Amy Xu
        self.image = app.loadImage('chef.png')
        self.animation = []
        self.animationName = ''
        self.animationDict = dict()
        self.counterDict = dict()
        animations = ['up', 'down', 'left', 'right', 'chop', 'cook', 'wash']
        #code for making animations from a sprite sheet modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
        for animation in animations:
            isFlipped = False
            isWash = False
            if animation == 'right':
                isFlipped = True
                animation = 'left'
            elif animation == 'wash':
                isWash = True
                animation = 'cook'
            imageName = 'chef_' + animation + '.png'
            spriteStrip = app.loadImage(imageName)
            sprites = []
            spriteLen = spriteStrip.size[0]//(16*3)
            for i in range(spriteLen):
                sprite = spriteStrip.crop((16*3*i, 0, 16*3*(i+1), 16*3))
                if isFlipped:
                    sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
                sprites.append(sprite)
            if isFlipped:
                animation = 'right'
            elif isWash:
                animation = 'wash'
            self.animationDict[animation] = sprites
            self.counterDict[animation] = 0
    
    def move(self, app, dx, dy):
        #moves by 1 pixel which = 3
        newX, newY = self.cx + 8*dx, self.cy + 8*dy
        if (app.counterX0 <= (newX - self.r) and 
            app.counterX1 >= (newX + self.r) and 
            app.counterY0 <= (newY - self.r) and
            app.counterY1 >= (newY + self.r)):
            self.cx, self.cy = newX, newY

    def setAnimation(self, name):
        self.animation = self.animationDict[name]
        if name != self.animationName:
            self.counterDict[self.animationName] = 0
            self.animationName = name
        else:
            self.counterDict[name] = (1+self.counterDict[name])%len(self.animation)

    def chop(self):
        #add time to chopping
        if (isinstance(self.holding, ingredient.Veggie) or isinstance(self.holding, ingredient.Meat)
            and not self.holding.isChopped):
            self.holding.chop()
            self.setAnimation('chop')

    def cook(self):
        #not cooked -> cooking -> cooked
        if (isinstance(self.holding, ingredient.Meat) and self.holding.isChopped 
            and not self.holding.isCooked):
            self.holding.cook()
            self.setAnimation('cook')

    def serve(self, order):
        order.orderDone = True
        plate = self.holding.plate
        self.holding = None
        plate.makeDirty()
        return plate
    
    #add method that adds ingredient to plate (can be on counter or in hand)
    
    def wash(self):
        self.holding.makeClean()
        self.setAnimation('wash')
    
    def discard(self):
        if self.holding != None:
            self.holding = None

    def killRat(self, rat):
        rat.dead = True
    

    #remove from main
    def pickUp(self, item):
        pass #check if holding anything

    def drawChef(self, canvas):
        pass

