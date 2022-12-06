import random
import decimal
import copy
from cmu_112_graphics import *
from astar import *

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

class Rat:
    #target is a counter with an ingredient (which is what is the target)
    def __init__(self, app, target):
        self.col, self.row = random.randint(0, PathPlan.cols-1), random.randint(0, PathPlan.rows-1)
        
        self.dead = False
        self.hasFood = False
        
        self.x, self.y = self.convertToPixels(self.row, self.col)
        self.moveTarget = (-1,-1)
        #Rat image credit: from https://www.pixilart.com/draw/big-ear-rat-9b1f2c785eb607a
        self.image = app.loadImage('rat.png')
        self.isFlipped = False

        # self.pathPlanner = PathPlan(app, self.x, self.y)
        self.generatePath(target, self.row, self.col)

    ############################################################################
    #A* algorithm logic taken from https://isaaccomputerscience.org/concepts/dsa_search_a_star?examBoard=all&stage=all
    #Under section "A* algorithm - step-by-step
    def generatePath(self, target, startRow, startCol):
        self.target = target #targets a counter with food on it
        self.targetRow, self.targetCol = self.convertToRowCol(target.x0, target.y0)
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
    
    def resetPath(self):
        self.path = None
        self.visited = []
        self.unvisited = []
        self.moveTarget = (-1,-1)

    def findNeighbors(self, node):
        neighbors = []
        row, col = node.node[0], node.node[1]
        for loc in [(0,1), (0,-1), (1,0), (-1,0)]:
            drow, dcol = loc[0], loc[1]
            neighbor = (row+drow, col+dcol)
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
    
    def grabFood(self):
        if not self.dead and not self.hasFood:
            if self.path != None and len(self.path) >= 0:
                if self.moveTarget == (-1,-1):
                    drow, dcol = self.path[0].node[0], self.path[0].node[1]
                    print(drow, dcol)
                    self.moveTarget = self.convertToPixels(drow, dcol)
                    self.start = self.path.pop(0)
                else:
                    self.move()                
                targetX, targetY = self.convertToPixels(self.targetRow, self.targetCol)
                if self.x > targetX:
                    if not self.isFlipped:
                        self.isFlipped = True
                        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
                elif self.x < targetX:
                    if self.isFlipped:
                        self.isFlipped = False
                        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
                elif almostEqual(self.x,targetX) and almostEqual(self.y,targetY):
                    self.hasFood = True
                
    def move(self):
        if self.x > self.moveTarget[0]:
            self.x -= 16*3/4
        elif self.x < self.moveTarget[0]:
            self.x += 16*3/4
        if self.y > self.moveTarget[1]:
            self.y -= 16*3/4
        elif self.y < self.moveTarget[1]:
            self.y += 16*3/4
        if almostEqual(self.x, self.moveTarget[0]) and almostEqual(self.y, self.moveTarget[1]):
            self.moveTarget = (-1, -1)


    #converts the coordinates used in the board to pixels on actual map
    def convertToPixels(self, row, col):
        x, y = (col+1)*16*3, (row+4)*16*3
        return x, y
    
    def convertToRowCol(self, x, y):
        row, col = int(y//(16*3)-4), int(x//(16*3)-1)
        return row, col

#Node class - Idea to use a class came from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#To determine what parameters are passed, used logic from https://isaaccomputerscience.org/concepts/dsa_search_a_star?examBoard=all&stage=all
#Under section "A* algorithm - step-by-step
class Node():
    def __init__(self, coord, g, f, parent):
        self.node = coord
        self.g = g
        self.f = f
        self.parent = parent
