from cmu_112_graphics import *
import cs112_f22_week10_linter
import decimal
import chef
import ingredient

#Overchefed

#################################################
# Helper functions from 
# https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#RecommendedFunctions
#################################################
def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
#################################################

def appStarted(app):
    app.chef1 = chef.Chef(1)
    #center coordinates of the chef
    app.chef1X, app.chef1Y = app.width/2, app.height/2
    app.chef1R = 20 #radius of chef
    app.counterX0, app.counterY0 = app.width/5, app.height/5
    app.counterX1, app.counterY1 = app.width*(4/5), app.height*(4/5)
    app.boxSize = (app.counterY1-app.counterY0)/5
    app.box1X0, app.box1Y0 = app.counterX0-app.width/10, app.counterY0+app.boxSize
    app.box1X1, app.box1Y1 = app.counterX0, app.counterY0+2*app.boxSize
    app.box2Y1 = app.box1Y1+app.boxSize
    app.box3Y1 = app.box2Y1+app.boxSize

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
        if inRange(app.chef1, app.box):
            pass #pick up or drop
    elif event.key == 'Tab':
        pass #chop
    #dash?

def timerFired(app):
    pass

def moveChef(app, dx, dy):
    newX, newY = app.chef1X + dx*5, app.chef1Y + dy*5
    if (app.counterX0 < (newX - app.chef1R) and 
        app.counterX1 > (newX + app.chef1R) and 
        app.counterY0 < (newY - app.chef1R) and
        app.counterY1 > (newY + app.chef1R)):
        app.chef1X, app.chef1Y = newX, newY

def redrawAll(app, canvas):
    #draws counter
    canvas.create_rectangle(app.counterX0, app.counterY0, app.counterX1, app.counterY1)
    canvas.create_rectangle(app.counterX0-app.width/10, app.counterY0-app.width/10, 
                app.counterX1+app.width/10, app.counterY1+app.width/10)
    #draws interfaces on counter
    canvas.create_rectangle(app.box1X0, app.box1Y0, app.box1X1, app.box1Y1)
    canvas.create_rectangle(app.box1X0, app.box1Y1, app.box1X1, app.box2Y1)
    canvas.create_rectangle(app.box1X0, app.box2Y1, app.box1X1, app.box3Y1)
    #draws chef
    canvas.create_oval(app.chef1X-app.chef1R, app.chef1Y-app.chef1R,
                app.chef1X+app.chef1R, app.chef1Y+app.chef1R)

    

runApp(width=800, height=600)