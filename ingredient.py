import random
from cmu_112_graphics import *

class Ingredient:
    def __init__(self, type, app):
        self.type = type #str
        if type == 'bread':
            self.isRaw = False
            self.image = app.loadImage('bread.png')
        else:
            self.isRaw = True
        self.box = None #if on box, this = to box obj
        self.plate = None
    
    def __repr__(self):
        # descrip = 
        # if self.plate != None:
        #     descrip += str(self.plate)
        return self.type.capitalize()

    def __eq__(self, other):
        if isinstance(other, Ingredient) and self.type == other.type:
            return True
        else:
            return False

class Veggie(Ingredient):
    def __init__(self, type, app):
        super().__init__(type, app)
        self.isChopped = False
        self.app = app
        if type == 'tomato':
            self.image = app.loadImage('tomato.png')
        elif type == 'lettuce':
            self.image = app.loadImage('lettuce.png')

    def __repr__(self):
        chopped = ''
        if self.isChopped:
            chopped = '(chopped)'
        return self.type.capitalize()+' '+chopped

    def __eq__(self, other):
        if (isinstance(other, Veggie) and self.type == other.type 
                and self.isChopped == other.isChopped):
            return True
        else:
            return False
    
    #chef also has chop method
    def chop(self):
        self.isChopped = True
        self.isRaw = False
        if self.type == 'lettuce':
            self.image = self.app.loadImage('chopped_lettuce.png')
        elif self.type == 'tomato':
            self.image = self.app.loadImage('chopped_tomato.png')

#inherit from Veggie
class Meat(Ingredient):
    def __init__(self, type, app):
        super().__init__(type, app)
        self.isChopped = False
        self.isCooked = False
        self.app = app
        self.image = app.loadImage('meat.png')
    
    def __repr__(self):
        chopped = ''
        cooked = ''
        if self.isChopped:
            chopped = '(chopped)'
        if self.isCooked:
            cooked = '(cooked)'
        return self.type.capitalize()+' '+chopped+cooked
    
    def __eq__(self, other):
        #possibly just str(self) == str(other) ???
        if (isinstance(other, Meat) and self.type == other.type
                and self.isChopped == other.isChopped
                and self.isCooked == other.isCooked):
            return True
        else:
            return False

    #chef also has chop method, copy of veggie method
    def chop(self):
        self.isChopped = True
        self.image = self.app.loadImage('chopped_meat.png')
    
    #chef also has chop method
    def cook(self):
        self.isCooked = True
        self.isRaw = False
        self.image = self.app.loadImage('cooked_meat.png')

class Burger:
    def __init__(self, ingredients, app):
        #ingredients is a set of the ingredient obj in burger
        self.ingredients = ingredients
        #sort code taken from https://www.techiedelight.com/sort-list-of-objects-python/
        self.ingredients.sort(key=lambda x: x.type)
        self.plate = None
        self.image = app.loadImage('burger.png')
    
    def __repr__(self):
        name = ''
        for ingred in self.ingredients:
            name += str(ingred) + ', '
        if name.endswith(', '):
            name = name[:len(name)-2]
        return name
    
    def __eq__(self, other):
        if isinstance(other, Burger) and self.ingredients == other.ingredients:
            print('self', self.ingredients)
            print('other', other.ingredients)
            return True
        else:
            return False
    
    def addIngred(self, ingred):
        if isinstance(ingred, Burger):
            for item in ingred.ingredients:
                self.ingredients.append(item)
        else: #is not a Burger
            self.ingredients.append(ingred)
        #sort code taken from https://www.techiedelight.com/sort-list-of-objects-python/
        self.ingredients.sort(key=lambda x: x.type)

class Order:
    def __init__(self, app):
        tomato, lettuce, meat, bread = Veggie('tomato', app), Veggie('lettuce', app), Meat('meat', app), Ingredient('bread', app)
        tomato.isChopped = True
        lettuce.isChopped = True
        meat.isChopped = True
        meat.isCooked = True
        ingredients = [tomato, lettuce]
        self.order = Burger(ingredients, app) #burger with specific ingredients
        self.orderDone = False
        self.orderFailed = False
        self.orderDoubled = False

        #randomized order:
        choices = [tomato, lettuce, (tomato, lettuce)]
        item = random.choice(choices)
        if isinstance(item, tuple):
            self.order = Burger([bread, meat]+list(item), app)
            self.image = app.loadImage('order3.png')
            self.orderDoubled = True
            self.totalTime = 60
        else:
            self.totalTime = 50
            self.order = Burger([bread, meat, item], app)
            if item.type == 'tomato':
                self.image = app.loadImage('order2.png')
            else:
                self.image = app.loadImage('order1.png')
        self.orderTime = self.totalTime


    def __repr__(self):
        descrip = ''
        for ingred in self.order.ingredients:
            descrip += str(ingred) + ' '
        return descrip

    def completeOrder(self, target): #target is a burger obj
        if self.order == target:
            return True
        else:
            return False
    
    def countdown(self):
        if self.orderTime > 0:
            self.orderTime -= 1
        else:
            self.orderFailed = True

class Plate:
    def __init__(self, app):
        self.isDirty = False
        self.app = app
        self.image = self.app.loadImage('clean_plate.png')
        self.counter = None

    def __repr__(self):
        descrip = 'Plate'
        if self.isDirty:
            descrip += '(dirty)'
        else:
            descrip += '(clean)'
        return descrip

    def makeDirty(self):
        self.isDirty = True
        self.image = self.app.loadImage('dirty_plate.png')
    
    def makeClean(self):
        self.isDirty = False
        self.image = self.app.loadImage('clean_plate.png')
