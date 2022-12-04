from cmu_112_graphics import *
import cs112_f22_week10_linter
import decimal
import copy

#Import object classes
from ingredient import *
from chef import *
from box import *
from rat import *

#Title: Overcooked! - A Ratty Situation
#Map size is 720x528 and is divided into 15x11 total boxes, each sized (16*3)x(16*3)

def appStarted(app):
    app.background = app.loadImage('background.png') #map drawn by me
    url = 'https://www.team17.com/wp-content/uploads/2020/08/Overcooked_iPad_Tile.jpg'
    app.homescreen = app.loadImage(url)
    app.homescreen = app.scaleImage(app.homescreen, 1/1.75)
    #characters
    app.chef1 = Chef(1, app.width/2, app.height/2, 24, app)
    app.rat = None
    #sets bounds for walkable tiles and sets size of each box
    app.counterX0, app.counterY0 = 16*2*3, 16*5*3
    app.counterX1, app.counterY1 = app.width-16*2*3, app.height-16*2*3
    app.boxSize = 16*3
    #ingredient boxes
    app.box1 = Counter(16*3, 16*5*3, app.boxSize, Veggie('tomato', app))
    app.box2 = Counter(16*3, 16*6*3, app.boxSize, Meat('meat', app))
    app.box3 = Counter(16*3, 16*7*3, app.boxSize, Ingredient('bread', app))
    app.box4 = Counter(16*3, 16*8*3, app.boxSize, Veggie('lettuce', app))
    app.boxes = [app.box1, app.box2, app.box3, app.box4]
    #appliances (chop board, stove, and trash)
    app.chopBoard = Appliance(16*3*3, app.height-16*2*3, app.boxSize, app.chef1.chop)
    app.chopBoard2 = Appliance(16*5*3, app.height-16*2*3, app.boxSize, app.chef1.chop)
    app.chopBoards = [app.chopBoard, app.chopBoard2]
    app.stove = Appliance(app.width-16*3*3, 16*4*3, app.boxSize, app.chef1.cook)
    app.stove2 = Appliance(app.width-16*4*3, 16*4*3, app.boxSize, app.chef1.cook)
    app.stove3 = Appliance(app.width-16*5*3, 16*4*3, app.boxSize, app.chef1.cook)
    app.stove4 = Appliance(app.width-16*6*3, 16*4*3, app.boxSize, app.chef1.cook)
    app.stoves = [app.stove, app.stove2, app.stove3, app.stove4]
    app.trash = Appliance(16*3, 16*10*3, app.boxSize, app.chef1.discard)
    app.orderBox = Appliance(app.width-16*2*3, 16*7*3, app.boxSize, app.chef1.serve)
    app.orderBox2 = Appliance(app.width-16*2*3, 16*8*3, app.boxSize, app.chef1.serve)
    app.sink = Appliance(16*3*3, 16*4*3, app.boxSize, app.chef1.wash)
    app.specialBoxes = app.chopBoards + app.stoves + app.boxes + [app.trash, app.orderBox, app.orderBox2, app.sink]
    #plates
    app.plates = [Plate(app), Plate(app), Plate(app)]
    app.plateCounters = [Counter(app.width-16*5*3, app.height-16*2*3, app.boxSize, app.plates[0]), 
        Counter(app.width-16*4*3, app.height-16*2*3, app.boxSize, app.plates[1]), 
        Counter(app.width-16*3*3, app.height-16*2*3, app.boxSize, app.plates[2])]
    #other variables
    app.time = 0
    app.timerDelay = 100
    app.endTime = 65*10 #125
    app.paused = False
    app.score = 0
    app.maxScore = 0
    app.gameOver = False
    app.mode = 'splashScreenMode'
    app.usedCounters = []
    app.orders = [Order(app)] #creates new order when game starts

# Splash Screen Mode
def splashScreenMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.homescreen))
    canvas.create_text(app.width/2, app.height*(9/10), text='Press any key to start', fill='white', font='Arial 20 bold')

# Mode code based off of https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
# This method below was copied from the link
def splashScreenMode_keyPressed(app, event):
    app.mode = 'gameMode'

