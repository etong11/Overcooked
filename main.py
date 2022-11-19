from cmu_112_graphics import *
import cs112_f22_week10_linter
import decimal
import copy

import chef
import ingredient
import box

#Overchefed

#################################################
# Helper functions from 
# https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#RecommendedFunctions
#################################################
def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
#################################################

def appStarted(app):
    app.chef1 = chef.Chef(1, app.width/2, app.height/2, 20)
    app.counterX0, app.counterY0 = app.width/5, app.height/5
    app.counterX1, app.counterY1 = app.width*(4/5), app.height*(4/5)
    app.boxSize = app.width/10
    app.box1X0, app.box1Y0 = app.counterX0-app.width/10, app.counterY0+app.boxSize/3
    app.box1X1, app.box1Y1 = app.counterX0, app.counterY0+2*app.boxSize

    app.box1 = box.Box(ingredient.Ingredient('bread'), app.box1X0, app.box1Y0, app.boxSize)
    app.box2 = box.Box(ingredient.Meat('meat'), app.box1X0, app.box1Y0+app.boxSize, app.boxSize)
    app.box3 = box.Box(ingredient.Veggie('tomato'), app.box1X0, app.box1Y0+2*app.boxSize, app.boxSize)
    app.box4 = box.Box(ingredient.Veggie('lettuce'), app.box1X0, app.box1Y0+3*app.boxSize, app.boxSize)
    app.boxes = [app.box1, app.box2, app.box3, app.box4]

    app.chopBoard = box.Box(None, app.counterX0+app.boxSize, app.counterY1, app.boxSize)
    app.stove = box.Box(None, app.counterX0+app.boxSize, app.counterY0-app.boxSize, app.boxSize)

    app.placedIngred = []
    app.order1 = ingredient.Order()
    app.orderDone = False
    app.orderBox = box.Box(None, app.counterX1, app.width/2, app.boxSize)

    app.time = 0

def keyPressed(app, event):
    if event.key == 'w':
        moveChef(app, 0, -1)
    elif event.key == 'a':
        moveChef(app, -1, 0)
    elif event.key == 's':
        moveChef(app, 0, +1)
    elif event.key == 'd':
        moveChef(app, +1, 0)
    elif event.key == 'Space':
        if app.chef1.holding == None:
        #checks if in range of ingredient boxes
            for box in app.boxes:
                if inRange(app, app.chef1, box):
                    #picks up ingredient if within range of the box
                    app.chef1.holding = copy.copy(box.ingredient)
            pickUp(app)
        else:
            #checks if in range of stove
            if inRange(app, app.chef1, app.stove):
                #cook() only cooks if given chopped meat
                app.chef1.cook()
            elif inRange(app, app.chef1, app.orderBox) and app.chef1.holding == app.order1.order:
                app.orderDone = True
                app.chef1.holding = None
            #checks if in range of counter, if so then drop the item
            elif not (inRange(app, app.chef1, app.boxes[0]) or inRange(app, app.chef1, app.boxes[1])
                or inRange(app, app.chef1, app.boxes[2]) or inRange(app, app.chef1, app.boxes[3])
                or inRange(app, app.chef1, app.chopBoard) or inRange(app, app.chef1, app.orderBox)):
                pickUp(app)
                placeOnCounter(app)
    elif event.key == 'Tab':
        #checks if in range of chopping board
        if inRange(app, app.chef1, app.chopBoard) and (isinstance(app.chef1.holding, ingredient.Veggie)
                or isinstance(app.chef1.holding, ingredient.Meat)):
            app.chef1.chop()
        #dash?

def timerFired(app):
    app.time += 1

def moveChef(app, dx, dy):
    newX, newY = app.chef1.x + dx*5, app.chef1.y + dy*5
    if (app.counterX0 <= (newX - app.chef1.r) and 
        app.counterX1 >= (newX + app.chef1.r) and 
        app.counterY0 <= (newY - app.chef1.r) and
        app.counterY1 >= (newY + app.chef1.r)):
        app.chef1.x, app.chef1.y = newX, newY

#Note: fix so holding a raw/raw on counter will not do anything
#picks up ingredient on table
# if chef is holding another ingredient and the two can be combined, combines them to make a burger
def pickUp(app):
    otherIngred = None
    #change so that if already in burger, ingredient can't be combined
    # if (isinstance(app.chef1.holding, ingredient.Burger) or 
    #     isinstance(app.chef1.holding, ingredient.Ingredient) and not app.chef1.holding.isRaw):
    if ((isinstance(app.chef1.holding, ingredient.Veggie) and app.chef1.holding.isChopped)
            or (isinstance(app.chef1.holding, ingredient.Meat) and app.chef1.holding.isCooked)
            or isinstance(app.chef1.holding, ingredient.Burger)):
        otherIngred = app.chef1.holding
    count = 0
    while count < len(app.placedIngred):
        ingred = app.placedIngred[count]
        if (((ingred[1]+app.boxSize/2 == app.chef1.x-app.chef1.r or 
                ingred[1]-app.boxSize/2 == app.chef1.x+app.chef1.r) and 
                ingred[2]-5 <= app.chef1.y <= ingred[2]+5) or 
                ((ingred[2]+app.boxSize/2 == app.chef1.y-app.chef1.r or
                ingred[2]-app.boxSize/2 == app.chef1.y+app.chef1.r) and
                ingred[1]-5 <= app.chef1.x <= ingred[1]+5)):
            #item is within chef range on left, right, top, or bottom counter (with leniance)
            # not ((not isinstance(app.chef1.holding, ingredient.Burger) and app.chef1.holding.isRaw)
            #         or (isinstance(app.chef1.holding, ingredient.Burger) and ingred[0].isRaw))
            app.placedIngred.pop(count)
            app.chef1.holding = ingred[0]
        else:
            count += 1
    #combines the two ingred/burgers -> burger
    if otherIngred != None:
        if (isinstance(app.chef1.holding, ingredient.Burger) and 
                isinstance(otherIngred, ingredient.Burger)):
            for ingred in otherIngred.ingredients:
                app.chef1.holding.addIngred(ingred)
        elif isinstance(app.chef1.holding, ingredient.Burger):
            app.chef1.holding.addIngred(otherIngred)
        elif isinstance(otherIngred, ingredient.Burger):
            app.chef1.holding = otherIngred.addIngred(app.chef1.holding)
        else: #neither are burgers
            app.chef1.holding = ingredient.Burger({str(app.chef1.holding), str(otherIngred)})

