class Box:
    #add name argument, default is counter, override if do inheritance
    def __init__(self, x0, y0, size):
        #box is a square
        self.size = size
        self.x0 = x0
        self.x1 = x0+size
        self.y0 = y0
        self.y1 = y0+size
    
    def __eq__(self, other):
        if (isinstance(other, Box) and self.x0 == other.x0 and self.x1 == other.x1
            and self.y0 == other.y0 and self.y1 == other.y1):
            return True
        else:
            return False
    
    #Given the center coordinates of a chef, returns whether if chef is within box bounds
    def withinBox(self, chef):
        #checks if obj is within box on the left or right
        if (chef.cx-chef.r == self.x1 or chef.cx+chef.r == self.x0) and self.y0 <= chef.cy <= self.y1:
            if chef.animationName in ['left', 'right']: #change if make rest position default
                return True
        #checks if obj is within box on the top or bottom
        elif (chef.cy+chef.r == self.y0 or chef.cy-chef.r == self.y1) and self.x0 <= chef.cx <= self.x1:
            if chef.animationName in ['up', 'down', 'chop', 'cook']:
                return True
        else:
            return False

    def getRange(self):
        return self.x0, self.y0, self.x1, self.y1

class Counter(Box):
    def __init__(self, x0, y0, size, ingredient):
        super().__init__(x0, y0, size)
        self.ingredient = ingredient

    def hasIngredient(self):
        if self.ingredient != None: return True
        else: return False

    def getIngredient(self):
        return self.ingredient
    
    def removeIngredient(self):
        self.ingredient = None

class Appliance(Box):
    def __init__(self, x0, y0, size, action):
        super().__init__(x0, y0, size)
        self.action = action

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