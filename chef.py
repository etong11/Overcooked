import ingredient

class Chef:
    def __init__(self, player, x, y, radius):
        #designate as player 0 or 1
        self.player = player
        self.x, self.y = x, y
        self.r = radius
        self.holding = None #will hold item, can only hold 1 at a time
    
    def chop(self):
        #add time to chopping
        if (isinstance(self.holding, ingredient.Veggie) or isinstance(self.holding, ingredient.Meat)
            and not self.holding.isChopped):
            self.holding.isChopped = True

    def cook(self):
        #not cooked -> cooking -> cooked
        if (isinstance(self.holding, ingredient.Meat) and self.holding.isChopped 
            and not self.holding.isCooked):
            self.holding.isCooked = True
        #must be chopped first?

    def serve(self, ingredient, plate):
        pass
        #adds ingredient to plate (can be on counter or in hand)
    