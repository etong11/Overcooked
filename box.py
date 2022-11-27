class Box:
    #change so can be a rect?
    #add name argument, default is counter, override if do inheritance
    def __init__(self, ingredient, x0, y0, size):
        self.ingredient = ingredient
        #box is a square
        self.size = size
        self.x0 = x0
        self.x1 = x0+size
        self.y0 = y0
        self.y1 = y0+size
    
    #Given the center coordinates of a chef, returns whether if chef is within box bounds
    def withinBox(self, chef):
        #checks if obj is within box on the left or right
        if (chef.cx-chef.r == self.x1 or chef.cx+chef.r == self.x0) and self.y0 <= chef.cy <= self.y1:
            return True
        #checks if obj is within box on the top or bottom
        elif (chef.cy+chef.r == self.y0 or chef.cy-chef.r == self.y1) and self.x0 <= chef.cx <= self.x1:
            return True
        else:
            return False

    def getIngredient(self):
        return self.ingredient

    def getRange(self):
        return self.x0, self.y0, self.x1, self.y1

#improve OOP with redrawAll, etc.
#implement buttons
#implement speed:
# x += dx
# dx += dxx
# add dx to x when timer fired
#image object class -> pass in img url when making obj

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