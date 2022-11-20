import random

class Ingredient:
    def __init__(self, type):
        self.type = type #str
        self.isRaw = True
    
    def __repr__(self):
        return self.type

    def __eq__(self, other):
        if isinstance(other, Ingredient) and self.type == other.type:
            return True
        else:
            return False

class Veggie(Ingredient):
    def __init__(self, type):
        super().__init__(type)
        self.isChopped = False

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

class Meat(Ingredient):
    def __init__(self, type):
        super().__init__(type)
        self.isChopped = False
        self.isCooked = False
    
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

class Burger:
    def __init__(self, ingredients):
        #ingredients is a set of the ingredient obj in burger
        self.ingredients = ingredients
        self.plate = None
    
    def __repr__(self):
        name = ''
        for ingred in self.ingredients:
            name += str(ingred)
        if self.plate != None:
            name += str(self.plate)
        return name
    
    def __eq__(self, other):
        if isinstance(other, Burger) and self.ingredients == other.ingredients:
            return True
        else:
            return False
    
    def addIngred(self, ingred):
        self.ingredients.add(str(ingred))
    
    def plateBurger(self, plate):
        self.plate = plate # plate object

class Order:
    def __init__(self):
        #add randomized order later
        #add bread (currently doesn't work)
        tomato, lettuce, meat = Veggie('tomato'), Veggie('lettuce'), Meat('meat')
        tomato.isChopped = True
        lettuce.isChopped = True
        meat.isChopped = True
        meat.isCooked = True
        #look into making classes immutable -> error: can't put mutable obj in set
        ingredients = {str(lettuce), str(tomato)}
        self.order = Burger(ingredients) #burger with specific ingredients
        self.orderDone = False
    
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

class Plate:
    def __init__(self, meal, x, y):
        self.meal = meal
        self.clean = True
        self.r = 20
        self.x, self.y = x, y #center coords
    
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
