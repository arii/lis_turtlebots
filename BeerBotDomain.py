#!/usr/bin/env python
# Author: Ariel Anders
# Domain classes for beerbots
import numpy as np  

class AGENTS:
    DONATELLO, LEONARDO = range(2)

class ACTIONS:
    ROOOM_1, ROOM_2, ROOM_3, KITCHEN, GET_DRINK = range(5)

class ObservationType:
    num= 0
    def num_observations(self):
        return self.num

class LOC(ObservationType):
    num = 4
    R1, R2, R3, KITCHEN= range(4)


class ORDERS(ObservationType):
    num = 2

class HOLD(ObservationType):
    num = 2

class PR2:
    SOMEONE, INHAND, NOTHING = range(3)
    num = 3

class Observations:
    def __init__(self):
        self.observation_types =  [LOC(), ORDERS(), HOLD(), PR2()]
        self.total_obs = 1
        for obs_type in self.observation_types:
            self.total_obs *= obs_type.num
        print "total_obs = %s " % self.total_obs
        self.lookup_dot_vect = np.array([12, 6, 3, 1])

    def lookup(self, obs):
        idx = np.dot(self.lookup_dot_vect,  np.array(obs) )
        assert (idx >= 0 and idx < self.total_obs)
        return idx

if __name__=="__main__":
    obs = Observations()
    for i in range(4):
        for j in range( 2):
            for k in range(2):
                for l in range(3):
                    o = [i,j,k,l]
                    print "observation  %d =  %s" %(obs.lookup(o), o)