def placeOnCounter(app):
    ingredX, ingredY = 0, 0
    #checks if within counter ranges
    if app.counterX0 == app.chef1.x-app.chef1.r:
        #left
        ingredX, ingredY = app.counterX0-app.boxSize/2, app.chef1.y
    elif app.counterX1 == app.chef1.x+app.chef1.r:
        #right
        ingredX, ingredY = app.counterX1+app.boxSize/2, app.chef1.y
    elif app.counterY0 == app.chef1.y-app.chef1.r:
        #up
        ingredX, ingredY = app.chef1.x, app.counterY0-app.boxSize/2
    elif app.counterY1 == app.chef1.y+app.chef1.r:
        #down
        ingredX, ingredY = app.chef1.x, app.counterY1+app.boxSize/2
    if ingredX != 0 and ingredY != 0:
        # if app.placedIngred == []:
        app.placedIngred.append((app.chef1.holding, ingredX, ingredY))
        app.chef1.holding = None
        # else:
        #     for ingred in app.placedIngred:
        #         if not (ingred[1]-5 <= ingredX <= ingred[1] + 5 and ingred[2]-5 <= ingredY <= ingred[2]+5):
        #             app.placedIngred.append((app.chef1.holding, ingredX, ingredY))
        #             app.chef1.holding = None

def inRange(app, chef, box):
    if ((chef.x-chef.r == box.x1 or chef.x+chef.r == box.x0)
            and box.y0 <= chef.y <= box.y1):
        return True #left and right side of counter
    elif ((chef.y+chef.r == box.y0 or chef.y-chef.r == box.y1) 
        and box.x0 <= chef.x <= box.x1):
        return True #bottom and top of counter
    else:
        return False

def redrawAll(app, canvas):
    #prints order
    if not app.orderDone:
        canvas.create_text(70, 50, text='order: '+str(app.order1))
    #draws counter
    canvas.create_rectangle(app.counterX0, app.counterY0, app.counterX1, app.counterY1)
    canvas.create_rectangle(app.counterX0-app.boxSize, app.counterY0-app.boxSize, 
                app.counterX1+app.boxSize, app.counterY1+app.boxSize)
    #draws interfaces on counter
    canvas.create_rectangle(app.box1.x0, app.box1.y0, app.box1.x1, app.box1.y1)
    canvas.create_text(app.box1.x0+app.boxSize/2, app.box1.y0+app.boxSize/2, text=app.box1.ingredient)
    canvas.create_rectangle(app.box2.x0, app.box2.y0, app.box2.x1, app.box2.y1)
    canvas.create_text(app.box2.x0+app.boxSize/2, app.box2.y0+app.boxSize/2, text=app.box2.ingredient)
    canvas.create_rectangle(app.box3.x0, app.box3.y0, app.box3.x1, app.box3.y1)
    canvas.create_text(app.box3.x0+app.boxSize/2, app.box3.y0+app.boxSize/2, text=app.box3.ingredient)
    canvas.create_rectangle(app.box4.x0, app.box4.y0, app.box4.x1, app.box4.y1)
    canvas.create_text(app.box4.x0+app.boxSize/2, app.box4.y0+app.boxSize/2, text=app.box4.ingredient)
    #draw chopping board
    canvas.create_rectangle(app.chopBoard.x0, app.chopBoard.y0, app.chopBoard.x1, app.chopBoard.y1)
    canvas.create_text(app.chopBoard.x0+app.boxSize/2, app.chopBoard.y0+app.boxSize/2, text='chopping\nboard')
    #draw stove
    canvas.create_rectangle(app.stove.x0, app.stove.y0, app.stove.x1, app.stove.y1)
    canvas.create_text(app.stove.x0+app.boxSize/2, app.stove.y0+app.boxSize/2, text='stove')
    #draw order box
    canvas.create_rectangle(app.orderBox.x0, app.orderBox.y0, app.orderBox.x1, app.orderBox.y1)
    canvas.create_text(app.orderBox.x0+app.boxSize/2, app.orderBox.y0+app.boxSize/2, text='orders')
    #draws chef
    canvas.create_oval(app.chef1.x-app.chef1.r, app.chef1.y-app.chef1.r,
                app.chef1.x+app.chef1.r, app.chef1.y+app.chef1.r)
    #shows what chef is holding
    if app.chef1.holding != None:
        canvas.create_text(app.chef1.x, app.chef1.y, text=app.chef1.holding)
    #shows what is on the counters
    for ingred in app.placedIngred:
        ingredX, ingredY = ingred[1], ingred[2]
        name = ingred[0]
        canvas.create_text(ingredX, ingredY, text=name)
    
runApp(width=800, height=600)