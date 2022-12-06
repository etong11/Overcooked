class Astar:
    def __init__(self, app):
        self.bounds = [app.counterX0, app.counterY0, app.counterX1, app.counterY1]
        self.rows, self.cols = 8, 13 #number of 16*3x16*3 boxes (walkable space + countertops)
        pass
