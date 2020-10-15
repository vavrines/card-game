##### Second Player 
import numpy as np
def play(nplayers, ncards, nturn, playerid, history, cheated):
  mycards = history[:nturn, playerid]      # these are the cards I played
  possiblecards = np.arange(ncards)       # cards from 0 to ncards -1 
  validcards = np.sort(np.setdiff1d(possiblecards,mycards)) # cards I can still play


  # first round
  if(nturn == 0):
    return np.random.randint(8)


  # last round
  elif(nturn == 9):
    return validcards[0]


  # if any successive round
  else:
    # calcualte position
    position = 5
    for i in range(0, nplayers):
      if(history[nturn,i] == -1):
        position -= 1

    # figure out what is the highest card on the opponents hands
    highest_cards_left = np.zeros(nplayers)
    for i in range(0, nplayers):
      cards_playerid = history[:nturn, i]
      validcards_playerid = np.setdiff1d(possiblecards,cards_playerid)
      highest_cards_left[i] = np.amax(validcards_playerid)
    # identify if we have only highest card in the game
    # find highest drawn card in the game
    high_card = np.amax(history[nturn,:])

    # adopt strategy due to position
    if(position == 1):
      #return validcards[0]
      id1 = np.mod(playerid+1, nplayers)
      id2 = np.mod(playerid+2, nplayers)
      id3 = np.mod(playerid+3, nplayers)
      high1 = highest_cards_left[id1]
      high2 = highest_cards_left[id2]
      high3 = highest_cards_left[id3]
      limit = np.amax([high1, high2, high3])
      larger_cards = validcards[validcards > limit]
      if(len(larger_cards) > 0):
        return larger_cards[0]
      else:
        return validcards[0]

    elif(position == 2):
      id = []
      for i in range(0, nplayers):
        if((history[nturn, i] == -1) and (i != playerid)):
          id.append(i)
      id1 = id[0]
      id2 = id[1]
      high1 = highest_cards_left[id1]
      high2 = highest_cards_left[id2]
      limit = np.amax([high1, high2, high_card])
      larger_cards = validcards[validcards > limit]
      if(len(larger_cards) > 0):
        return larger_cards[0]
      else:
        return validcards[0]


    elif(position == 3):
      # if highest card in game and highest card of player after us is smaller than one of our valid cards, get stitch
      for i in range(0, nplayers):
        if((history[nturn, i] == -1) and (i != playerid)):
          lastplayerid = i
      highest_card_last = highest_cards_left[lastplayerid]
      limit = np.amax([highest_card_last, high_card])
      # if we have the highest card in the game
      if((highest_card_last - high_card) < 4):
        larger_cards = validcards[validcards > limit]
        if(len(larger_cards) > 0):
          return larger_cards[0]
      elif((high_card < 5) and (highest_card_last > 6)):
        return validcards[0]
      

    elif(position == 4):
      # find highest drawn card in the game
      high_card = np.amax(history[nturn,:])
      # play lowest valid card that is larger than the highest card in the game
      larger_cards = validcards[validcards > high_card]
      if(len(larger_cards) > 0):
        return larger_cards[0]
      else:
        return validcards[0]


  if(len(validcards)>2):
    return validcards[np.random.randint(3)]

  return validcards[0]