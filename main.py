from cmu_112_graphics import *
import cs112_f22_week10_linter
import decimal
import copy
import pygame
import random

#Import object classes
from ingredient import *
from chef import *
from box import *
from rat import *

################################################################################
#Overcooked! - A Ratty Situation
#Note on graphics: Map size is 720x528 and is divided into 15x11 total boxes, each sized (16*3)x(16*3)
################################################################################

def appStarted(app):
    #Map drawn by me
    app.background = app.loadImage('background.png')
    url = 'https://www.team17.com/wp-content/uploads/2020/08/Overcooked_iPad_Tile.jpg'
    app.homescreen = app.loadImage(url)
    app.homescreen = app.scaleImage(app.homescreen, 1/1.75)
    #Rock image source: http://pixelartmaker.com/art/da268f06e621b21
    app.rock = app.loadImage('rock.png')
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
    app.plates = [Plate(app), Plate(app)]
    app.plateCounters = [Counter(app.width-16*3*3, app.height-16*2*3, app.boxSize, app.plates[0]), 
        Counter(app.width-16*4*3, app.height-16*2*3, app.boxSize, app.plates[1])]
    #other variables
    app.time = 0
    app.timerDelay = 100
    app.endTime = 120*10 #120
    app.paused = True
    app.score = 0
    app.maxScore = 0
    app.gameOver = False
    app.mode = 'startScreenMode'
    app.usedCounters = []
    app.orders = [Order(app)] #creates new order when game starts
    app.level = ''
    app.obstacles = []
    app.instructions = app.loadImage('instructions.jpg')
    pygame.mixer.init()

#Stops music when app stops
def appStopped(app):
    pygame.mixer.music.stop()

# Start Screen Mode
################################################################################
def startScreenMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.homescreen))
    canvas.create_text(app.width/4, app.height*(9/10), text="Press '1' for normal mode", fill='white', font='Arial 16 bold')
    canvas.create_text(app.width*(3/4), app.height*(9/10), text="Press '2' for hard mode", fill='white', font='Arial 16 bold')

# Mode code based off of https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
def startScreenMode_keyPressed(app, event):
    if event.key in ['1', '2']:
        if event.key == '1':
            app.level = 'normal'
        else:
            app.level = 'hard'
            spawnObstacles(app)
        app.mode = 'helpMode'
        #Game Music sound from https://downloads.khinsider.com/game-soundtracks/album/overcooked-2016-pc/Demo%25201%2520v2.mp3
        pygame.mixer.music.load('game_music.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.pause()

def spawnObstacles(app):
    while len(app.obstacles) < 8: #spawns in 8 obstacles (doesn't obstruct path to counters)
        col, row = random.randint(0+2, PathPlan.cols-1-2), random.randint(0+2, PathPlan.rows-1-2)
        if (row, col) in app.obstacles:
            continue
        elif (row, col) == PathPlan.convertToRowCol(app.chef1.cx, app.chef1.cy):
            continue
        else:
            app.obstacles.append((row, col))
################################################################################

# Help Mode
################################################################################
def helpMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.instructions))

def helpMode_keyPressed(app, event):
    #pauses game and shows instructions
    if event.key == 'Escape':
        app.mode = 'gameMode'
        app.paused = False
        pygame.mixer.music.unpause()
################################################################################

