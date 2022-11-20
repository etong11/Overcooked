from cmu_112_graphics import *
import cs112_f22_week10_linter
import decimal
import copy

import chef
import ingredient
import box
import rat

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
    app.sink = box.Box(None, app.width/2, app.counterY0-app.boxSize, app.boxSize)

    app.placedIngred = []
    app.orders = [ingredient.Order()]
    app.orderBox = box.Box(None, app.counterX1, app.width/2, app.boxSize)
     
    plateX, plateY = app.counterX1*(2/3), app.counterY1+app.boxSize/2
    #change to a list, also show on screen how many plates left (if stacked)
    app.plate = ingredient.Plate(None, plateX, plateY)
    app.dirtyPlates = []
    app.time = 0
    app.timerDelay = 1000
    app.paused = False
    app.score = 0

    app.rat = None

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
            if (app.dirtyPlates != [] and inRange(app, app.chef1, app.dirtyPlates[0])):
                app.chef1.holding = app.dirtyPlates[0]
                app.dirtyPlates.pop()
            else:
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
            elif (inRange(app, app.chef1, app.orderBox) and app.chef1.holding == app.orders[0].order
                    and app.chef1.holding.plate != None):
                app.chef1.serve(app.orders[0])
                #check if always valid
                app.score += 1
            elif (inRange(app, app.chef1, app.sink) and isinstance(app.chef1.holding, ingredient.Plate)
                    and not app.chef1.holding.clean):
                app.chef1.holding.clean = True
            #checks if in range of counter, if so then drop the item
            elif not (inRange(app, app.chef1, app.boxes[0]) or inRange(app, app.chef1, app.boxes[1])
                or inRange(app, app.chef1, app.boxes[2]) or inRange(app, app.chef1, app.boxes[3])
                or inRange(app, app.chef1, app.chopBoard) or inRange(app, app.chef1, app.orderBox)):
                if inRange(app, app.chef1, app.plate):
                    app.chef1.holding.plateBurger(app.plate) #must hold burger -> can plate it
                else:
                    pickUp(app)
                    placeOnCounter(app)
    elif event.key == 'Tab':
        #checks if in range of chopping board
        if inRange(app, app.chef1, app.chopBoard) and (isinstance(app.chef1.holding, ingredient.Veggie)
                or isinstance(app.chef1.holding, ingredient.Meat)):
            app.chef1.chop()
        #dash?
    elif event.key == 'Escape':
        app.paused = not app.paused

def timerFired(app):
    if not app.paused:
        app.time += 1
    #prevent indexing error if no orders
    if app.orders != [] and app.orders[0].orderDone:
        plateX, plateY = app.counterX1+app.boxSize/2, app.orderBox.y0-app.boxSize*2
        newDirtyPlate = ingredient.Plate(None, plateX, plateY)
        newDirtyPlate.clean = False
        app.dirtyPlates.append(newDirtyPlate)
        app.orders.pop(0)
    if app.time%10 == 0 and len(app.orders) <= 5: #sets a max of 5 orders at a time
        app.orders.append(ingredient.Order())
    if app.orders != []:
        orderNum = 0
        while orderNum < len(app.orders):
            order = app.orders[orderNum]
            order.countdown()
            if order.orderFailed:
                app.orders.pop(orderNum) #remove order w/o rewarding points
            else:
                orderNum += 1
    if 0 <= app.time%10 <= 2 and app.placedIngred != [] and app.rat == None:
        spawnRat(app)
    if app.rat != None:
        #increase speed
        app.rat.grabFood()
        if app.rat.hasFood:
            app.placedIngred.remove(app.rat.target)
            app.rat = None
        ingredMoved = True
        for ingred in app.placedIngred:
            if ingred == app.rat.target:
                ingredMoved = False
        if ingredMoved:
            app.rat.dead = True
            app.rat = None
    if app.time == 1000:
        app.time = 0

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

#modify to check range of diffrent objects
def inRange(app, chef, box):
    if isinstance(box, ingredient.Plate):
        if ((box.x-box.r <= chef.x <= box.x+box.r and chef.y+chef.r == box.y-app.boxSize/2) or
                box.y-box.r <= chef.y <= box.y+box.r and chef.x+chef.r == box.x-app.boxSize/2):
            return True #add to ranges, right now only accounts for plates at bottom and right counter
        else:
            return False
    if ((chef.x-chef.r == box.x1 or chef.x+chef.r == box.x0)
            and box.y0 <= chef.y <= box.y1):
        return True #left and right side of counter
    elif ((chef.y+chef.r == box.y0 or chef.y-chef.r == box.y1) 
        and box.x0 <= chef.x <= box.x1):
        return True #bottom and top of counter
    else:
        return False

#spawns in a rat with a given target
def spawnRat(app):
    target = app.placedIngred[0] #change so ingred obj has x, y
    targetX, targetY = target[1], target[2]
    app.rat = rat.Rat(app, target, targetX, targetY)

def redrawAll(app, canvas):
    canvas.create_text(50, app.height-50, text=app.time)
    #shows score
    canvas.create_text(app.width-40, 20, text=f'score:{app.score}')
    #prints order
    for order in app.orders:
        if not order.orderDone:
            num = app.orders.index(order) + 1
            canvas.create_text(90*num, 50, text='order: '+str(order))
            canvas.create_text(90*num, 20, text=f'time left:{order.orderTime}')
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
    #draws sink
    canvas.create_rectangle(app.sink.x0, app.sink.y0, app.sink.x1, app.sink.y1)
    canvas.create_text(app.sink.x0+app.boxSize/2, app.sink.y0+app.boxSize/2, text='sink')
    #draws plates
    canvas.create_oval(app.plate.x-app.plate.r, app.plate.y-app.plate.r, app.plate.x+app.plate.r, app.plate.y+app.plate.r)
    canvas.create_text(app.plate.x, app.plate.y, text='clean plates')
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
    #draws dirty plates
    for plate in app.dirtyPlates:
        canvas.create_oval(plate.x-plate.r, plate.y-plate.r, plate.x+plate.r, plate.y+plate.r)
        canvas.create_text(plate.x, plate.y, text='dirty plates')
    #draw rat
    if app.rat != None and not app.rat.dead:
        r = 30
        canvas.create_oval(app.rat.x-r, app.rat.y-r, app.rat.x+r, app.rat.y+r)
        canvas.create_text(app.rat.x, app.rat.y, text=app.rat)
    
runApp(width=800, height=600)