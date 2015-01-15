

from point import *
from orientation import *

#MAP LOCATIONS:

#ROOM 2:

#Position = (x, y) = (-4.41, 3.57)
#Orientation = (z, w) = (0.98, 0.19)

# Goal points

ROOM1 = (Point(-4.31, 0.22), Orientation(0.990, 0.144))
ROOM2 = (Point(-3.29, 3.87), Orientation(0.982, 0.189))
ROOM3 = (Point(-3.59, 7.07), Orientation(0.954, 0.301))
KITCHEN1 = (Point(0, -0.83), Orientation(-0.06, 0.998))
KITCHEN2 = (Point(0.05, -0.12), Orientation(-0.239, 0.971))
AFTER_PR2 = (Point(0.03, 0.57), Orientation(1, 0))

# Waypoints

PR2 = (Point(1.1, -0.49), Orientation(0.801, 0.598))

ROOM1_ENTRANCE = (Point(-2, 0.05), Orientation(1, 0))
ROOM1_EXIT = (Point(-2, -0.44), Orientation(0, 1))
ROOM1_HALLWAY = (Point(-1.33, 0.16), Orientation(-0.281, 0.960))
#ROOM1_SPECIAL = (Point(), Orientation())

ROOM2_ENTRANCE = (Point(-1.88, 3.60), Orientation(1, 0))
ROOM2_EXIT = (Point(-1.95, 2.57), Orientation(-0.646, 0.763))
ROOM2_HALLWAY = (Point(-1.35, 3.32), Orientation(0.702, 0.712))

ROOM3_ENTRANCE = (Point(-2.11, 6.67), Orientation(1, 0))
ROOM3_EXIT = (Point(-1.97, 5.53), Orientation(-0.640, 0.769))
ROOM3_HALLWAY = (Point(-1.21, 6.02), Orientation(0.828, 0.560)) #x,y = -1.53, 6.77


# PATHS
PATH_WAYPOSES = {}
PATH_WAYPOSES[("room1", "room2")] = [ROOM1_EXIT, ROOM1_HALLWAY, ROOM2_HALLWAY, ROOM2_ENTRANCE, ROOM2]
PATH_WAYPOSES[("room1", "room3")] = [ROOM1_EXIT, ROOM1_HALLWAY, ROOM2_HALLWAY, ROOM3_HALLWAY, ROOM3_ENTRANCE, ROOM3]
PATH_WAYPOSES[("room1", "kitchen1")] = [ROOM1_EXIT, ROOM1_HALLWAY, KITCHEN1]
PATH_WAYPOSES[("room1", "kitchen2")] = [ROOM1_EXIT, ROOM1_HALLWAY, KITCHEN2]

PATH_WAYPOSES[("room2", "room1")] = [ROOM2_EXIT, ROOM1_ENTRANCE, ROOM1]
PATH_WAYPOSES[("room2", "room3")] = [ROOM2_EXIT, ROOM2_HALLWAY, ROOM3_HALLWAY, ROOM3_ENTRANCE, ROOM3]
PATH_WAYPOSES[("room2", "kitchen1")] = [ROOM2_EXIT, ROOM1_ENTRANCE, ROOM1_HALLWAY, KITCHEN1]
PATH_WAYPOSES[("room2", "kitchen2")] = [ROOM2_EXIT, ROOM1_ENTRANCE, ROOM1_HALLWAY, KITCHEN2]

PATH_WAYPOSES[("room3", "room1")] = [ROOM3_EXIT, ROOM2_ENTRANCE, ROOM2_EXIT, ROOM1_ENTRANCE, ROOM1]
PATH_WAYPOSES[("room3", "room2")] = [ROOM3_EXIT, ROOM2_ENTRANCE, ROOM2]
PATH_WAYPOSES[("room3", "kitchen1")] = [ROOM3_EXIT, ROOM2_ENTRANCE, ROOM2_EXIT, ROOM1_ENTRANCE, ROOM1_HALLWAY, KITCHEN1]
PATH_WAYPOSES[("room3", "kitchen2")] = [ROOM3_EXIT, ROOM2_ENTRANCE, ROOM2_EXIT, ROOM1_ENTRANCE, ROOM1_HALLWAY, KITCHEN2]

PATH_WAYPOSES[("kitchen", "after_pr2")] = [PR2, AFTER_PR2]
PATH_WAYPOSES[("kitchen", "room1")] = [ROOM1_HALLWAY, ROOM1_ENTRANCE, ROOM1]
PATH_WAYPOSES[("kitchen", "room2")] = [ROOM1_HALLWAY, ROOM2_HALLWAY, ROOM2_ENTRANCE, ROOM2]
PATH_WAYPOSES[("kitchen", "room3")] = [ROOM1_HALLWAY, ROOM2_HALLWAY, ROOM3_HALLWAY, ROOM3_ENTRANCE, ROOM3]

PATH_WAYPOSES[("pr2", "after_pr2")] = [AFTER_PR2]

PATH_WAYPOSES[("after_pr2", "room1")] = [ROOM1_HALLWAY, ROOM1_ENTRANCE, ROOM1]
PATH_WAYPOSES[("after_pr2", "room2")] = [ROOM1_HALLWAY, ROOM2_HALLWAY, ROOM2_ENTRANCE, ROOM2]
PATH_WAYPOSES[("after_pr2", "room3")] = [ROOM1_HALLWAY, ROOM2_HALLWAY, ROOM3_HALLWAY, ROOM3_ENTRANCE, ROOM3]


#ROOM1_POSITION = {"donatello" : Point(0, 0), "leonardo" : Point(0, 0)}
#ROOM1_ORIENTATION = {"donatello" : Orientation(0, 1), "leonardo" : Orientation(0, 1)}

#ROOM2_POSITION = {"donatello" : (0, 0), "leonardo" : (0, 0)}
#ROOM2_ORIENTATION = {"donatello" : Orientation(0, 1), "leonardo" : Orientation(0, 1)}

#KITCHEN_POSITION = {"donatello" : (1.79, -0.57), "leonardo" : (1.25, -1.03)}
#KITCHEN_ORIENTATION = {"donatello" : Orientation(0.9, 0.44), "leonardo" : Orientation(0.78, 0.63)}

#PR2_POSITION = {"donatello" : (0.83, 0.44), "leonardo" : (0, 0)}
#PR2_ORIENTATION = {"donatello" : Orientation(-0.63, 0.77), "leonardo" : Orientation(0, 1)}



