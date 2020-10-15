import numpy as np

def play(nplayers, ncards, nturn, playerid, history, cheated):
  """
   Play the next card.
   Keyword arguments:
     nplayer   -- number of players in game (including you).
     ncards    -- number of initial cards (cards 0,...,ncards-1).
     nturn     -- number of turns already played.
     playyerid -- your player id to access the history matrix.
     history   -- matrix of size (ncards,nplayers) with the cards already played.
                  Note:
                       -- "unplayed slots" are filled with -1
                       -- after the first round, the winner will come first and we go round-robin with open cards
                          so if you are third in line, you can see the cards of other two player in the row `nturn` of history
   Return:
     card      -- the card that you play this turn. It has to be valid!
   """


  # this player plays the cards from ncards-1 to 0
  return ncards-1-nturn