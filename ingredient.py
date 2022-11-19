class Ingredient:
    def __init__(self, type):
        self.type = type #str
    
    def __repr__(self):
        return self.type

class Veggie(Ingredient):
    def __init__(self, type):
        super().__init__(type)
        self.isChopped = False

    def __repr__(self):
        chopped = ''
        if self.isChopped:
            chopped = 'chopped'
        return self.type+'\n'+chopped

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

class Burger:
    def __init__(self, ingredients):
        #ingredients is a set of the ingredient obj in burger
        self.ingredients = ingredients
    
    def __repr__(self):
        name = ''
        for ingred in self.ingredients:
            name += str(ingred)
        return name
    
    def addIngred(self, ingred):
        self.ingredients.add(ingred)

class Order:
    def __init__(self, order):
        self.order = order #type
        pass

class Plate:
    def __init__(self, meal):
        self.meal = meal
