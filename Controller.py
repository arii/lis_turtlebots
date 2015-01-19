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

class Agent:
    def __init__(self, num=0):
        self.num = num

    def do_action(self, action):
        raise NotImplementedError()

class DummyAgent(Agent):
    def do_action(self, action):
        print "doing action %s " % action
        return [0,0,0,0]

class Controller:
    def __init__(self, agent, prefix = "1node"):
        self.agent = agent

        act_filename = "planner_files/ActMapMealy_%s.csv" % prefix
        trans_filename = "planner_files/TransMap_%s.csv" % prefix

        self.act = import_map(act_filename)
        self.trans = import_map(trans_filename)
        self.observations = Observations()
    
    def action(self, observation):
        obs_num = self.observations.lookup(observation)
        lookup_str =gen_lookup_str([self.agent.num, self.node, obs_num])
        try:
            action = self.act[lookup_str]
        except:
            print "could not find action from lookup str %s " % lookup_str
            raise Exception
        print "action %s : %s" % (lookup_str, action)
        return action

    def transition(self, observation, action):
        obs_num = self.observations.lookup(observation)
        lookup_str=gen_lookup_str([self.agent.num, self.node, obs_num, action])
        try:
            node = self.trans[lookup_str]
        except:
            print "could not find transition from lookup str %s " % lookup_str
            raise Exception
        print "transition %s : %s" % (lookup_str, node)
        return node
    
    def run(self, start_node, start_obs, debug=True):
        self.node = start_node
        obs = start_obs
        while True:
            act = self.action(obs)
            self.node = self.transition(obs, act)
            print "Doing action %s " % act
            if debug:
                raw_input()
            obs = self.agent.do_action(act)
             


if __name__=="__main__":
    agent = DummyAgent()
    ctrl = Controller(agent)

    """ Run event loop wih dummy agent """
    ctrl.run(0, [0,0,0,0], True)
    
    """ Test all permuations of observations and actions"""
    for i in range(4):
        for j in range( 2):
            for k in range(2):
                for l in range(3):
                    o = [i,j,k,l]
                    ctrl.action(o)
                    for action in range(5):
                        ctrl.transition(o, action)

