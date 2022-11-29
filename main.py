from cmu_112_graphics import *
import cs112_f22_week10_linter
import decimal
import copy

from ingredient import *
from chef import *
from box import *
from rat import *

#Overchefed
#images drawn by me (except chef image - credit to Amy Xu)

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
    #images
    app.background = app.loadImage('background.png')
    # app.background = app.scaleImage(app.background, 3)
    print(app.background.size)
    app.chef = app.loadImage('chef.png')
    print(app.chef.size)

    #note: each box is 16x16 pixels (*3 because image expanded to 300%)
    app.chef1 = Chef(1, app.width/2, app.height/2, 24, app)
    app.counterX0, app.counterY0 = 16*2*3, 16*5*3
    app.counterX1, app.counterY1 = app.width-16*2*3, app.height-16*2*3
    app.boxSize = 16*3

    app.box1 = Counter(16*3, 16*5*3, app.boxSize, Veggie('tomato', app))
    app.box2 = Counter(16*3, 16*6*3, app.boxSize, Meat('meat', app))
    app.box3 = Counter(16*3, 16*7*3, app.boxSize, Ingredient('bread', app))
    app.box4 = Counter(16*3, 16*8*3, app.boxSize, Veggie('lettuce', app))
    app.boxes = [app.box1, app.box2, app.box3, app.box4]

    #include duplicates in range check
    app.chopBoard = Appliance(16*3*3, app.height-16*2*3, app.boxSize, app.chef1.chop)
    app.chopBoard2 = Appliance(16*5*3, app.height-16*2*3, app.boxSize, app.chef1.chop)
    app.chopBoards = [app.chopBoard, app.chopBoard2]
    app.stove = Appliance(app.width-16*3*3, 16*4*3, app.boxSize, app.chef1.cook)
    app.stove2 = Appliance(app.width-16*4*3, 16*4*3, app.boxSize, app.chef1.cook)
    app.stove3 = Appliance(app.width-16*5*3, 16*4*3, app.boxSize, app.chef1.cook)
    app.stove4 = Appliance(app.width-16*6*3, 16*4*3, app.boxSize, app.chef1.cook)
    app.stoves = [app.stove, app.stove2, app.stove3, app.stove4]
    app.sink = Appliance(16*3*3, 16*4*3, app.boxSize, app.chef1.wash)
    app.trash = Appliance(16*3, 16*10*3, app.boxSize, app.chef1.discard)

    app.placedIngred = []
    app.usedCounters = []
    app.orders = [Order(app)]
    app.orderBox = Appliance(app.width-16*2*3, 16*7*3, app.boxSize, app.chef1.serve)
    app.orderBox2 = Appliance(app.width-16*2*3, 16*8*3, app.boxSize, app.chef1.serve)

    #makes orders identicals - fix
    # app.order = app.loadImage(app.orders[0].image)
    # print(app.order.size)

    app.specialBoxes = app.chopBoards + app.stoves + app.boxes + [app.sink, app.trash, app.orderBox, app.orderBox2]
    # plateX, plateY = app.counterX1*(2/3), app.counterY1+app.boxSize/2
    # #change to a list, also show on screen how many plates left (if stacked)
    # app.plate = Plate(None, plateX, plateY)
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
        #split by if within bounds of each box
        if app.chef1.holding == None: #chef holding nothing
        #     if (app.dirtyPlates != [] and inRange(app, app.chef1, app.dirtyPlates[0])):
        #         app.chef1.holding = app.dirtyPlates[0]
        #         app.dirtyPlates.pop()
        #     else:
                #checks if in range of ingredient boxes
            for box in app.boxes:
                if box.withinBox(app.chef1):
                    #picks up ingredient if within range of the box
                    app.chef1.holding = copy.copy(box.ingredient)                
            count = 0
            while count < len(app.usedCounters):
                counter = app.usedCounters[0]
                if counter.withinBox(app.chef1):
                    app.chef1.holding = counter.ingredient
                    app.usedCounters.pop(count)
                else:
                    count += 1
        else: #chef holding something
            #checks if in range of stove
            for stove in app.stoves:
                if stove.withinBox(app.chef1):
                    #cook() only cooks if given chopped meat
                    app.chef1.cook()
            if (app.orderBox.withinBox(app.chef1) or app.orderBox2.withinBox(app.chef1)):
                for order in app.orders:
                    if app.chef1.holding == order.order:
                    # and app.chef1.holding.plate != None):
                #change equality statement
                        print('order is valid')
                        app.chef1.serve(order)
                #check if always valid
                        app.score += 1
            elif (app.sink.withinBox(app.chef1) and isinstance(app.chef1.holding, Plate)
                    and not app.chef1.holding.clean):
                app.chef1.holding.clean = True
            elif (app.trash.withinBox(app.chef1)):
                app.chef1.holding = None
            #checks counters, if can combine with ingred on counter, do so
            for counter in app.usedCounters:
                if counter.withinBox(app.chef1):
                    counterItem = counter.ingredient
                    if (isinstance(app.chef1.holding, Burger)):
                        if isinstance(counterItem, Burger): #burger on counter
                            if counterItem != app.chef1.holding: #checks if both burgers don't have same ingred
                                counter.ingredient.addIngred(app.chef1.holding)
                                app.chef1.holding = None
                        else: #Veggie, Meat, Bread on counter
                            if not counterItem.isRaw and counterItem not in app.chef1.holding.ingredients:
                                app.chef1.holding.addIngred(counterItem)
                                counter.ingredient = app.chef1.holding
                                app.chef1.holding = None
                    elif (app.chef1.holding != None and not app.chef1.holding.isRaw): #cooked meat, chopped veggies, or bread
                        if isinstance(counterItem, Burger):
                            if app.chef1.holding not in counterItem:
                                counter.ingredient.addIngred(app.chef1.holding)
                                app.chef1.holding = None
                        else: #Veggie, Meat, Bread on counter
                            if not counterItem.isRaw and counterItem != app.chef1.holding:
                                newBurg = Burger([counterItem, app.chef1.holding], app)
                                app.chef1.holding = None
                                counter.ingredient = newBurg
                #note: fix redundant code (make burger and ingredient have same functions)
            else: #should be not at edge of counter or at edge of an empty counter
                chefx0, chefy0 = app.chef1.cx-app.chef1.r, app.chef1.cy-app.chef1.r
                chefx1, chefy1 = app.chef1.cx+app.chef1.r, app.chef1.cy+app.chef1.r
                x0, y0 = 0, 0
                if chefx0 == app.counterX0:
                    x0, y0 = app.counterX0-app.boxSize, (app.chef1.cy//(16*3))*16*3
                elif chefx1 == app.counterX1:
                    x0, y0 = app.counterX1, (app.chef1.cy//(16*3))*16*3
                elif chefy0 == app.counterY0:
                    x0, y0 = (app.chef1.cx//(16*3))*16*3, app.counterY0-app.boxSize
                elif chefy1 == app.counterY1:
                    x0, y0 = (app.chef1.cx//(16*3))*16*3, app.counterY1
                #if at edge of empty counter, place item down
                #CANNOT BE WITHIN BOUNDS OF OTHER SPECIAL COUNTERS
                if x0+y0 != 0:
                    newCounter = Counter(x0, y0, app.boxSize, app.chef1.holding)
                    isValid = True
                    for counter in app.usedCounters:
                        if counter == newCounter:
                            isValid = False
                    for box in app.specialBoxes:
                        if box == newCounter:
                            isValid = False
                    if isValid:
                        app.usedCounters.append(newCounter)
                        app.chef1.holding = None
    elif event.key == 'Tab':
        #checks if in range of chopping board
        for board in app.chopBoards:
            if board.withinBox(app.chef1) and (isinstance(app.chef1.holding, Veggie)
                    or isinstance(app.chef1.holding, Meat)):
                app.chef1.chop()
        #dash?
    elif event.key == 'Escape':
        app.paused = not app.paused

def timerFired(app):
    if not app.paused:
        app.time += 1
    #prevent indexing error if no orders
    if app.orders != [] and app.orders[0].orderDone:
        # plateX, plateY = app.counterX1+app.boxSize/2, app.orderBox.y0-app.boxSize*2
        # newDirtyPlate = Plate(None, plateX, plateY)
        # newDirtyPlate.clean = False
        # app.dirtyPlates.append(newDirtyPlate)
        app.orders.pop(0)
    if app.time%10 == 0 and len(app.orders) <= 5: #sets a max of 5 orders at a time
        app.orders.append(Order(app))
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
    #moves by 1 pixel which = 3
    newX, newY = app.chef1.cx + 6*dx, app.chef1.cy + 6*dy
    if (app.counterX0 <= (newX - app.chef1.r) and 
        app.counterX1 >= (newX + app.chef1.r) and 
        app.counterY0 <= (newY - app.chef1.r) and
        app.counterY1 >= (newY + app.chef1.r)):
        app.chef1.cx, app.chef1.cy = newX, newY

#Note: fix so holding a raw/raw on counter will not do anything
#picks up ingredient on table
# if chef is holding another ingredient and the two can be combined, combines them to make a burger
def pickUp(app):
    otherIngred = None
    #change so that if already in burger, ingredient can't be combined
    # if (isinstance(app.chef1.holding, Burger) or 
    #     isinstance(app.chef1.holding, Ingredient) and not app.chef1.holding.isRaw):
    if ((isinstance(app.chef1.holding, Veggie) and app.chef1.holding.isChopped)
            or (isinstance(app.chef1.holding, Meat) and app.chef1.holding.isCooked)
            or isinstance(app.chef1.holding, Burger)):
        otherIngred = app.chef1.holding
    count = 0
    while count < len(app.placedIngred):
        ingred = app.placedIngred[count]
        if (((ingred[1]+app.boxSize/2 == app.chef1.cx-app.chef1.r or 
                ingred[1]-app.boxSize/2 == app.chef1.cx+app.chef1.r) and 
                ingred[2]-5 <= app.chef1.cy <= ingred[2]+5) or 
                ((ingred[2]+app.boxSize/2 == app.chef1.cy-app.chef1.r or
                ingred[2]-app.boxSize/2 == app.chef1.cy+app.chef1.r) and
                ingred[1]-5 <= app.chef1.cx <= ingred[1]+5)):
            #item is within chef range on left, right, top, or bottom counter (with leniance)
            # not ((not isinstance(app.chef1.holding, Burger) and app.chef1.holding.isRaw)
            #         or (isinstance(app.chef1.holding, Burger) and ingred[0].isRaw))
            app.placedIngred.pop(count)
            app.chef1.holding = ingred[0]
        else:
            count += 1
    #combines the two ingred/burgers -> burger
    if otherIngred != None:
        if (isinstance(app.chef1.holding, Burger) and 
                isinstance(otherIngred, Burger)):
            for ingred in otherIngred.ingredients:
                app.chef1.holding.addIngred(ingred)
        elif isinstance(app.chef1.holding, Burger):
            app.chef1.holding.addIngred(otherIngred)
        elif isinstance(otherIngred, Burger):
            app.chef1.holding = otherIngred.addIngred(app.chef1.holding)
        else: #neither are burgers
            app.chef1.holding = Burger(app.chef1.holding, otherIngred)

def placeOnCounter(app):
    ingredX, ingredY = 0, 0
    #checks if within counter ranges
    if app.counterX0 == app.chef1.cx-app.chef1.r:
        #left
        ingredX, ingredY = app.counterX0-app.boxSize/2, app.chef1.cy
    elif app.counterX1 == app.chef1.cx+app.chef1.r:
        #right
        ingredX, ingredY = app.counterX1+app.boxSize/2, app.chef1.cy
    elif app.counterY0 == app.chef1.cy-app.chef1.r:
        #up
        ingredX, ingredY = app.chef1.cx, app.counterY0-app.boxSize/2
    elif app.counterY1 == app.chef1.cy+app.chef1.r:
        #down
        ingredX, ingredY = app.chef1.cx, app.counterY1+app.boxSize/2
    if ingredX != 0 and ingredY != 0:
        # if app.placedIngred == []:
        app.placedIngred.append((app.chef1.holding, ingredX, ingredY))
        app.chef1.holding = None
        # else:
        #     for ingred in app.placedIngred:
        #         if not (ingred[1]-5 <= ingredX <= ingred[1] + 5 and ingred[2]-5 <= ingredY <= ingred[2]+5):
        #             app.placedIngred.append((app.chef1.holding, ingredX, ingredY))
        #             app.chef1.holding = None

# def inRange(app, chef, box):
    # if isinstance(box, Plate):
    #     if ((box.x-box.r <= chef.cx <= box.x+box.r and chef.cy+chef.r == box.y-app.boxSize/2) or
    #             box.y-box.r <= chef.cy <= box.y+box.r and chef.cx+chef.r == box.x-app.boxSize/2):
    #         return True #add to ranges, right now only accounts for plates at bottom and right counter
    #     else:
    #         return False

#spawns in a rat with a given target
def spawnRat(app):
    target = app.placedIngred[0] #change so ingred obj has x, y
    targetX, targetY = target[1], target[2]
    app.rat = Rat(app, target, targetX, targetY)

def redrawAll(app, canvas):
    bgCenterX, bgCenterY = app.width/2, app.height-app.background.size[1]/2
    canvas.create_image(bgCenterX, bgCenterY, image=ImageTk.PhotoImage(app.background))
    ord1X, ord1Y = 0, 0
    for order in app.orders:
        if not order.orderDone:
            imageWidth, imageHeight = order.image.size[0], order.image.size[1]
            canvas.create_image(ord1X+imageWidth/2, ord1Y+imageHeight/2, image=ImageTk.PhotoImage(order.image))
            canvas.create_rectangle(ord1X, ord1Y+imageHeight, ord1X+imageWidth*order.orderTime/order.totalTime, ord1Y+imageHeight+16*3/2, fill='red')
            ord1X += imageWidth
    canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef))
    #shows what chef is holding
    if app.chef1.holding != None:
        canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef1.holding.image))
    #shows score
    canvas.create_text(16*3, app.height-16*3/2, text=f'Score: {app.score}', fill='white', font='Arial 13 bold')
    #draw order box
    canvas.create_rectangle(app.orderBox.x0, app.orderBox.y0, app.orderBox.x1, app.orderBox.y1)
    canvas.create_text(app.orderBox.x0+app.boxSize/2, app.orderBox.y0+app.boxSize/2, text='orders')
    #draws plates
    # canvas.create_oval(app.plate.x-app.plate.r, app.plate.y-app.plate.r, app.plate.x+app.plate.r, app.plate.y+app.plate.r)
    # canvas.create_text(app.plate.x, app.plate.y, text='clean plates')
    #draws chef
    canvas.create_oval(app.chef1.cx-app.chef1.r, app.chef1.cy-app.chef1.r,
                app.chef1.cx+app.chef1.r, app.chef1.cy+app.chef1.r)
    #shows what is on the counters
    # for ingred in app.placedIngred:
    #     ingredX, ingredY = ingred[1], ingred[2]
    #     name = ingred[0]
    #     canvas.create_text(ingredX, ingredY, text=name)
    for counter in app.usedCounters:
        canvas.create_text(counter.x0+24, counter.y0+24, text=str(counter.ingredient))
        cx, cy = counter.x0+app.boxSize/2, counter.y0+app.boxSize/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(counter.ingredient.image))
    #draws dirty plates
    for plate in app.dirtyPlates:
        canvas.create_oval(plate.x-plate.r, plate.y-plate.r, plate.x+plate.r, plate.y+plate.r)
        canvas.create_text(plate.x, plate.y, text='dirty plates')
    #draw rat
    if app.rat != None and not app.rat.dead:
        r = 30
        canvas.create_oval(app.rat.x-r, app.rat.y-r, app.rat.x+r, app.rat.y+r)
        canvas.create_text(app.rat.x, app.rat.y, text=app.rat)
    
    # canvas.create_line(16*3, 0, 16*3, 600, fill='red')
    # canvas.create_line(32*3, 0, 32*3, 600, fill='red')
    # canvas.create_line(0, 48*3, 700, 48*3, fill='red')


runApp(width=720, height=528+32*3)