# Game Mode
def gameMode_keyPressed(app, event):
    if app.gameOver:
        return
    if event.key == 'w':
        app.chef1.move(app, 0, -1)
        app.chef1.setAnimation('up')
    elif event.key == 'a':
        app.chef1.move(app, -1, 0)
        app.chef1.setAnimation('left')
    elif event.key == 's':
        app.chef1.move(app, 0, +1)
        app.chef1.setAnimation('down')
    elif event.key == 'd':
        app.chef1.move(app, +1, 0)
        app.chef1.setAnimation('right')
    elif event.key == 'Space':
        if app.chef1.holding == None: #chef holding nothing
            #checks if in range of ingredient boxes
            for box in app.boxes:
                if box.withinBox(app.chef1):
                    #picks up ingredient if within range of the box
                    app.chef1.holding = copy.copy(box.ingredient)                
            count = 0
            #picks up ingredient if counter has it
            while count < len(app.usedCounters):
                counter = app.usedCounters[count]
                if counter.withinBox(app.chef1):
                    app.chef1.holding = counter.ingredient
                    app.usedCounters.pop(count)
                else:
                    count += 1
            count = 0
            #picks up plate on counter
            while count < len(app.plateCounters):
                counter = app.plateCounters[count]
                if counter.withinBox(app.chef1):
                    app.chef1.holding = app.plateCounters.pop(count).ingredient
                else:
                    count += 1
        else: #chef holding something
            #checks if in range of stove
            for stove in app.stoves:
                if stove.withinBox(app.chef1):
                    #cook() only cooks if given chopped meat
                    app.chef1.cook()
            #checks if within range of trash box, if so then trashes object
            if (app.trash.withinBox(app.chef1) and not isinstance(app.chef1.holding, Plate)):
                if app.chef1.holding.plate != None:
                    plate = app.chef1.holding.plate
                    app.chef1.holding = plate
                else:
                    app.chef1.holding = None
            elif (app.sink.withinBox(app.chef1)):
                if isinstance(app.chef1.holding, Plate):
                    app.chef1.wash()
            #checks if in range of order box and can complete order
            elif (app.orderBox.withinBox(app.chef1) or app.orderBox2.withinBox(app.chef1)):
                for order in app.orders:
                    if app.chef1.holding == order.order and app.chef1.holding.plate != None and not app.chef1.holding.plate.isDirty:
                        if order.orderDoubled:
                            app.score += 2
                        else:
                            app.score += 1
                        dirtyPlate = app.chef1.serve(order)
                        app.plateCounters.append(Counter(app.width-16*2*3, 16*9*3, app.boxSize, dirtyPlate))
            #holding an non-raw ingredient that does not have a plate in front of a counter with a plate -> plates ingredient and places it on counter
            elif not isinstance(app.chef1.holding, Plate) and (isinstance(app.chef1.holding, Burger) or not app.chef1.holding.isRaw):
                count = 0
                while count < len(app.plateCounters):
                    counter = app.plateCounters[count]
                    if counter.withinBox(app.chef1) and app.chef1.holding.plate == None:
                        app.chef1.holding.plate = counter.ingredient
                        app.plateCounters[count].ingredient = app.chef1.holding
                        newCounter = app.plateCounters.pop(count)
                        app.usedCounters.append(newCounter)
                        app.chef1.holding = None
                    else:
                        count += 1
            #checks counters, if can combine with ingred on counter, do so
            for counter in app.usedCounters:
                counterItem = counter.ingredient
                if counter.withinBox(app.chef1) and not isinstance(counterItem, Plate) and app.chef1.holding != None and counterItem != None:
                    if isinstance(counterItem, Burger) or not counterItem.isRaw:
                        if isinstance(app.chef1.holding, Plate):
                            if counterItem.plate != None:
                                plate = app.chef1.holding.plate
                                counter.ingredient.addIngred(app.chef1.holding)
                                app.chef1.holding = None
                                counter.ingredient.plate = plate
                        else:
                            if not (app.chef1.holding.plate != None and counterItem.plate != None): #don't run if both have plates
                                if (isinstance(app.chef1.holding, Burger)):
                                    if isinstance(counterItem, Burger): #burger on counter
                                        if counterItem != app.chef1.holding: #checks if both burgers don't have same ingred
                                            counter.ingredient.addIngred(app.chef1.holding)
                                            if app.chef1.holding.plate != None:
                                                counter.ingredient.plate = app.chef1.holding.plate
                                            app.chef1.holding = None
                                    else: #Veggie, Meat, Bread on counter
                                        if not counterItem.isRaw and counterItem not in app.chef1.holding.ingredients:
                                            app.chef1.holding.addIngred(counterItem)
                                            counter.ingredient = app.chef1.holding
                                            if counterItem.plate != None:
                                                app.chef1.holding.plate = counterItem.plate
                                            app.chef1.holding = None
                                elif (not app.chef1.holding.isRaw): #cooked meat, chopped veggies, or bread
                                    if isinstance(counterItem, Burger):
                                        if app.chef1.holding not in counterItem.ingredients:
                                            counter.ingredient.addIngred(app.chef1.holding)
                                            if app.chef1.holding.plate != None:
                                                counter.ingredient.plate = app.chef1.holding.plate
                                            app.chef1.holding = None
                                    else: #Veggie, Meat, Bread on counter
                                        if not counterItem.isRaw and counterItem != app.chef1.holding:
                                            newBurg = Burger([counterItem, app.chef1.holding], app)
                                            if counterItem.plate != None:
                                                newBurg.plate = counterItem.plate
                                            elif app.chef1.holding != None:
                                                newBurg.plate = app.chef1.holding.plate
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
                if x0+y0 != 0:
                    newCounter = Counter(x0, y0, app.boxSize, app.chef1.holding)
                    isValid = True
                    for counter in app.usedCounters:
                        if counter == newCounter:
                            isValid = False
                    for box in app.specialBoxes:
                        if box == newCounter:
                            isValid = False
                    for counter in app.plateCounters:
                        if counter == newCounter:
                            isValid = False
                    #prevents plate from being placed where dirty plates will spawn
                    if newCounter.x0 == app.width-16*2*3 and newCounter.y0 == 16*9*3:
                        isValid = False
                    if isValid:
                        if isinstance(newCounter.ingredient, Plate):
                            app.plateCounters.append(newCounter)
                        else:
                            app.usedCounters.append(newCounter)
                        app.chef1.holding = None
    elif event.key == 'Tab':
        #checks if in range of chopping board
        for board in app.chopBoards:
            if board.withinBox(app.chef1) and (isinstance(app.chef1.holding, Veggie)
                    or isinstance(app.chef1.holding, Meat)):
                app.chef1.chop()
    elif event.key == 'Escape':
        app.paused = not app.paused

