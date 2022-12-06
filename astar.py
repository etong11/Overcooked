# A PathPlan object creates a path when given a starting and ending point (target)
class PathPlan:
    #Constants
    rows, cols = 8, 13 #number of 16*3x16*3 boxes (walkable space + countertops)

    def __init__(self, app, startX, startY, target):
        self.bounds = [app.counterX0, app.counterY0, app.counterX1, app.counterY1]
        pass