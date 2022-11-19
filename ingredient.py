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
        self.onPlate = False
    
    def __repr__(self):
        name = ''
        for ingred in self.ingredients:
            name += str(ingred)
        return name
    
    def __eq__(self, other):
        if isinstance(other, Burger) and self.ingredients == other.ingredients:
            return True
        else:
            return False
    
    def addIngred(self, ingred):
        self.ingredients.add(str(ingred))

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
    
    def __repr__(self):
        descrip = ''
        for ingred in self.order.ingredients:
            descrip += str(ingred)
        return descrip

    def completeOrder(self, target):
        if self.order == target:
            print('true')
            return True
        else:
            print('false')
            return False

class Plate:
    def __init__(self, meal):
        self.meal = meal
