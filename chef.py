import ingredient

class Chef:
    def __init__(self, player):
        #designate as player 0 or 1
        self.player = player
        self.holding = None #will hold item, can only hold 1 at a time
    
    def chop(self, ingredient):
        #add time to chopping
        if self.holding != None and (isinstance(ingredient, ingredient.Veggie) or 
                isinstance(ingredient, ingredient.Meat)):
            ingredient.isChopped = True

    def cook(self, meat):
        #not cooked -> cooking -> cooked
        if self.holding != None and isinstance(meat, ingredient.Meat):
            meat.isCooked = True
        #must be chopped first?

    def serve(self, ingredient, plate):
        pass
        #adds ingredient to plate (can be on counter or in hand)
    