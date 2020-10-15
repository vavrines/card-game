import numpy as np



def logic(nplayers, ncards, nturn, playerid, history, cheated):
  cards_on_table = list()
  players_not_played = list()
  for n in range(nplayers):
    if history[nturn, n] != -1:
      cards_on_table.append(history[nturn, n])
    else:
      players_not_played.append(n)
    if n == playerid:
      new_id = len(players_not_played) - 1
  cards_in_hand_of_notplayed = list()
  max_notplayed_others = list()
  for n in players_not_played:
    cards_in_hand_of_notplayed.append(np.setdiff1d(np.arange(ncards), history[:nturn, n]))
    if n is not playerid:
      max_notplayed_others.append(max(cards_in_hand_of_notplayed[-1]))
  max_all = -1
  if len(cards_on_table) > 1:
    max_all = max(cards_on_table)
  if len(max_notplayed_others) > 1:
    max_all = max([max_all, max(max_notplayed_others)])
  # if we can win this round, do so with minimal one
  if max(cards_in_hand_of_notplayed[new_id]) > max_all:
    for i in range(min(cards_in_hand_of_notplayed[new_id]), max(cards_in_hand_of_notplayed[new_id])+1, 1):
      if i in cards_in_hand_of_notplayed[new_id] and i > max_all:
        return True, i
  else:
    return False, min(cards_in_hand_of_notplayed[new_id])

def theirlogic(nplayers, ncards, nturn, playerid, history, cheated):
  cards_on_table = list()
  players_not_played = list()
  for n in range(nplayers):
    if history[nturn, n] != -1:
      cards_on_table.append(history[nturn, n])
    else:
      players_not_played.append(n)
    if n == playerid:
      new_id = len(players_not_played) - 1
  cards_in_hand_of_notplayed = list()
  max_notplayed_others = list()
  maximalni=list()
  i=0
  for k in players_not_played:
    for n in players_not_played:
      cards_in_hand_of_notplayed.append(np.setdiff1d(np.arange(ncards), history[:nturn, n]))
      if n is not k:
        max_notplayed_others.append(max(cards_in_hand_of_notplayed[-1]))
    max_all=-1
    if len(cards_on_table) > 1:
      max_all = max(cards_on_table)
    if len(max_notplayed_others) > 1:
      max_all = max([max_all, max(max_notplayed_others)])
    maximalni.append([k, max_all])
    max_notplayed_others=list()
    cards_in_hand_of_notplayed = list()
  for n in players_not_played:
    cards_in_hand_of_notplayed.append(np.setdiff1d(np.arange(ncards), history[:nturn, n]))
  for j in range(len(players_not_played)):
    if((max(cards_in_hand_of_notplayed[j])>maximalni[j][1]) and (players_not_played[j] is not playerid)):
      return True, min(cards_in_hand_of_notplayed[new_id])
  return False, min(cards_in_hand_of_notplayed[new_id])





def getcards(nplayers, ncards, nturn, playerid, history, cheated):

  # Let's say you have cards 1 2 3 4 5 9 on your hand
  # and the cards that are out are 4 5
  # then you will never play the 2 or 3 but instead the 1
  # so your valid cards should become
  # 1 5 9
  #
  # same if you have 1 2 3 4 5 8 and there's a 9 out, you are playing the 1 
  mycards = history[:nturn,playerid]     # these are the cards I played
  possiblecards = np.arange(ncards) # cards from 0 to ncards -1 
  validcards = np.setdiff1d(possiblecards,mycards) # cards I can still play

  row = history[nturn,:]
  cardsout = row[row>-1]
  if len(cardsout)>0:
    maxcardout = max(cardsout)
  else:
    maxcardout = -1

  reasonable_cards = [] 
  for i,card in enumerate(validcards):
    if card >= maxcardout or i == 0:
      reasonable_cards.append(card)
  validcards = np.array(reasonable_cards)
  return validcards






def play(nplayers, ncards, nturn, playerid, history, cheated):
  winning,cardwinning = logic(nplayers, ncards, nturn, playerid, history, cheated)
  if winning:
    return cardwinning
  loosing, cardloosing = theirlogic(nplayers, ncards, nturn, playerid, history, cheated)
  if loosing:
    return cardloosing
  position = np.sum(history[nturn,:]>-1)
  validcards = getcards(nplayers, ncards, nturn, playerid, history, cheated)  
  

  row = history[nturn,:]
  cardsout = row[row>-1]
  if position == nplayers -2 : # second to last play, pretend the cards of the last player are already open 
    nextid = (playerid + 1) % 4
    theirvalidcards = getcards(nplayers, ncards, nturn, nextid, history, cheated)  
    cardsout = np.append(cardsout,theirvalidcards) 

  if position in [0,1]:
    return validcards[0] if nturn<3 else validcards[-1]

  maxcardout = max(cardsout)
  if position in [nplayers-1, nplayers-2]: # last player or second to last 
    idx = np.argwhere(validcards >= maxcardout)

    if idx.shape[0]>0: # do we have a card better or equal than the best that is out
      ourcard = validcards[idx[0]] # the one that is just above the best out
      if sum(cardsout == ourcard) < 3: #(<2 means win alone or two-way split)
        return ourcard
      else:
        return validcards[0] # our worst card
    else:
      return validcards[0] # our worst card

  
  return validcards[0]
