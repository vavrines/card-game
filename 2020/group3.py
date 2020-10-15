import numpy as np
import numpy.random as rng

nGamesPlayed = 0
bookkeeper_firstRound = np.empty((1,4))

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

  #inits
  current_turn = history[nturn,:] #aktueller turn mit ggf. nicht gespielten Karten

  turn_pos = sum(current_turn >= 0) #unsere zug position
  remainingOpponentCards = GetRemainingOpponentCards(history,ncards) # alle verbleibenden Karten der Gegner (ncards-nturns, nplayers)
  current_hand = np.setdiff1d(np.arange(ncards), history[:,playerid]) # alle unsere verbleibenden Karten 

  try:
    cheated = detect_cheater(history,nplayers) # hat jemand eine Karte doppelt gespielt
    if any(cheated) and turn_pos != 0: # wenn jemand gecheated hat und wir nicht die Rundebeginnen muss unsere Stratie angepasst werden weil wir effektiv einen anderen turn spielen
          turn_pos -= sum(cheated)
          for i in np.arange(len(cheated)):
                if cheated[i] == True :
                      current_turn[i] = -1
      
    turnCards = current_turn[current_turn > 0] # alle bisher gespielten Karten                       
          
    card = rng.choice(current_hand) # absicherung damit wir auf jeden Fall eine gültige Karte zurückgeben

    avgCardValueOpponent = [np.mean(i) for i in remainingOpponentCards] #durchschnittlicher Kartenwert der vergangenen Runden
    strategyOpponent = np.zeros((nplayers-1,1))
    for i in np.arange(nplayers-1):
          strategyOpponent[i] = avgCardValueOpponent[i] > (ncards-1)/(2)*1.2 #True if enermy is hoarding and we want to play aggressive        
  
    if nturn==0: #handle round 0  
      if nGamesPlayed > 3: # wenn wir etwas statistik haben um das Verhalten der Gegner zu schätzen
            win_avg_card = np.mean(np.max(bookkeeper_firstRound, axis=1)) # durchschnittlicher Kartenwert der die erste Runde gewinnt
            if win_avg_card>6: # durchschnittlicher Kartenwert > 6 lohnt nicht 
                  card = 0
            else:
                  card = np.ceil(win_avg_card) # spiele knapp überm durchschnittlichen Kartenwert
      else:
        card = 0 # kleinste Karte als erstes

    else: #handle all other rounds
      if nturn == 1: #alle ersten Runden global abspeichern      
        np.append(bookkeeper_firstRound, history[0,:])
      
      # wir fangen an
      if turn_pos == 0:
            # wenn alle Gegner Karten horten spielen wir mittelhohe Karten, falls verfügbar
            if np.mean(strategyOpponent)>= 0.5 and int(np.median(current_hand)) in np.arange(int(ncards*0.4), int(ncards*0.6)): #aggressive
                  card = int(np.median(current_hand))
            else: #passive
                  card = min(current_hand) #spiele die kleine Karte falls alle aggressiv sind        
      # wir sind an 1 oder 2       
      elif turn_pos in [1,2]-sum(cheated):
            # teste welche teams noch nach uns kommen und nicht gecheated haben
            remainingTeams = np.where(current_turn == -1)
            remainingTeams = remainingTeams[0][:-1]
            remainingTeams = [i for i in remainingTeams if not cheated[i]]     
            # den spieler nach uns ignorieren   
            remainingTargetTeams = remainingTeams       
            if turn_pos == 1:
                remainingTargetTeams = np.where(remainingTeams != 0)            
            # aggressiv spielen wenn alle nach uns Karten horten
            if np.mean(strategyOpponent[remainingTargetTeams]) >= 0.5:          
              # wenn unsere höchste Karte größer als die höchste karte aller folgenden Gegner ist -> spielen
              if ( max(current_hand) > max(max(i) for i in remainingOpponentCards[remainingTargetTeams])):         
                    card = min(i for i in current_hand if i > max(max(i) for i in remainingOpponentCards[remainingTargetTeams]))
              else:
                    # ist eine der gespielten Karten > 0.6*ncards -> lohnt nicht -> spielen kleinste karte
                    if any(turnCards >= int(ncards*0.6)):                        
                          card = min(current_hand)
                    # wenn wir ne karte zum reizen haben, tun wir das
                    elif int(np.median(current_hand)) in np.arange(int(ncards*0.4), int(ncards*0.6)):
                          card = int(np.median(current_hand))
                    # sonst kleinste karte
                    else:
                          card = min(current_hand)
                      
            else: #passive     
              # wenn unsere höchste Karte größer als die höchste karte aller folgenden Gegner ist -> spielen        
              if ( max(current_hand) > max(max(i) for i in remainingOpponentCards[remainingTeams])):         
                    card = min(i for i in current_hand if i > max(max(i) for i in remainingOpponentCards[remainingTeams]))
              # sonst kleinste karte
              else:                  
                    card = min(current_hand)
      # wir sind letzter              
      elif turn_pos == 3-sum(cheated):       
            highCard = max(turnCards)
            # können wir den stich bekommen -> nehmen                    
            if max(current_hand)<=highCard:
                  card = min(current_hand)
            # wenn nicht -> abwerfen
            else:
                  card = min(current_hand[current_hand>highCard])

    if card in current_hand:
      return card
    else:
      return rng.choice(current_hand)
  except ValueError:
    return rng.choice(current_hand)
  except ZeroDivisionError:
      return rng.choice(current_hand)

def GetRemainingOpponentCards(history, ncards):
    playedCards_grp0 = history[:,0]
    playedCards_grp1 = history[:,1]
    playedCards_grp2 = history[:,2]

    allCards = np.arange(ncards)
        
    return np.array([np.setdiff1d(allCards, playedCards_grp0),
                     np.setdiff1d(allCards, playedCards_grp1), 
                     np.setdiff1d(allCards, playedCards_grp2)],dtype=object)


def detect_cheater(history, nplayers):
      cheated = np.zeros((3,1))
      for i in np.arange(nplayers-1):
            filtered_history = history[:,i]
            filtered_history = filtered_history[filtered_history != -1]
            cheated[i] = len(np.unique(filtered_history)) != len(filtered_history)
            #if cheated[i]:
            #      print(str(i) + ' cheated')
      return cheated
