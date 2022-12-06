import decimal
from cmu_112_graphics import *

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

############################################################################
#A* algorithm logic taken from https://isaaccomputerscience.org/concepts/dsa_search_a_star?examBoard=all&stage=all
#Under section "A* algorithm - step-by-step
class Astar:
    def __init__(self, target, startY, startX):
        self.rows, self.cols = 8, 13 #change to not include counters (target is cell in front of food)
        self.generatePath(target, startY, startX)
        self.moveX, self.moveY = self.convertToPixels(self.y, self.x)

    def generatePath(self, target, startY, startX):
        self.target = target #targets a counter with food on it
        self.targetX, self.targetY = self.convertToListCoords(target.x0, target.y0)
        self.start = (startY, startX)
        self.end = (self.targetY, self.targetX)
        # print('target', self.targetY, self.targetX)
        # print('rat', self.x, self.y)
        print('start', self.start)
        print('end', self.end)
        startNode = Node(self.start, 0, self.findHScore(self.start), None)
        # print('hscore', self.findHScore)
        self.unvisited = [startNode]
        for row in range(self.rows):
            for col in range(self.cols):
                coords = (row, col)
                node = Node(coords, 10**5, 10**5, None)
                self.unvisited.append(node)
        self.visited = []
        # print('unvisited, visited', self.unvisited, self.visited)
        foundPath = self.findPath()
        if foundPath:
            endNode = self.findNode(self.end)
            self.path = self.makePath(endNode, [endNode])[::-1]
        else:
            self.path = None
        # print('path', self.path)

    def resetPath(self):
        self.path = None
        self.visited = []
        self.unvisited = []
        # self.moveX, self.moveY = roundHalfUp(self.moveX/(16*3))*16*3, roundHalfUp(self.moveY//(16*3))*16*3
        self.moveTarget = (-1,-1)

    def findNeighbors(self, node):
        neighbors = []
        x, y = node.node[0], node.node[1]
        for loc in [(0,1), (0,-1), (1,0), (-1,0)]:
            drow, dcol = loc[0], loc[1]
            neighbor = (x+drow, y+dcol)
            if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols:
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
        x, y = node.node[0], node.node[1]
        #Using forumla f(n) = g(n) + h(n)
        g = node.g
        #Uses Manhattan heuristic to calculate h, formula taken from https://brilliant.org/wiki/a-star-search/
        h = abs(x-self.end[0]) + abs(y-self.end[1])
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
            # print('node', thisScore)
            # print('fscore',thisScore)
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
    
    def moveToTarget(self, obj, reachedTarget):
        if not obj.dead and not reachedTarget:
            if self.path != None and len(self.path) >= 0:
                if self.moveTarget == (-1,-1):
                    drow, dcol = self.path[0].node[0], self.path[0].node[1]
                    self.moveTarget = self.convertToPixels(drow, dcol)
                    self.start = self.path.pop(0)
                # print('target', self.convertToPixels(self.targetY, self.targetX))
                    
                else:
                    self.move()                
                
                targetPixelX, targetPixelY = self.convertToPixels(self.targetY, self.targetX)
                # print('move', self.moveX, self.moveY)
                # print('target', targetPixelX, targetPixelY)
                # print('path', self.path)
                # print('moveTarget', self.moveTarget)
                if self.moveX > targetPixelX:
                    if not obj.isFlipped:
                        obj.isFlipped = True
                        obj.image = obj.image.transpose(Image.FLIP_LEFT_RIGHT)
                elif self.moveX < targetPixelX:
                    if obj.isFlipped:
                        obj.isFlipped = False
                        obj.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
                elif almostEqual(self.moveX,targetPixelX) and almostEqual(self.moveY,targetPixelY):
                    reachedTarget = True
                    # print('rat has food', self.hasFood)
                
    def move(self):
        if self.moveX > self.moveTarget[0]:
            self.moveX -= 16*3/4
        elif self.moveX < self.moveTarget[0]:
            self.moveX += 16*3/4
        if self.moveY > self.moveTarget[1]:
            self.moveY -= 16*3/4
        elif self.moveY < self.moveTarget[1]:
            self.moveY += 16*3/4
            # self.moveX, self.moveY = self.moveTarget[0], self.moveTarget[1]
        if almostEqual(self.moveX, self.moveTarget[0]) and almostEqual(self.moveY, self.moveTarget[1]):
            self.moveTarget = (-1, -1)

    @staticmethod
    #converts the coordinates used in the board to pixels on actual map
    def convertToPixels(row, col):
        x, y = (col+1)*16*3, (row+4)*16*3
        return x, y
    @staticmethod
    def convertToListCoords(x, y):
        return int(x//(16*3)-1), int(y//(16*3)-4) #cols, rows
        
#Node class - Idea to use a class came from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#To determine what parameters are passed, used logic from https://isaaccomputerscience.org/concepts/dsa_search_a_star?examBoard=all&stage=all
#Under section "A* algorithm - step-by-step
class Node():
    def __init__(self, coord, g, f, parent):
        self.node = coord
        self.g = g
        self.f = f
        self.parent = parent
