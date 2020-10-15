import numpy as np
import time
import matplotlib.pyplot as plt
import sys

sys.path.insert(0, 'dummydirectory') #'/content/drive/My Drive/Colab Notebooks/gamenight'

from arena import letsplay
from scoring import score_stich, score_game, did_cheat

from group0 import play as player0
from group1 import play as player1
from group2 import play as player2
from group3 import play as player3

players = [player0, player1, player2, player3]

ncards = 10
toprint = True
score, history = letsplay(players,ncards,toprint,score_stich,score_game,did_cheat)