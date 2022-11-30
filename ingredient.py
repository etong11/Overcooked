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
    
    def __repr__(self):
        return self.type

    def __eq__(self, other):
        if isinstance(other, Ingredient) and self.type == other.type:
            return True
        else:
            return False
    
    # def drawIngredient(self, app, canvas):
    #     image = app.loadImage(self.image)
    #     canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef))

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
            chopped = 'chopped'
        return self.type+'\n'+chopped

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
            chopped = 'chopped'
        if self.isCooked:
            cooked = 'cooked'
        return self.type+'\n'+chopped+cooked
    
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
        # print('unsorted', self.ingredients)
        self.ingredients.sort(key=lambda x: x.type)
        # print('sorted', self.ingredients)
        self.plate = None
        self.image = app.loadImage('burger.png')
    
    def __repr__(self):
        name = ''
        for ingred in self.ingredients:
            name += str(ingred)
        if self.plate != None:
            name += str(self.plate)
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
    
    def plateBurger(self, plate):
        self.plate = plate # plate object

class Order:
    def __init__(self, app):
        #add randomized order later
        #add bread (currently doesn't work)
        tomato, lettuce, meat, bread = Veggie('tomato', app), Veggie('lettuce', app), Meat('meat', app), Ingredient('bread', app)
        tomato.isChopped = True
        lettuce.isChopped = True
        meat.isChopped = True
        meat.isCooked = True
        #look into making classes immutable -> error: can't put mutable obj in set
        ingredients = [tomato, lettuce]
        self.order = Burger(ingredients, app) #burger with specific ingredients
        self.orderDone = False
        self.totalTime = 50
        self.orderTime = self.totalTime #modify based on recipe difficulty
        self.orderFailed = False

        #randomized order:
        choices = [tomato, lettuce, (tomato, lettuce)]
        item = random.choice(choices)
        if isinstance(item, tuple):
            self.order = Burger([bread, meat]+list(item), app)
            self.image = app.loadImage('order3.png')
        else:
            self.order = Burger([bread, meat, item], app)
            if item.type == 'tomato':
                self.image = app.loadImage('order2.png')
            else:
                self.image = app.loadImage('order1.png')

    def __repr__(self):
        descrip = ''
        for ingred in self.order.ingredients:
            descrip += str(ingred)
        return descrip

    def completeOrder(self, target): #target is a burger obj
        if self.order == target and target.plate != None:
            return True
        else:
            return False
    
    def countdown(self):
        if self.orderTime > 0:
            self.orderTime -= 1
        else:
            self.orderFailed = True

class Plate:
    def __init__(self, meal, app):
        self.meal = meal
        self.clean = True
        self.image = app.loadImage('plate.png')
    
    def __repr__(self):
        descrip = ''
        if self.clean:
            descrip += 'clean'
        else:
            descrip += 'dirty'
        descrip += 'plate'
        return descrip

    def plate(self, burger):
        burger.plateBurger(self)
        self.meal = burger
