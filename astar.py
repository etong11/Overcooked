import decimal

# Helper functions from 
# https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#RecommendedFunctions
################################################################################
def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
################################################################################

# A PathPlan object creates a path when given a starting and ending point (target)
class PathPlan:
    #Constants
    rows, cols = 8, 13 #number of 16*3x16*3 boxes (walkable space + countertops)

    def __init__(self, app, startX, startY, target):
        self.bounds = [app.counterX0, app.counterY0, app.counterX1, app.counterY1]
        self.startX, self.startY = startX, startY
        self.startRow, self.startCol = self.convertToRowCol(startX, startY)
        self.target = target #targets a counter with food on it
        self.obstacles = app.obstacles
        self.resetPath()
        self.generatePath(target, self.startRow, self.startCol)

    def resetPath(self):
        self.path = None
        self.visited = []
        self.unvisited = []
        self.moveTarget = (-1,-1)

    #converts the coordinates used in the board to pixels on actual map
    @staticmethod
    def convertToPixels(row, col):
        x, y = (col+1)*16*3, (row+4)*16*3
        return x, y
    
    @staticmethod
    def convertToRowCol(x, y):
        row, col = int(y//(16*3)-4), int(x//(16*3)-1)
        return row, col

    ############################################################################
    #A* algorithm logic taken from https://isaaccomputerscience.org/concepts/dsa_search_a_star?examBoard=all&stage=all
    #Under section "A* algorithm - step-by-step
    def generatePath(self, target, startRow, startCol):
        self.target = target #targets a counter with food on it; changes to a new target if different
        self.targetRow, self.targetCol = PathPlan.convertToRowCol(target.x0, target.y0)
        self.targetX, self.targetY = PathPlan.convertToPixels(self.targetRow, self.targetCol)

        self.start = (startRow, startCol)
        self.end = (self.targetRow, self.targetCol)
        startNode = Node(self.start, 0, self.findHScore(self.start), None)
        self.unvisited = [startNode]
        for row in range(PathPlan.rows):
            for col in range(PathPlan.cols):
                coords = (row, col)
                node = Node(coords, 10**5, 10**5, None)
                self.unvisited.append(node)
        self.visited = []
        foundPath = self.findPath()
        if foundPath:
            endNode = self.findNode(self.end)
            self.path = self.makePath(endNode, [endNode])[::-1]
        else:
            self.path = None

    def findNeighbors(self, node):
        neighbors = []
        row, col = node.node[0], node.node[1]
        for loc in [(0,1), (0,-1), (1,0), (-1,0)]:
            drow, dcol = loc[0], loc[1]
            neighbor = (row+drow, col+dcol)
            if neighbor in self.obstacles:
                continue
            if 0 <= neighbor[0] < PathPlan.rows and 0 <= neighbor[1] < PathPlan.cols:
                isVisited = False
                for node in self.visited:
                    name = node.node
                    if name == neighbor:
                        isVisited = True
                if not isVisited:
                    neighbors.append(neighbor)
        return neighbors

    #given coord, find name in self.unvisited
    def findNode(self, coord):
        for node in self.unvisited:
            name = node.node
            if name == coord:
                return node
        return None

    def findFScore(self, node):
        row, col = node.node[0], node.node[1]
        #Using forumla f(n) = g(n) + h(n)
        g = node.g
        #Uses Manhattan heuristic to calculate h, formula taken from https://brilliant.org/wiki/a-star-search/
        h = abs(row-self.end[0]) + abs(col-self.end[1])
        f = g + h
        return f

    #Uses Manhattan heuristic to calculate h, formula taken from https://brilliant.org/wiki/a-star-search/
    def findHScore(self, coord):
        x, y = coord[0], coord[1]
        return abs(x-self.end[0]) + abs(y-self.end[1])
    
    def findMinFScore(self):
        minScore = 10**10
        minNode = None
        for node in self.unvisited:
            thisScore = self.findFScore(node)
            if thisScore < minScore:
                minScore = thisScore
                minNode = node
        return minNode

    #Uses A*
    def findPath(self):
        currentNode = self.findMinFScore()
        if currentNode.node == self.end:
            return True
        else:
            neighbors = self.findNeighbors(currentNode)
            for neighbor in neighbors:
                node = self.findNode(neighbor)
                newG = currentNode.g + 1
                if newG < node.g:
                    node.g = newG
                    node.parent = currentNode
                    node.f = self.findFScore(node)
            self.visited.append(currentNode)
            self.unvisited.remove(currentNode)
            return self.findPath()

    #After all nodes have been visited, makes list of path with nodes as elements using backtracking
    def makePath(self, node, path):
        if node.parent == None:
            path.append(node)
            return path
        else:
            path.append(node.parent)
            return self.makePath(node.parent, path)
    ############################################################################

    def moveToTarget(self, movingObj):
        atTarget = False
        if self.path != None and len(self.path) >= 0:
            if self.moveTarget == (-1,-1):
                nextRow, nextCol = self.path[0].node[0], self.path[0].node[1]
                self.moveTarget = PathPlan.convertToPixels(nextRow, nextCol)
                self.start = self.path.pop(0)
            else:
                atTarget = self.move(movingObj)
        return atTarget

            # if movingObj.x > self.targetX:
            #     if not self.isFlipped:
            #         self.isFlipped = True
            #         self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            # elif movingObj.x < self.targetX:
            #     if self.isFlipped:
            #         self.isFlipped = False
            #         self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            # elif almostEqual(movingObj.x,self.targetX) and almostEqual(movingObj.y,targetY):
            #     self.hasFood = True
                    
    def move(self, movingObj):
        if movingObj.x > self.moveTarget[0]:
            movingObj.x -= 16*3/4
            movingObj.facing = 'left'
        elif movingObj.x < self.moveTarget[0]:
            movingObj.x += 16*3/4
            movingObj.facing = 'right'
        if movingObj.y > self.moveTarget[1]:
            movingObj.y -= 16*3/4
            movingObj.facing = 'up'
        elif movingObj.y < self.moveTarget[1]:
            movingObj.y += 16*3/4
            movingObj.facing = 'down'

        if almostEqual(movingObj.x, self.moveTarget[0]) and almostEqual(movingObj.y, self.moveTarget[1]):
            if almostEqual(movingObj.x, self.targetX) and almostEqual(movingObj.y, self.targetY):
                return True
            else:
                self.moveTarget = (-1, -1)
                return False

#Node class - Idea to use a class came from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#To determine what parameters are passed, used logic from https://isaaccomputerscience.org/concepts/dsa_search_a_star?examBoard=all&stage=all
#Under section "A* algorithm - step-by-step
class Node():
    def __init__(self, coord, g, f, parent):
        self.node = coord
        self.g = g
        self.f = f
        self.parent = parent