# Game Mode
################################################################################
def gameMode_keyPressed(app, event):
    if app.gameOver:
        if event.key == 'Enter':
            app.gameOver = False
            appStarted(app) #restarts game
        else:
            return
    if not app.chef1.animationName in ['chop', 'cook', 'wash']:
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
    if event.key == 'Space':
        if app.chef1.holding == None: #chef holding nothing
            #checks if in range of ingredient boxes
            for box in app.boxes:
                if box.withinBox(app.chef1):
                    #picks up ingredient
                    app.chef1.holding = copy.copy(box.ingredient)                
            #checks if in range of counters with ingredients on it
            count = 0
            while count < len(app.usedCounters):
                counter = app.usedCounters[count]
                if counter.withinBox(app.chef1):
                    #picks up ingredient, removing it from counter
                    app.chef1.holding = counter.ingredient
                    app.usedCounters.pop(count)
                else:
                    count += 1
            #picks up plate on counter if in range
            count = 0
            while count < len(app.plateCounters) and app.chef1.holding == None:
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
            #checks if in range of chopping board
            for board in app.chopBoards:
                if board.withinBox(app.chef1) and (isinstance(app.chef1.holding, Veggie)
                        or isinstance(app.chef1.holding, Meat)):
                    app.chef1.chop()
            #checks if within range of trash box, if so then trashes object
            if (app.trash.withinBox(app.chef1) and not isinstance(app.chef1.holding, Plate)):
                if app.chef1.holding.plate != None:
                    #only trashes food on the plate, not the plate itself
                    plate = app.chef1.holding.plate
                    app.chef1.holding = plate
                else:
                    app.chef1.holding = None
            #checks if within range of sink
            elif (app.sink.withinBox(app.chef1)):
                if isinstance(app.chef1.holding, Plate) and app.chef1.holding.isDirty:
                    app.chef1.wash()
            #checks if in range of order box and can complete order
            elif (app.orderBox.withinBox(app.chef1) or app.orderBox2.withinBox(app.chef1)):
                for order in app.orders:
                    if app.chef1.holding == order.order and app.chef1.holding.plate != None and not app.chef1.holding.plate.isDirty:
                        if order.orderDoubled: #if is a big order, doubles score
                            #score is based off of how much time is left before order is completed
                            app.score += 2*(order.totalTime-order.orderTime+1)
                        else:
                            app.score += (order.totalTime-order.orderTime+1)
                        dirtyPlate = app.chef1.serve(order) #serves order and makes plate dirty
                        app.plateCounters.append(Counter(app.width-16*2*3, 16*9*3, app.boxSize, dirtyPlate))
                        #Code to play sound from https://stackoverflow.com/questions/42393916/how-can-i-play-multiple-sounds-at-the-same-time-in-pygame
                        #Sound Effect from https://pixabay.com/sound-effects/search/ding/
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('bell.wav')) #plays sound when order served
            #holding an non-raw ingredient that does not have a plate in front of a counter with a plate -> plates ingredient and places it on counter
            elif not isinstance(app.chef1.holding, Plate) and (isinstance(app.chef1.holding, Burger) or not app.chef1.holding.isRaw):
                count = 0
                while count < len(app.plateCounters):
                    counter = app.plateCounters[count]
                    if counter.withinBox(app.chef1) and app.chef1.holding.plate == None and not counter.ingredient.isDirty:
                        app.chef1.holding.plate = counter.ingredient
                        app.plateCounters[count].ingredient = app.chef1.holding
                        newCounter = app.plateCounters.pop(count)
                        app.usedCounters.append(newCounter)
                        app.chef1.holding = None
                    else:
                        count += 1
            #checks counters with ingredients on it, if can combine what chef is holding with what's on the counter, do so
            for counter in app.usedCounters:
                counterItem = counter.ingredient
                if counter.withinBox(app.chef1) and not isinstance(counterItem, Plate) and app.chef1.holding != None and counterItem != None:
                    if isinstance(counterItem, Burger) or not counterItem.isRaw: #ingredient on counter has to be not raw (either chopped/cooked - unless it's bread)
                        if isinstance(app.chef1.holding, Plate):
                            #if chef is holding an empty plate, put what's on the counter on the plate and place the plate on the counter
                            if counterItem.plate == None and not app.chef1.holding.isDirty:
                                plate = app.chef1.holding
                                app.chef1.holding = None
                                counter.ingredient.plate = plate
                        else: #chef is not holding a plate
                            #checks that what the chef is holding and what's on the counter don't both have plates
                            if not (app.chef1.holding.plate != None and counterItem.plate != None):
                                #chef holding burger
                                if (isinstance(app.chef1.holding, Burger)):
                                    if isinstance(counterItem, Burger):
                                        #chef holding burger and burger on counter -> combines if they don't have the same ingredients
                                        if counterItem != app.chef1.holding:
                                            counter.ingredient.addIngred(app.chef1.holding)
                                            if app.chef1.holding.plate != None: #if chef's burger has a plate, transfer the plate to the new burger
                                                counter.ingredient.plate = app.chef1.holding.plate
                                            app.chef1.holding = None
                                    else: #Veggie, Meat, Bread on counter (must not be raw) -> adds them to the burger the chef is holding if ingredient is not already in burger
                                        if not counterItem.isRaw and counterItem not in app.chef1.holding.ingredients:
                                            app.chef1.holding.addIngred(counterItem)
                                            counter.ingredient = app.chef1.holding
                                            if counterItem.plate != None: #if counter's burger has a plate, transfer the plate to the new burger
                                                app.chef1.holding.plate = counterItem.plate
                                            app.chef1.holding = None
                                #chef holding non-raw ingredients (cooked meat, chopped veggies, or bread)
                                elif (not app.chef1.holding.isRaw):
                                    #if counter has a burger and chef is holding an ingredient not in it, add it to the burger
                                    if isinstance(counterItem, Burger):
                                        if app.chef1.holding not in counterItem.ingredients:
                                            counter.ingredient.addIngred(app.chef1.holding)
                                            if app.chef1.holding.plate != None:
                                                counter.ingredient.plate = app.chef1.holding.plate
                                            app.chef1.holding = None
                                    else: #Non-raw Veggie, Meat, Bread on counter
                                        #if counter item and what chef is holding are both non-raw ingredients, make new Burger with them
                                        if not counterItem.isRaw and counterItem != app.chef1.holding:
                                            newBurg = Burger([counterItem, app.chef1.holding], app)
                                            if counterItem.plate != None:
                                                newBurg.plate = counterItem.plate
                                            elif app.chef1.holding != None:
                                                newBurg.plate = app.chef1.holding.plate
                                            app.chef1.holding = None
                                            counter.ingredient = newBurg
            else: #checks if chef is located in front of an empty counter
                chefx0, chefy0 = app.chef1.cx-app.chef1.r, app.chef1.cy-app.chef1.r
                chefx1, chefy1 = app.chef1.cx+app.chef1.r, app.chef1.cy+app.chef1.r
                x0, y0 = 0, 0
                #if at the corner of a map, determines which counter chef is facing by checking its orientation (up/down/right)
                if chefx0 == app.counterX0:
                    #doesn't check if chef in left direction because then chef will be facing the trash which is not an empty counter
                    if chefy1 == app.counterY1 and app.chef1.animationName == 'down':
                        x0, y0 = chefx0, app.counterY1
                    elif chefy0 == app.counterY0 and app.chef1.animationName == 'up':
                        x0, y0 = chefx0, app.counterY0-app.boxSize
                    else: #if chef is not at a corner
                        x0, y0 = app.counterX0-app.boxSize, (app.chef1.cy//(16*3))*16*3
                elif chefx1 == app.counterX1:
                    if chefy1 == app.counterY1 and app.chef1.animationName == 'down':
                        x0, y0 = chefx0, app.counterY1
                    elif chefy0 == app.counterY0 and app.chef1.animationName == 'up':
                        x0, y0 = chefx0, app.counterY0-app.boxSize
                    elif app.chef1.animationName == 'right':
                        x0, y0 = app.counterX1, (app.chef1.cy//(16*3))*16*3
                #chef is not at a corner, either facing the top or bottom row of counters
                elif chefy0 == app.counterY0:
                    x0, y0 = (app.chef1.cx//(16*3))*16*3, app.counterY0-app.boxSize
                elif chefy1 == app.counterY1:
                    x0, y0 = (app.chef1.cx//(16*3))*16*3, app.counterY1
    
                #if chef is facing an empty counter, place item chef is holding on counter
                if x0+y0 != 0:
                    newCounter = Counter(x0, y0, app.boxSize, app.chef1.holding)
                    isValid = True
                    #cannot place item on used or special boxes
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
                    #if new counter is valid (can place item on it) -> do so
                    if isValid:
                        #places down plate
                        if isinstance(newCounter.ingredient, Plate):
                            app.plateCounters.append(newCounter)
                        else: #places down food
                            app.usedCounters.append(newCounter)
                        app.chef1.holding = None        
    elif event.key == 'm':
        #if in range, chef kills the rat
        if app.rat != None:
            if abs(app.chef1.cx-app.rat.x) <= app.boxSize and abs(app.chef1.cy-app.rat.y) <= app.boxSize:
                app.rat.counterDict[app.rat.animationName] = 0
                app.rat.animationName = ''
                app.rat.animation = []
                app.rat.image = app.hitImage
                app.rat.dead = True
    #pauses the game and shows the help screen
    elif event.key == 'Escape':
        app.paused = True
        pygame.mixer.music.pause()
        app.mode = 'helpMode'
    #shortcut commands for testing 
    elif event.key == '0': #quick gameOver key
        app.gameOver = True
    elif event.key == '9':
        if app.rat == None:
            setRatTarget(app)

def gameMode_timerFired(app):
    if app.gameOver: #if game over, function stops running
        pygame.mixer.music.pause()
        return
    if not app.paused:
        app.time += 1
        pygame.mixer.music.unpause()
    if app.paused:
        pygame.mixer.music.pause()
    if app.time == app.endTime:
        app.gameOver = True
        pygame.mixer.music.stop()
    if app.rat != None and app.rat.dead: #if rat is dead but object still exists, set object to None
        app.rat = None
    #changes animation index (counter)
    if app.chef1.animationName in ['chop', 'cook', 'wash']:
        name = app.chef1.animationName
        if app.chef1.counterDict[name] < len(app.chef1.animation):
            app.chef1.counterDict[name] += 1
        if app.chef1.counterDict[name] == len(app.chef1.animation):
            app.chef1.animationName = ''
            app.chef1.animation = []
            app.chef1.counterDict[name] = 0
    #removes orders when order is done (happens when orders are served)
    if app.orders != [] and app.orders[0].orderDone:
        app.orders.pop(0)
    if app.time%(15*10) == 0 and len(app.orders) < 5: #spawns new orders, sets a max of 5 orders at a time 
        newOrder = Order(app)
        app.orders.append(newOrder)
        if newOrder.orderDoubled:
            app.maxScore += 2*(newOrder.totalTime*(1/3))
        else:
            app.maxScore += newOrder.totalTime*(1/3)
    #removes orders if they expire (time runs out)
    if app.orders != []:
        orderNum = 0
        while orderNum < len(app.orders):
            order = app.orders[orderNum]
            order.countdown()
            if order.orderFailed:
                app.orders.pop(orderNum) #remove order w/o rewarding points
            else:
                orderNum += 1
    #spawns in rat every 10 seconds (with 2 second leniance)
    if 0 <= app.time%(10*10) <= 2 and app.usedCounters != [] and app.rat == None:
        setRatTarget(app)
    #rat targets food
    if app.rat != None:
        if app.rat.pathPlanner.target != None:
            app.rat.grabFood()
        if app.rat.hasFood:
            #rat takes food when reaches target
            app.usedCounters.remove(app.rat.pathPlanner.target)
            app.rat = None
        else:
            ingredMoved = True
            for counter in app.usedCounters:
                if counter == app.rat.pathPlanner.target:
                    ingredMoved = False
            if ingredMoved: #if rat's target moves, either sets new target (if possible) or rat is resting
                if app.usedCounters == []:
                    app.rat.pathPlanner.resetPath()
                    app.rat.pathPlanner.target = None
                    app.rat.counterDict[app.rat.animationName] = 0
                    app.rat.animation = []
                    app.rat.animationName = ''
                else:
                    setRatTarget(app)

def setRatTarget(app):
    #spawns in a rat with a given target
    setTarget = False
    count = 0
    #ensures that rat picks up a legal target
    while not setTarget and count < len(app.usedCounters):
        target = app.usedCounters[count]
        if target.ingredient.plate == None: #does not target items with a plate
            setTarget = True
        count += 1
    if setTarget:
        if app.rat == None:
            app.rat = Rat(app, target)
        else:
            row, col = PathPlan.convertToRowCol(app.rat.x, app.rat.y)
            app.rat.pathPlanner.generatePath(target, row, col)

def gameMode_redrawAll(app, canvas):
    #draws map
    bgCenterX, bgCenterY = app.width/2, app.height-app.background.size[1]/2
    canvas.create_image(bgCenterX, bgCenterY, image=ImageTk.PhotoImage(app.background))
    #draws obstacles (if there are any)
    for obstacle in app.obstacles:
        x, y = PathPlan.convertToPixels(obstacle[0], obstacle[1])
        canvas.create_image(x+app.boxSize/2, y+app.boxSize/2, image=ImageTk.PhotoImage(app.rock))
    #draws orders
    ord1X, ord1Y = 0, 0
    for order in app.orders:
        if not order.orderDone:
            imageWidth, imageHeight = order.image.size[0], order.image.size[1]
            canvas.create_image(ord1X+imageWidth/2, ord1Y+imageHeight/2, image=ImageTk.PhotoImage(order.image))
            canvas.create_rectangle(ord1X, ord1Y+imageHeight, ord1X+imageWidth*order.orderTime/order.totalTime, ord1Y+imageHeight+16*3/2, fill='red')
            ord1X += imageWidth
    #draws chef
    if app.chef1.animation == []: #if chef has no animation, draws resting image
        canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef1.image))
    else: #draws chef's currrent animation
        i = app.chef1.counterDict[app.chef1.animationName]
        canvas.create_image(app.chef1.cx, app.chef1.cy, image=ImageTk.PhotoImage(app.chef1.animation[i]))
    #draws what chef is holding on top of chef
    if app.chef1.holding != None:
        if app.chef1.animationName in ['chop', 'cook', 'wash']:
            thisBox = None
            if isinstance(app.chef1.holding, Plate): #washing
                im = app.chef1.holding.dirtyImage
            else: #cooking 
                im = app.chef1.holding.rawImage

            if app.chef1.animationName == 'chop':
                for board in app.chopBoards:
                    if board.withinBox(app.chef1):
                        thisBox = board
            elif app.chef1.animationName == 'wash':
                if app.sink.withinBox(app.chef1):
                    thisBox = app.sink
            else:
                for stove in app.stoves:
                    if stove.withinBox(app.chef1):
                        thisBox = stove
            canvas.create_image(thisBox.x0+app.boxSize/2, thisBox.y0+app.boxSize/2, image=ImageTk.PhotoImage(im))
        else:
            #draws ingredient chef is holding, location changes depending on the chef's orientation
            if app.chef1.animationName == 'up':
                objX, objY = app.chef1.cx, app.chef1.cy-app.boxSize/4
            elif app.chef1.animationName == 'down':
                objX, objY = app.chef1.cx, app.chef1.cy+app.boxSize/4
            elif app.chef1.animationName == 'right':
                objX, objY = app.chef1.cx+app.boxSize/4, app.chef1.cy
            elif app.chef1.animationName == 'left':
                objX, objY = app.chef1.cx-app.boxSize/4, app.chef1.cy
            else:
                objX, objY = app.chef1.cx, app.chef1.cy
            #draws plate if chef is holding plate or chef is holding ingredient with plate
            if isinstance(app.chef1.holding, Plate):
                canvas.create_image(objX, objY, image=ImageTk.PhotoImage(app.chef1.holding.image))
            elif app.chef1.holding.plate != None:
                canvas.create_image(objX, objY, image=ImageTk.PhotoImage(app.chef1.holding.plate.image))
            
            if isinstance(app.chef1.holding, Burger):
                if app.chef1.holding.imageList: #if chef has veggies/meat, no bread
                    for ingred in app.chef1.holding.ingredients:
                        canvas.create_image(objX, objY, image=ImageTk.PhotoImage(ingred.image))
                else: #if chef has bread -> special burger images
                    canvas.create_image(objX, objY, image=ImageTk.PhotoImage(app.chef1.holding.image))
            else:
                canvas.create_image(objX, objY, image=ImageTk.PhotoImage(app.chef1.holding.image))
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
                if counter.ingredient.imageList:
                    for ingred in counter.ingredient.ingredients:
                        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(ingred.image))
                else:
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(counter.ingredient.image))
            else:
                canvas.create_image(cx, cy, image=ImageTk.PhotoImage(counter.ingredient.image))
    #draws plates on counters
    for counter in app.plateCounters:
        cx, cy = counter.x0+app.boxSize/2, counter.y0+app.boxSize/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(counter.ingredient.image))
    #draws rat
    if app.rat != None:
        if app.rat.animation != [] and app.rat.pathPlanner.target != None: #draws rat moving animation
            i = app.rat.counterDict[app.rat.animationName]
            canvas.create_image(app.rat.x+app.boxSize/2, app.rat.y+app.boxSize/2, image=ImageTk.PhotoImage(app.rat.animation[i]))
        else:
            canvas.create_image(app.rat.x+app.boxSize/2, app.rat.y+app.boxSize/2, image=ImageTk.PhotoImage(app.rat.image))
    #draws game over screen
    if app.gameOver:
        canvas.create_rectangle(app.width/5, app.height/3, app.width*(4/5), app.height*(2/3), fill='light blue')
        canvas.create_text(app.width/2, 2/5*app.height, text="Time's Up!", font='Arial 20 bold')
        if app.score >= app.maxScore/2:
            outcome = 'win!'
        else:
            outcome = 'lose.'
        canvas.create_text(app.width/2, 2.5/5*app.height, text=f'Your score was {app.score}. You {outcome}', font='Arial 20 bold')
        canvas.create_text(app.width/2, 3/5*app.height, text='Press ENTER to play again', font='Arial 20 bold')
################################################################################

runApp(width=720, height=528+32*3)