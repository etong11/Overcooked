import random

class Rat:
    def __init__(self, app, target, targetX, targetY):
        self.bounds = [app.counterX0, app.counterY0, app.counterX1, app.counterY1]
        self.x = random.randint(self.bounds[0], self.bounds[2]+1)
        self.y = random.randint(self.bounds[1], self.bounds[3]+1)
        self.target = target #targets a food
        self.targetX, self.targetY = targetX, targetY
        self.dead = False
        self.hasFood = False

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
            self.moveRat()
            if self.x == self.targetX and self.y == self.targetY:
                self.hasFood = True
    
    def moveRat(self):
        #change complexity of path
        #move towards target and grab food
        if self.x < self.targetX:
            self.x += 1
        elif self.x > self.targetX:
            self.x -= 1
        if self.y < self.targetY:
            self.y += 1
        elif self.y > self.targetY:
            self.y -= 1