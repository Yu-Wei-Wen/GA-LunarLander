"""
* The state is an 8-dimensional vector: 
    (1,2) the coordinates of the lander in x & y, 
    (3,4) its linear velocities in x & y, 
    (5,6) its angle, its angular velocity, and
    (7,8) two booleans that represent whether each leg is in contact with the ground or not.

* Action is two real values vector from -1 to +1.
    (1) First value controls main engine
        * [-1, 0] off, engine can't work with less than 50% power.
        * [0, 1] throttle from 50% to 100% power.
    (2) Second value controls side engine
        * [-1.0, -0.5] fire left engine
        * [0.5, 1.0] fire right engine
        * [0.5, 0.5] off.

* In this practice, an observation is reduced to a "state" by `Observation2State` function.
    (1) A state is a high-level representation of the lunar lander's conditions.
    (2) The GA is used to search for the optimal state-action mapping (control policy).
"""

import gymnasium as gym
import numpy as np
import random
import GA
import math
import copy
import pickle
import csv

OUTFILE_PREFIX = "LL-Result0-BX-GM"


####### LunarLander Constants #######
STATE_DIM = 3 * 3 * 3
N_ENGINE  = 2
THRUST_LB = -1.
THRUST_UB = 1.

STATE_LB = [ 1.5,  1.5,  5.,  5.,  3.14,  5., 1., 1.]   # unused
STATE_UB = [-1.5, -1.5, -5., -5., -3.14, -5., 0., 0.]   # unused

rescale   = lambda x, t_lb, t_ub : x * (t_ub - t_lb) + t_lb

####### Function Declaration #######
def Observation2State(obsv:list) -> list:
    #### Horizontally Centered ####
    """
    [State]
      0: almost centered
      1: on the left of center
      2: on the right of center
    """
    x_pos  = obsv[0]
    s_cntr = 0
    if x_pos < -0.1:
        s_cntr = 1
    elif x_pos > 0.1:
        s_cntr = 2

    #### Descending ####
    """
    [State]
      0: descending moderately 
      1: climbing or hovering
      2: descending fast
    """
    aprx_vel = obsv[3] * -1
    s_desc = 0
    if aprx_vel < 0.1:
        s_desc = 1
    elif aprx_vel > 0.25:
        s_desc = 2

    #### Tilt ####
    """
    [State]
      0: almost upright
      1: left tilted
      2: right tilted
    """
    angle  = obsv[4] / 3.14 * 180
    s_tilt =  0

    if angle < 3:
        s_tilt = 1
    elif angle > 3:
        s_tilt = 2

    return [s_cntr, s_desc, s_tilt]

def Observation2Action(obsv:list, policy:list) -> list:
    s_cntr, s_desc, s_tilt = Observation2State(obsv)
    s_landed_L, s_landed_R = obsv[6], obsv[7]

    p_arr = np.array(policy)
    p_arr = np.reshape(p_arr, (3, 3, 3, 2)) # centered (0,1,2), descend (0,1,2), tilt (0,1,2), thrust (main, side)

    thrust_m, thrust_s = 0., 0.

    if s_landed_L != s_landed_R:
        thrust_m, thrust_s = 0.05, 0.
    else:
        thrust_m, thrust_s = p_arr[s_cntr][s_desc][s_tilt]

    return [thrust_m, thrust_s]

def Simulation(env, policy, n_repeat=1, verbose=False, graphic=False):
    total_reward = 0.

    for ep in range(n_repeat):
        env.reset()
        action = [0., 0.]
        ep_reward = 0.
        while True:
            if graphic:
                env.render()

            observation, reward, terminated, truncated, info = env.step(action)
            ep_reward = (ep_reward + reward) if not truncated else -math.inf

            if terminated or truncated:
                break
            else:
                action = Observation2Action(observation, policy)
        
        total_reward += ep_reward
        
        if verbose:
            print(f"\r>>> simulating ... [EP{ep+1:02}] reward: {ep_reward:8.3f}", end="")
    
    if verbose:
        print(f"\r{' '*80}\r", end="")

    return total_reward
    

####### Main #######
if __name__ == "__main__":

    # `env` simulate without rendering graphics (faster)
    ll_env = gym.make("LunarLanderContinuous-v2")

    ll_env_graphic = gym.make("LunarLanderContinuous-v2", render_mode="human")

    #### GA Parameters ####
    chrm_len = (STATE_DIM * N_ENGINE)
    pop_size = 50
    xover_rate = 0.9
    mutat_rate = 0.1
    lb = THRUST_LB
    ub = THRUST_UB
    n_sim = 10
    #######################

    # Store the best-so-far solution for replay
    # Remember to update these variables whenever a better policy is found.
    best_policy  = None
    best_fitness = -math.inf

    ## INITIALIZE the population (pop) with random chromosomes ##
    pop = []
    fit = []
    for i in range(pop_size):
        pop.append([random.uniform(lb, ub) for i in range(chrm_len)])
        fit.append(-math.inf)

    ## EVALUATE the initial population through repeated simulation ##
    for i in range(pop_size):
        fitness = Simulation(ll_env, pop[i], n_repeat=n_sim) / n_sim
        fit[i] = fitness

    #################################
    ####   YOUR CODE GOES HERE   ####
    #################################

    #### Evolution Cycle ####
    
    ## 1) PARENT SELECTION ##

    ## 2) Crossover ##

    ## 3) Mutation ##

    ## 4) Evaluation ##
    """ May refer to the above code snippet for EVALUATE"""

    ## 5) Survival Selection ##
    """ You may need to sort the `pop` list based on the `fit` list.
        To do so, please see: https://stackoverflow.com/questions/6618515/sorting-list-according-to-corresponding-values-from-a-parallel-list
    """

    ## The next generation ##
    # After dying out the less competitive half of the population, 
    # start over a new generation (the next evolution cycle).
    


    ####### Post-Evolution #######
    """ May use the following function call to see how your policy behaves. """
    # Replay the best control policy
    Simulation(ll_env_graphic, best_policy, n_repeat=30, verbose=True, graphic=True)