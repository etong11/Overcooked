class Box:
    def __init__(self, ingredient, x0, y0, size):
        self.ingredient = ingredient
        #box is a square
        self.size = size
        self.x0 = x0
        self.x1 = x0+size
        self.y0 = y0
        self.y1 = y0+size
        
    def getIngredient(self):
        return self.ingredient

    def getRange(self):
        return self.x0, self.y0, self.x1, self.y1


# class ChoppingBoard(Box):
#     def __init__(self, ingredient, x0, y0, size):
#         super().__init__(ingredient, x0, y0, size)
#         self.isChopped = False
    
#     def chop(self):
#         self.isChopped = True

# class Stove(Box):
#     def __init__(self, ingredient, x0, y0, size):
#         super().__init__(ingredient, x0, y0, size)
#         self.isCooked = False

#     def cook(self):
#         self.isCooked = True