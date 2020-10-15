
import numpy as np
import math
import random



#def playRandOfTheLowestIniRound(ownCards,ncards):
#  lowerThird = math.floor(2/3*nCards) # just take one of the lower third
#  card_to_play = random.randint(0, lowerThird)
#  return card_to_play

def playLowestHighest(highestCardOnTable,  ownCards):
  candidateCards = []
  #get Candidates
  for i in range(0,ownCards.size):
    if(ownCards[i] > highestCardOnTable):
      candidateCards.append(ownCards[i])
  #get lowestCandidate
  card_to_play = min(candidateCards)
  return card_to_play

def playLowestHighestEq(highestCardOnTable,  ownCards):
  candidateCards = []
  #get Candidates
  for i in range(0,ownCards.size):
    if(ownCards[i] >= highestCardOnTable):
      candidateCards.append(ownCards[i])
  #get lowestCandidate
  card_to_play = min(candidateCards)
  return card_to_play

def firstRound(ncards):
    return random.randint(0, np.floor(ncards/3))

def playLowest(cards,playerid):
    CardToPlay = np.argmax(cards[playerid,:] > -1)
    return CardToPlay

def playMaybe(pos, ownCards, addInfo, playerId):
    if(pos == 2):
        if(addInfo<7):
            return addInfo
        else:
            playLowest(ownCards,playerId)
    else:
        if(addInfo<9):
            return addInfo
        else:
            playLowest(ownCards, playerId)

def playTie(pos, ownCards, addInfo, playerId, history, cheated, nTurn, nplayers):
    card = 0;
    (card_to_playCWW, enemies) = addInfo
    scores = current_scores(history, cheated, nTurn, nplayers)


    card_to_play = tieWithCloseProximity(scores, enemies, ownCards, card_to_playCWW, nplayers)

    return card_to_play

def canWeWin(cards, playerid, grp_ind, botsAlreadyPlayed,cardsAlreadyPlayedIn):
    #cards= cards other players are holding
    # playerId = :)
    # botsAlreadyPlayed = idx of bot already played
    # cardsAlreadyPlayed = cards already played by te bots already played
    cardsAlreadyPlayed = cardsAlreadyPlayedIn[0]
    ownCards=cards[playerid,:]
    botsAfterUs = np.setdiff1d(grp_ind,botsAlreadyPlayed)
    currentLeader = []
    if(cardsAlreadyPlayed.size == 0):
        highestCardOnTable = -1
    else:
        highestCardOnTable = np.amax(cardsAlreadyPlayed)
        for i in range(len(botsAlreadyPlayed)):  # who of the bots after us has the highest cards avail
            if highestCardOnTable == cardsAlreadyPlayed[i]:
                currentLeader.append(botsAlreadyPlayed[i])



    highestStillPlayableCard = -1
    botWithMax=[]
    for i in range(len(botsAfterUs)): #who of the bots after us has the highest cards avail
      if  highestStillPlayableCard < np.max(cards[botsAfterUs[i],:]):
        highestStillPlayableCard = np.max(cards[botsAfterUs[i],:])
        botWithMax.append(botsAfterUs[i])
      elif highestStillPlayableCard == np.max(cards[botsAfterUs[i],:]):
        botWithMax.append(botsAfterUs[i])

    candidateCardsWin = []
    candidateCardsTie = []
    candidateCardsMaybe = []
    ourEnemies =[]

    if highestStillPlayableCard < highestCardOnTable:
        ourEnemies.append(currentLeader)
    elif highestStillPlayableCard > highestCardOnTable:
        ourEnemies.append(botWithMax)
    else:
        ourEnemies.append(botWithMax)
        ourEnemies.append(currentLeader)

    #get Candidates

    for i in range(0,ownCards.size):
      #if(ownCards[i] < highestCardOnTable and ownCards[i] < highestStillPlayableCard):
      #break
      if(ownCards[i] > highestCardOnTable and ownCards[i] > highestStillPlayableCard):
        candidateCardsWin.append(ownCards[i])
      elif(ownCards[i] > highestCardOnTable and ownCards[i] == highestStillPlayableCard):
        candidateCardsTie.append(ownCards[i])
      elif(ownCards[i] == highestCardOnTable and ownCards[i] == highestStillPlayableCard):
        candidateCardsTie.append(ownCards[i])
      elif(ownCards[i] == highestCardOnTable and ownCards[i] > highestStillPlayableCard):
        candidateCardsTie.append(ownCards[i])
      elif(ownCards[i] > highestCardOnTable):
        candidateCardsMaybe.append(ownCards[i])

    if len(candidateCardsWin) != 0 :
      card_to_play = min(candidateCardsWin)
      return (1, card_to_play)
    elif len(candidateCardsTie) != 0:
      card_to_play = min(candidateCardsTie)
      return (2, (card_to_play,ourEnemies))
    elif len(candidateCardsMaybe) != 0:
      card_to_play = min(candidateCardsMaybe)
      return (3, card_to_play)
    else:
      return (4, -1)


def playMedium(ownCards):
    tmp = ownCards.sort()
    return tmp[int(len(tmp)/2)]


def tieWithCloseProximity(currentScores,tiePlayer,cards,CardToTie,nplayer):
  closeProximity = 2
  diff = np.zeros(nplayer)
  for i in range(nplayer):
    diff[i] = abs(currentScores[i]-currentScores[2])
  if diff[tiePlayer] <= closeProximity:
    return CardToTie
  else:
    playLowest(cards)


def areWeLeader(history,cheated,nTurn, nplayers, playerid):
  scoreBoard = current_scores(history,cheated,nTurn, nplayers)
  return scoreBoard(playerid) == max(scoreBoard)


def current_scores(history, cheated, nTurn, nplayers):

  #loop over all terms
  currScores = np.zeros(nplayers)
  for i in range(0,nTurn-1):
    currScores+=score_stich(history[i], cheated) # careful,  this is not completely right

  return currScores

def score_stich(cards, cheated):
  """Distributes the reward and return winner id."""

  cardscopy = np.copy(cards)
  cardscopy[cheated] = -99999999

  winner = cardscopy == np.max(cardscopy)
  # Normalize reward:
  # 1 winner: 1   point
  # 2 winnnr: 1/2 points
  # 3 winner: 1/3 points
  # 4 winner: 1/4 points
  # (but the code should work with n players too)
  points =  winner / np.sum(winner)

  # find out which player won (if multiple winner, pick one)
  winnerid = np.random.permutation(np.argwhere(cardscopy == np.max(cardscopy)))[0]
  return points, winnerid





