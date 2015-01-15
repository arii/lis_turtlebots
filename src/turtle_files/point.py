import math

class Point(object):
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, p):
        if (p == None):
            return False
        return (self.x == p.x) and (self.y == p.y) and (self.z == p.z)

    def __ne__(self, p):
        if (p == None):
            return True
        return (self.x != p.x) or (self.y != p.y) or (self.z != p.z)

    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y, self.z + p.z)

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y, self.z - p.z)

    def __str__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

    __repr__ = __str__

    def distance(self, p):
        return math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2 + (self.z - p.z) ** 2)


