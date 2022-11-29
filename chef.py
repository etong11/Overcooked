import ingredient

class Chef:
    def __init__(self, player, cx, cy, radius, app):
        #designate as player 0 or 1
        self.player = player
        self.cx, self.cy = cx, cy
        self.r = radius
        self.holding = None #will hold item, can only hold 1 at a time
        self.image = app.loadImage('chef.png')
    
    def chop(self):
        #add time to chopping
        if (isinstance(self.holding, ingredient.Veggie) or isinstance(self.holding, ingredient.Meat)
            and not self.holding.isChopped):
            self.holding.chop()

    def cook(self):
        #not cooked -> cooking -> cooked
        if (isinstance(self.holding, ingredient.Meat) and self.holding.isChopped 
            and not self.holding.isCooked):
            self.holding.cook()

    def serve(self, order):
        order.orderDone = True
        self.holding = None
    
    #add method that adds ingredient to plate (can be on counter or in hand)
    
    def wash(self, plate):
        if not plate.clean:
            plate.clean = True
    
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

