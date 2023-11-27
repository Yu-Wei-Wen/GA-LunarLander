from LL import Simulation
import gymnasium as gym
import numpy as np
import random
import math
import pickle

#### main ###
ll_env_graphic = gym.make("LunarLanderContinuous-v2", render_mode="human")

# with open(f'{OUTFILE_PREFIX}-policy.pickle', 'rb') as f:
with open(f'policy/LL-Result2-BX-GM-policy.pickle', 'rb') as f:
    policy = pickle.load(f)
    Simulation(ll_env_graphic, policy, n_repeat=30, verbose=True, graphic=True)