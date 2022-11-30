from cmu_112_graphics import *
import cs112_f22_week10_linter
import decimal
import copy

from ingredient import *
from chef import *
from box import *
from rat import *

#Overchefed
#images drawn by me (except chef image - credit to Amy Xu, except rat image - https://www.pixilart.com/draw/big-ear-rat-9b1f2c785eb607a

def appStarted(app):
    #images
    app.background = app.loadImage('background.png')
    # app.background = app.scaleImage(app.background, 3)
    # print(app.background.size)
    app.chef = app.loadImage('chef.png')
    # print(app.chef.size)
    app.ratImage = app.loadImage('rat.png')

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
    # app.plate = Plate(None, app)
    # app.plate2, app.plate3 = copy.copy(app.plate), copy.copy(app.plate)
    # app.plates = [app.plate, app.plate2, app.plate3]
    # for plateIndex in range(len(app.plates)):
    #     app.usedCounters.append(Counter(app.width-16*3*(3+plateIndex), app.counterY1, app.boxSize))

    # app.dirtyPlates = []
    app.time = 0
    app.timerDelay = 1000
    app.paused = False
    app.score = 0

    app.rat = None
    app.gameOver = False

def keyPressed(app, event):
    if app.gameOver:
        return
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
                counter = app.usedCounters[count]
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
                        app.chef1.serve(order)
                        app.score += 1
            # elif (app.sink.withinBox(app.chef1) and isinstance(app.chef1.holding, Plate)
            #         and not app.chef1.holding.clean):
            #     app.chef1.holding.clean = True
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
                            if app.chef1.holding not in counterItem.ingredients:
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
    if app.gameOver:
        return
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
    if 0 <= app.time%10 <= 2 and app.usedCounters != [] and app.rat == None:
        spawnRat(app)
    if app.rat != None:
        #increase speed
        app.rat.grabFood()
        if app.rat.hasFood:
            print('has food')
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
    # if app.time == 1000:
    #     app.time = 0
    
    if app.time == 125:
        app.gameOver = True
    # print('counter', end=' ')
    # for counter in app.usedCounters:
    #     print(counter.ingredient, end='WHY')

def moveChef(app, dx, dy):
    #moves by 1 pixel which = 3
    newX, newY = app.chef1.cx + 6*dx, app.chef1.cy + 6*dy
    if (app.counterX0 <= (newX - app.chef1.r) and 
        app.counterX1 >= (newX + app.chef1.r) and 
        app.counterY0 <= (newY - app.chef1.r) and
        app.counterY1 >= (newY + app.chef1.r)):
        app.chef1.cx, app.chef1.cy = newX, newY

#spawns in a rat with a given target
def spawnRat(app):
    target = app.usedCounters[0]
    app.rat = Rat(app, target)

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
    canvas.create_text(app.width-16*3, app.height-16*3/2, text=f'Time: {app.time}', fill='white', font='Arial 13 bold')
    canvas.create_text(app.width/2, app.height-16*3/2, text=f'Holding: {app.chef1.holding}', fill='white', font='Arial 9 bold')
    #draw order box
    # canvas.create_rectangle(app.orderBox.x0, app.orderBox.y0, app.orderBox.x1, app.orderBox.y1)
    # canvas.create_text(app.orderBox.x0+app.boxSize/2, app.orderBox.y0+app.boxSize/2, text='orders')
    #draws plates
    # canvas.create_oval(app.plate.x-app.plate.r, app.plate.y-app.plate.r, app.plate.x+app.plate.r, app.plate.y+app.plate.r)
    # canvas.create_text(app.plate.x, app.plate.y, text='clean plates')
    #draws chef
    # canvas.create_oval(app.chef1.cx-app.chef1.r, app.chef1.cy-app.chef1.r,
    #             app.chef1.cx+app.chef1.r, app.chef1.cy+app.chef1.r)
    #shows what is on the counters
    # for ingred in app.placedIngred:
    #     ingredX, ingredY = ingred[1], ingred[2]
    #     name = ingred[0]
    #     canvas.create_text(ingredX, ingredY, text=name)
    for counter in app.usedCounters:
        cx, cy = counter.x0+app.boxSize/2, counter.y0+app.boxSize/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(counter.ingredient.image))
        canvas.create_text(counter.x0+24, counter.y0+24, text=str(counter.ingredient), font='Arial 9 bold', fill='white')
    #draws dirty plates
    # for plate in app.dirtyPlates:
    #     canvas.create_oval(plate.x-plate.r, plate.y-plate.r, plate.x+plate.r, plate.y+plate.r)
    #     canvas.create_text(plate.x, plate.y, text='dirty plates')
    #draw rat
    if app.rat != None and not app.rat.dead:
        # r = 16*3/2
        canvas.create_image(app.rat.moveX+app.boxSize/2, app.rat.moveY+app.boxSize/2, image=ImageTk.PhotoImage(app.ratImage))
        # canvas.create_oval(app.rat.moveX, app.rat.moveY, app.rat.moveX+app.boxSize, app.rat.moveY+app.boxSize)
        # canvas.create_text(app.rat.moveX, app.rat.moveY, text=app.rat)
    
    # canvas.create_line(16*3, 0, 16*3, 600, fill='red')
    # canvas.create_line(32*3, 0, 32*3, 600, fill='red')
    # canvas.create_line(0, 48*3, 700, 48*3, fill='red')

    if app.gameOver:
        canvas.create_text(app.width/2, app.height/2, text='game over', font='Arial 20 bold')


runApp(width=720, height=528+32*3)