def gameMode_timerFired(app):
    # app.chef1.animation = []
    # if app.chef1.animation != []:
    if app.chef1.animationName in ['chop', 'cook']:
        name = app.chef1.animationName
        if app.chef1.counterDict[name] < len(app.chef1.animation):
            app.chef1.counterDict[name] += 1
        if app.chef1.counterDict[name] == len(app.chef1.animation):
            app.chef1.animationName = 0
            app.chef1.animation = []
            app.chef1.counterDict[name] = 0
    if app.gameOver:
        return
    if not app.paused:
        app.time += 1
    if app.time == app.endTime:
        app.gameOver = True
    #prevent indexing error if no orders
    if app.orders != [] and app.orders[0].orderDone:
        app.orders.pop(0)
    if app.time%(10*15) == 0 and len(app.orders) <= 5: #sets a max of 5 orders at a time
        newOrder = Order(app)
        app.orders.append(newOrder)
        if newOrder.orderDoubled:
            app.maxScore += 2
        else:
            app.maxScore += 1
    if app.orders != []:
        orderNum = 0
        while orderNum < len(app.orders):
            order = app.orders[orderNum]
            order.countdown()
            if order.orderFailed:
                app.orders.pop(orderNum) #remove order w/o rewarding points
            else:
                orderNum += 1
    if 0 <= app.time%(15*10) <= 2 and app.usedCounters != [] and app.rat == None:
        #spawns in a rat with a given target
        setTarget = False
        count = 0
        while not setTarget and count < len(app.usedCounters):
            target = app.usedCounters[count]
            if target.ingredient.plate == None: #does not target items with a plate
                setTarget = True
            count += 1
        if setTarget:
            app.rat = Rat(app, target)
    if app.rat != None:
        if app.time%5==0:
            app.rat.grabFood()
        #Note: may be buggy if pick up food right before rat gets to it
        if app.rat.hasFood:
            # print('has food')
            app.usedCounters.remove(app.rat.target)
            app.rat = None
        else:
            ingredMoved = True
            for counter in app.usedCounters:
                if counter == app.rat.target:
                    ingredMoved = False
            if ingredMoved:
                app.rat.dead = True
                app.rat = None

