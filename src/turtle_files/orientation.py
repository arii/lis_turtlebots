

import math

class Orientation:
    def __init__(self, z, w, x = 0, y = 0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    # Gets the yaw angle from the quaternion describing the object's position
    def getTheta(self):
        w = self.w
        z = self.z
        mag = math.sqrt(w ** 2 + z ** 2)
        w /= mag
        z /= mag
        return math.atan2(2 * w * z, w ** 2 - z ** 2) #- math.pi / 2
