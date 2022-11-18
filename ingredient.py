class Ingredient:
    def __init__(self, type):
        self.type = type

class Veggie(Ingredient):
    def __init__(self, type):
        super().__init__(type)
        self.isChopped = False

class Meat(Ingredient):
    def __init__(self, type):
        super().__init__(type)
        self.isChopped = False
        self.isCooked = False

class Burger:
    def __init__(self, ingredients):
        #ingredients is a list of the ingredient obj in burger
        self.ingredients = ingredients

class Order:
    def __init__(self, order):
        self.order = order #type
        pass

class Plate:
    def __init__(self, meal):
        self.meal = meal
