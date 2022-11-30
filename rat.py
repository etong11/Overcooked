import random
import decimal

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

class Rat:
    #change so that x,y are cells
    def __init__(self, app, target):
        self.bounds = [app.counterX0, app.counterY0, app.counterX1, app.counterY1]
        self.rows, self.cols = 8, 13 #change to not include counters (target is cell in front of food)
        self.x, self.y = random.randint(0, self.cols-1), random.randint(0, self.rows-1)
        self.target = target #targets a counter with food on it
        self.targetX, self.targetY = int(target.x0//(16*3)-1), int(target.y0//(16*3)-4) #cols, rows
        self.dead = False
        self.hasFood = False
        print('target', self.targetX, self.targetY)
        print('rat', self.x, self.y)
        self.moveX, self.moveY = self.convertToPixels(self.x, self.y)

        #code copied from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2 
        # but modified to fit game
        ##############################################################
        board = [[0]*self.cols for row in range(self.rows)]

        self.start = (self.y, self.x)
        end = (self.targetY, self.targetX)

        self.path = astar(board, self.start, end)
        print('new path', self.path)
        ################################################################

    def __repr__(self):
        info = ''
        if self.dead:
            info += '(dead)'
        if self.hasFood:
            info += 'hasFood'
        info += f'target:{self.target}'
        return info
    
    def grabFood(self):
        #code in speed of rat?
        if not self.dead and not self.hasFood:
            if self.path != None and len(self.path) > 0:
                drow, dcol = self.path[0][0], self.path[0][1]
                self.moveX, self.moveY = self.convertToPixels(drow, dcol)
                self.start = self.path.pop(0)
                print('move', self.moveX, self.moveY)
                print('target', self.convertToPixels(self.targetY, self.targetX))
                targetPixelX, targetPixelY = self.convertToPixels(self.targetY, self.targetX)
                if almostEqual(self.moveX,targetPixelX) and almostEqual(self.moveY,targetPixelY):
                    self.hasFood = True
                    print('rat has food', self.hasFood)

    #converts the coordinates used in the board to pixels on actual map
    def convertToPixels(self, row, col):
        x, y = (col+1)*16*3, (row+4)*16*3
        return x, y

    #to implement: if move food, change target to next food on counter

#Code below copied from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)