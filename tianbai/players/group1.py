import numpy as np

def play(nplayers, ncards, nturn, playerid, history, cheated):
  # this player plays a random card and might therefore cheat
  return np.random.randint(ncards)