def gameMode_redrawAll(app, canvas):
    #draws map
    bgCenterX, bgCenterY = app.width/2, app.height-app.background.size[1]/2
    canvas.create_image(bgCenterX, bgCenterY, image=ImageTk.PhotoImage(app.background))
    #draws orders
    ord1X, ord1Y = 0, 0
    for order in app.orders:
        if not order.orderDone:
            imageWidth, imageHeight = order.image.size[0], order.image.size[1]
            canvas.create_image(ord1X+imageWidth/2, ord1Y+imageHeight/2, image=ImageTk.PhotoImage(order.image))
            canvas.create_rectangle(ord1X, ord1Y+imageHeight, ord1X+imageWidth*order.orderTime/order.totalTime, ord1Y+imageHeight+16*3/2, fill='red')
            ord1X += imageWidth
    #draws chef
    if app.chef1.animation == []:
        canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef1.image))
    else:
        i = app.chef1.counterDict[app.chef1.animationName]
        canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef1.animation[i]))
    #draws what chef is holding on top of chef
    if app.chef1.holding != None:
        if app.chef1.animationName == 'chop':
            canvas.create_image(app.chef1.cx, app.chef1.cy+app.boxSize, image=ImageTk.PhotoImage(app.chef1.holding.rawImage))
        elif app.chef1.animationName == 'cook':
            if isinstance(app.chef1.holding, Plate): #washing
                im = app.chef1.holding.dirtyImage
            else: #cooking
                im = app.chef1.holding.rawImage
            canvas.create_image(app.chef1.cx, app.chef1.cy-app.boxSize, image=ImageTk.PhotoImage(im))
        else:
            if isinstance(app.chef1.holding, Plate): 
                canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef1.holding.image))
            elif app.chef1.holding.plate != None:
                canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef1.holding.plate.image))
            if isinstance(app.chef1.holding, Burger):
                # app.chef1.holding.burgerImage(app)
                if app.chef1.holding.imageList:
                    for ingred in app.chef1.holding.ingredients:
                        canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(ingred.image))
                else:
                    canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef1.holding.image))
            else:
                canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef1.holding.image))
    #draws score, time, and what chef is holding at the bottom of the screen
    canvas.create_text(16*3, app.height-16*3/2, text=f'Score: {app.score}', fill='white', font='Arial 13 bold')
    canvas.create_text(app.width-16*1.5*3, app.height-16*3/2, text=f'Time left: {(app.endTime-app.time)//10}', fill='white', font='Arial 13 bold')
    holdingText = str(app.chef1.holding)
    if app.chef1.holding != None and not isinstance(app.chef1.holding, Plate) and app.chef1.holding.plate != None:
        holdingText += " " + str(app.chef1.holding.plate)
    canvas.create_text(app.width/2, app.height-16*3/2, text=f'Holding: {holdingText}', fill='white', font='Arial 9 bold')
    #draws items on counters
    for counter in app.usedCounters:
        if counter.ingredient != None:
            cx, cy = counter.x0+app.boxSize/2, counter.y0+app.boxSize/2
            if counter.ingredient.plate != None:
                canvas.create_image(cx, cy, image=ImageTk.PhotoImage(counter.ingredient.plate.image))
            if isinstance(counter.ingredient, Burger):
                # counter.ingredient.burgerImage(app)
                if counter.ingredient.imageList:
                    for ingred in counter.ingredient.ingredients:
                        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(ingred.image))
                else:
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(counter.ingredient.image))
            else:
                canvas.create_image(cx, cy, image=ImageTk.PhotoImage(counter.ingredient.image))
            # canvas.create_text(counter.x0+24, counter.y0+24, text=str(counter.ingredient), font='Arial 9 bold', fill='white')
    #draws plates
    for counter in app.plateCounters:
        cx, cy = counter.x0+app.boxSize/2, counter.y0+app.boxSize/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(counter.ingredient.image))
    #draws rat
    if app.rat != None and not app.rat.dead:
        canvas.create_image(app.rat.moveX+app.boxSize/2, app.rat.moveY+app.boxSize/2, image=ImageTk.PhotoImage(app.rat.image))
        # canvas.create_oval(app.rat.moveX, app.rat.moveY, app.rat.moveX+app.boxSize, app.rat.moveY+app.boxSize)
        # canvas.create_text(app.rat.moveX, app.rat.moveY, text=app.rat)
    #draws game over screen
    if app.gameOver:
        canvas.create_text(app.width/2, 2/5*app.height, text="Time's Up!", fill='white', font='Arial 20 bold')
        if app.score >= app.maxScore/3:
            outcome = 'win!'
        else:
            outcome = 'lose.'
        canvas.create_text(app.width/2, 3/5*app.height, fill='white', text=f'Your score was {app.score}. You {outcome}', font='Arial 20 bold')

runApp(width=720, height=528+32*3)