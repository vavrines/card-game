import numpy as np

a = np.zeros(5)

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

    # As an example, this bot plays a random, unplayed card.

    mycards = history[:nturn,playerid]     # these are the cards I played

    possiblecards = np.arange(ncards) # cards from 0 to ncards -1 

    validcards = np.setdiff1d(possiblecards,mycards) # cards I can still play

    shuffle = np.random.permutation(validcards) # shuffle

    return shuffle[0] # return the first of the shuffled cards