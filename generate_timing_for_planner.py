#!/usr/bin/env python
# script to quickly get timings

from BeerBotDomain import ACTIONS, LOC, ORDERS, HOLD, PR2
def main():

    # NAVIGATION_TIMES
    times = [None]*LOC.num

    times[LOC.R1] = {
            LOC.R1 : 0,
            LOC.R2 : 10,
            LOC.R3 : 20,
            LOC.KITCHEN: 30
            }

    times[LOC.R2] = {
            LOC.R1 : 0,
            LOC.R2 : 0,
            LOC.R3 : 0,
            LOC.KITCHEN: 0
            }

    times[LOC.R3] = {
            LOC.R1 : 0,
            LOC.R2 : 0,
            LOC.R3 : 0,
            LOC.KITCHEN: 0
            }

    times[LOC.KITCHEN] = {
            LOC.R1 : 0,
            LOC.R2 : 0,
            LOC.R3 : 0,
            LOC.KITCHEN: 0
            }

    
    # PR2 GRASP TIMES
    PR2_GRASP_TIMES = {
            PR2.INHAND : 40,
            PR2.NOT_READY: 90,
            PR2.NO_OBS: -1,
            PR2.SOMEONE: -1
            }


    # VALID OBSERVATIONS AFTER ACTIONS
    valid = [None]*ACTIONS.num

    valid[ACTIONS.ROOM_1] = [3, 7, 11, 15 ]
    valid[ACTIONS.ROOM_2] = [19, 23, 27, 31]
    valid[ACTIONS.ROOM_3] = [35, 39, 43, 47]
    valid[ACTIONS.KITCHEN] = [48, 49, 50, 52, 53, 54]
    valid[ACTIONS.GET_DRINK] = [52, 53, 54]

    # VALID OBSERVATION BEFORE GRAB DRINK
    valid_pre_drink = [49, 50, 53, 54]


    # GENERATE LIST OF OBSERVATIONS and INVALID OBSERVATIONS
    observation = [0]*64
    lookup = {}
    invalid = []
    i = 0
    for loc in [LOC.R1, LOC.R2, LOC.R3, LOC.KITCHEN]:
        for order in [ORDERS.NO_ORDERS, ORDERS.ORDERS]:
            for hold in [HOLD.NOT_HOLDING, HOLD.HOLDING]:
                for pr2 in [PR2.SOMEONE, PR2.INHAND, PR2.NOT_READY, PR2.NO_OBS]:
                    observation[i] = [loc, order, hold, pr2]
                    lookup_str = ("_").join(str(observation[i]))
                    lookup[lookup_str] = i
                    if loc == LOC.KITCHEN: 
                        if order != ORDERS.NO_ORDERS:
                            invalid.append(i)
                    else:
                        if pr2 != PR2.NO_OBS: 
                            invalid.append(i)
                    i += 1
    
    
    
    def get_time(action, pre_i,pre_obs, eff_i, eff_obs):
        if pre_i in invalid or eff_i in invalid:
            return -1
        
        if eff_i not in valid[action]:
            return -1           
        if action == ACTIONS.GET_DRINK:
            if pre_i not in valid_pre_drink:
                return -1
            time = PR2_GRASP_TIMES[pre_obs[3]] #pr2 index
        else:
            time = times[pre_obs[0]][eff_obs[0]] 
        return time
   
    filename = "timings.csv"
    f_csv = open(filename, "wb")

    filename = 'timings_all.txt'
    f_all = open(filename, "wb")
    
    filename = 'timings_valid.txt'
    f_valid = open(filename, "wb")

           
    for action in range(ACTIONS.num):
        for pre_i,pre_obs in enumerate(observation):
            for eff_i, eff_obs in enumerate(observation):
                time = get_time(action, pre_i, pre_obs, eff_i, eff_obs)
                if time > -1:
                    f_valid.write( "time[%s][%s][%s] = %s \n"\
                            % (action, pre_i, eff_i, time))
                f_all.write( "time[%s][%s][%s] = %s \n"\
                        % (action, pre_i, eff_i, time))
                f_csv.write("%s,%s,%s,%s\n"% (action, pre_i, eff_i, time))


    f_all.close()
    f_valid.close()
main()




