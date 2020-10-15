import numpy as np  
import time

def letsplay(players, ncards, printmode,score_stich, score_game,did_cheat):
  """
  Plays one single match.
  Keyword arguments:
    players      -- an array with the bots
    ncards       -- the number of cards for this match
    printmode    -- whether to print or not  
    score_stich  -- scoring for one stich
    score_game   -- scoring for the whole match
    did_cheat    -- checks whether someone cheated
  Return:
    points       -- the points after the match
  """
  printIntro()

  nplayers = len(players)
  stiche = np.zeros(nplayers)
  history = -np.ones((ncards,nplayers),dtype=int)
  playerorder = np.arange(nplayers)
  for nturn in range(ncards):
    #print(playerorder)
    for playerid in playerorder:
      #print(history[:nturn+1,:])
      cheated = did_cheat(history)
      player = players[playerid]
      if nturn == 0: # first round, everyone plays with cards covered
        card = player(nplayers, ncards, nturn, playerid,  -np.ones((ncards,nplayers),dtype=int), cheated)
      else: # after that, we go round-robin with open cards
        card = player(nplayers, ncards, nturn, playerid, history, cheated)

      history[nturn,playerid] = card

    
    stich, winnerid =score_stich(history[nturn,:], did_cheat(history))
    stiche += stich
    playerorderCopy = playerorder
    playerorder = np.roll(np.arange(nplayers),-winnerid) # winner comes first next round

    #if True:
     #print()
     # print(history[:nturn+1])
    if printmode:
      printTurn(cheated,nturn,stich,history[nturn,:],playerorderCopy)

  score = score_game(stiche)
  if printmode:
    printResults(stiche, score)

  return score, history


def printTurn(cheated, nturn,stich,cards, playerorder):
  time.sleep(1)
  print("\n")
  print(f"############### TURN {nturn} #################")
  print(f"# Team {playerorder[0]} opens the round!              #")
  print(f"# Team 0 plays: {int(cards[0])}                      #")
  print(f"# Team 1 plays: {int(cards[1])}                      #")
  print(f"# Team 2 plays: {int(cards[2])}                      #")
  print(f"# Team 4 plays: {int(cards[3])}                      #")
  print( "# ------------------------------------ #")
  if(any(cheated)):
    print("# There are teams that try to cheat!   #")
  if(cheated[0]):
    print("# Team 0 is disqualified this game!    #")
  if (cheated[1]):
    print("# Team 1 is disqualified this game!    #")
  if (cheated[2]):
    print("# Team 2 is disqualified this game!    #")
  if (cheated[3]):
    print("# Team 3 is disqualified this game!    #")
  if (any(cheated)):
    print( "# ------------------------------------ #")

  gewinner = np.count_nonzero(stich)
  if(gewinner == 1):
    player = 0
    for i in stich:
      if(i >0):
        print(f"# Team {player} wins this round!              #")
        print(f"# Congrats! They get 1 point           #")
        print(f"# and will open the next round.        #")
      player+=1

  if(gewinner >1):
    print(f"# We have a draw this round.           #")
    print(f"# All winners get " + "{:.1f}".format(1/gewinner) + " points.          #")
    print(f"# The opener is randomly chosen.       #")

  print( "########################################")
  #input(" \nPRESS ANY KEY TO START THE NEXT ROUND !!!\n")


  #print(f"\n\n\nIt's turn {nturn}. Up to now, the points are:")
  #for playerid, point in enumerate(stiche - stich):
  #  print("Group {}: {:.3f}".format(playerid, point), end=" ")
  #print("\n\nThis turn, the cards played are:")
  #for playerid, card in enumerate(cards):
  #  print("Group {}: {}".format(playerid, int(card)))
  #print("\n\nAnd the points rewarded are:")
  #for playerid, point in enumerate(stich):
  #  print("Group {}: {:.3f}".format(playerid, point), end=" ")

  return 0

def printResults(stiche, score):
  print(f"\n############## GAME OVER ###############")
  print(f"# Final Score:                         #")
  print(f"# Team 0 won {int(stiche[0])} times and gets {int(score[0])} points!#")
  print(f"# Team 1 won {int(stiche[1])} times and gets {int(score[1])} points!#")
  print(f"# Team 2 won {int(stiche[2])} times and gets {int(score[2])} points!#")
  print(f"# Team 4 won {int(stiche[3])} times and gets {int(score[3])} points!#")
  print("########################################")
  input(" \nPRESS ANY KEY TO EXIT !!!\n")

 # print("\n\nThe game ended. Final score:")
 # for playerid, point in enumerate(stiche):
 #   print("Group {}: {:.3f}".format(playerid, point), end=" ")
 # print("\n\nPoints for this game:")
 # for playerid, point in enumerate(score):
 #   print("Group {}: {:.3f}".format(playerid, point), end=" ")

  return 0

def printIntro():
  print("#########################################")
  print("#  ♥♠  _____    _     ___    __    ♦♣   #")
  print("#  ♠♦ /    |   / \\   |  |  |   \\   ♣♥   #")
  print("#  ♦♣ |       /___\\  |__   |   |   ♥♠   #")
  print("#  ♣♥ \\____| /     \\ |  \\  |__/    ♠♦   #")
  print("#                                      #")
  print("#    _   .   _   ___  _    _  ______   #")
  print("#   | \\  |  ||  /     |    |    ||     #")
  print("#   |  \\ |  ||  |  _  |----|    ||     #")
  print("#   |   \\|  ||  \___| |    |    ||     #")
  print("#                                      #")
  print("########################################")
  print(" ")
  input(" PRESS ANY KEY TO START !!!")

  return 0

