#!/usr/bin/env python
# Author: Ariel Anders
# Controller class for beerbots
from BeerBotDomain import Observations
def import_map(filename):
    mapping = {}
     
    with open(filename, 'r') as f:
        for line in f:
            data = line.split(',')
            lookup_arr= data[:-1]
            try:
                result = int(data[-1])
            except:
                continue
            lookup_str = ("_").join(lookup_arr)
            mapping[lookup_str] =  result
    return mapping

def gen_lookup_str(array):
    str_array = ['%s' % val for val in array]
    return ("_").join(str_array)

class Controller:
    def __init__(self, agent, node):
        self.agent = agent
        self.node = node
        self.act = import_map("planner_files/actMapMealy.csv")
        self.trans = import_map("planner_files/TransMap.csv")
        self.observations = Observations()
    
    def action(self, observation):
        obs_num = self.observations.lookup(observation)
        lookup_str =gen_lookup_str([self.agent, self.node, obs_num])
        try:
            action = self.act[lookup_str]
        except:
            print "could not find action from lookup str %s " % lookup_str
            raise Exception
        print "action %s : %s" % (lookup_str, action)
        return action

    def transition(self, observation, action):
        obs_num = self.observations.lookup(observation)
        lookup_str =gen_lookup_str([self.agent, self.node, obs_num, action])
        try:
            node = self.trans[lookup_str]
        except:
            print "could not find transition from lookup str %s " % lookup_str
            raise Exception
        print "transition %s : %s" % (lookup_str, node)
        self.node = node
        return node



if __name__=="__main__":
    ctrl = Controller(0, 0)
    
    for i in range(4):
        for j in range( 2):
            for k in range(2):
                for l in range(3):
                    o = [i,j,k,l]
                    ctrl.action(o)
                    for action in range(5):
                        ctrl.transition(o, action)

