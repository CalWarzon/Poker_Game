import os


def shuffle_deck():
  deck = set()
  suits = ['H', 'D', 'C', 'S']
  for i in range(1, 14):
    for e in suits:
      if i == 1:
        deck.add('A' + e)
      elif i == 11:
        deck.add('J' + e)
      elif i == 12:
        deck.add('Q' + e)
      elif i == 13:
        deck.add('K' + e)
      elif i == 10:
        deck.add('T' + e)
      else:
        deck.add(str(i) + e)
  return deck


def how_many_players():
  question1 = input("How many players are there? ")
  question2 = input("How many chips does everyone get? ")
  playerdict = {
      "chips": int(question2),
      "bet": 0,
      "hand": [],
      "status": 'waiting',
      'position': '0',
      "lastaction": 'none',
      'maxpot': 0,
      'callonallin': 0,
      'allinthishand' : 0,
  }
  info = []
  players = int(question1)
  for i in range(players):
    info.append(playerdict.copy())
  info.append(players)
  return info


def run_hand(info, first):
  downcards = []
  players = info[-1]
  pot = 0
  call = bigblind
  deck = shuffle_deck()
  os.system('clear')
  for i in range(players):
    name = int(((i + players + first) % players) + 1)
    info[name - 1]["hand"] = [deck.pop(), deck.pop()]
    info[name - 1]["position"] = players - (i + 1)
    info[name - 1]["lastaction"] = 'none'
    info[name - 1]["bet"] = 0
    info[name - 1]["status"] = 'waiting'
    if info[name - 1]["position"] == 1:
      if info[name - 1]["chips"] > bigblind:
        info[name - 1]["bet"] = bigblind
        info[name - 1]["chips"] -= bigblind
        pot += bigblind
      else:
        info[name - 1]["bet"] = info[name - 1]["chips"]
        pot += info[name - 1]["chips"]
        info[name - 1]["chips"] = 0
        info[name - 1]['status'] = 'all in'
    elif info[name - 1]["position"] == 2:
      if info[name - 1]["chips"] > smallblind:
        info[name - 1]["bet"] = smallblind
        info[name - 1]["chips"] -= smallblind
        pot += smallblind
      else:
        info[name - 1]["bet"] = info[name - 1]["chips"]
        pot += info[name - 1]["chips"]
        info[name - 1]["chips"] = 0
        info[name - 1]['status'] = 'All in'
  a = run_betting_round(info, players, first, call, downcards, pot)
  info = a[0]
  pot = a[1]
  call = 0
  for e in range(players):
    if info[e]['status'] != 'folded' and info[e]['status'] != 'all in':
      info[e]['status'] = 'waiting'
      info[e]['lastaction'] = 'none'
    if info[e]['status'] != 'all in':
      info[e]['maxpot'] = pot
    info[e]['bet'] = 0
  input('Press enter to deal the flop')
  for i in range(3):
    downcards.append(deck.pop())
  os.system('clear')
  print('The flop is ', downcards[0], ', ', downcards[1], ', ', downcards[2],
        '\n')
  input('Press enter to start betting round')
  os.system('clear')
  a = run_betting_round(info.copy(), players, first, call, downcards, pot)
  info = a[0]
  pot = a[1]
  call = 0
  for e in range(players):
    if info[e]['status'] != 'folded' and info[e]['status'] != 'all in':
      info[e]['status'] = 'waiting'
      info[e]['lastaction'] = 'none'
    if info[e]['status'] != 'all in':
      info[e]['maxpot'] = pot
    info[e]['bet'] = 0
  input('Press enter to deal the turn')
  downcards.append(deck.pop())
  print('The turn is ', downcards[0], ', ', downcards[1], ', ', downcards[2],
        ', ', downcards[3], '\n')
  input('Press enter to start betting round')
  os.system('clear')
  a = run_betting_round(info.copy(), players, first, call, downcards, pot)
  info = a[0]
  pot = a[1]
  for e in range(players):
    if info[e]['status'] != 'folded' and info[e]['status'] != 'all in':
      info[e]['status'] = 'waiting'
      info[e]['lastaction'] = 'none'
    if info[e]['status'] != 'all in':
      info[e]['maxpot'] = pot
    info[e]['bet'] = 0
  call = 0
  input('Press enter to deal the river')
  downcards.append(deck.pop())
  print('The river is ', downcards[0], ', ', downcards[1], ', ', downcards[2],
        ', ', downcards[3], ', ', downcards[4], '\n')
  input('Press enter to start betting round')
  os.system('clear')
  a = run_betting_round(info.copy(), players, first, call, downcards, pot)
  info = a[0]
  pot = a[1]
  for e in range(players):
    if info[e]['status'] != 'folded' and info[e]['status'] != 'all in':
      info[e]['status'] = 'waiting'
      info[e]['lastaction'] = 'none'
    if info[e]['status'] != 'all in':
      info[e]['maxpot'] = pot
    info[e]['bet'] = 0
  call = 0
  input('Press enter to show cards')
  os.system('clear')
  amountofplayersin = 0
  playersin = []
  for e in range(players):
    if info[e]['status'] != 'folded':
      amountofplayersin += 1
      playersin.append(e)
  if amountofplayersin != 1:
    for e in range(players):
      if info[e]['status'] != 'folded':
        print('Player ', e + 1, ' has ', info[e]['hand'][0], ' and ',
              info[e]['hand'][1], '\n')
      else:
        print('Player ', e + 1, ' folded \n')
    print('Down cards are ', downcards[0], ', ', downcards[1], ', ',
          downcards[2], ', ', downcards[3], ',', downcards[4], '\n')
    playerscards = []
    for e in range(amountofplayersin):
      templist = []
      for i in range(2):
        templist.append(simplifycards(info[playersin[e]]['hand'][i]).copy())
      for i in range(5):
        templist.append(simplifycards(downcards[i]).copy())
      playerscards.append(templist.copy())
    playerhandvalues = []
    for e in range(amountofplayersin):
      playerhandvalues.append(handvalue(playerscards[e]).copy())
    going = True
    potavailible = pot
    while going:
      best = findbesthand(playerhandvalues)
      if len(best) == 1:
        bestplayer = playersin[best[0]]
        potplayergets = info[bestplayer]['maxpot'] - (pot - potavailible)
        print('Player ', bestplayer + 1, ' has won the pot of ', potplayergets,
              ' chips')
        info[bestplayer]['chips'] += potplayergets
        potavailible -= potplayergets
        if potavailible == 0:
          pot = 0
          going = False
        del playersin[best[0]]
        del playerhandvalues[best[0]]
      else:
        bestplayers = []
        for i in best:
          bestplayers.append(playersin[i])
        print('There is a tie between players ')
        for e in bestplayers:
          info[e]['chips'] += potavailible / len(bestplayers)
          print(e + 1, ' wins ', potavailible / len(bestplayers))
          pot = 0
          going = False
  else:
    print('Player', playersin[0] + 1, ' wins the pot of ', pot, 'chips')
    info[playersin[0]]['chips'] += pot
  input('\n Press enter to continue')
  return[info.copy()]


def run_betting_round(info, players, first, call, downcards, pot):
  i = 0
  while True:
    name = int(((i + players + first - 1) % players) + 1)
    booltemp = False
    for e in range(players):
      if info[e]["status"] != 'in' and info[e]['status'] != 'folded' and info[
          e]['status'] != 'all in':
        booltemp = True
    if not booltemp:
      break
    playerscanbet = 0
    for e in range(players):
      if info[e]['status'] != 'folded' and info[e]['status'] != 'all in':
        playerscanbet += 1
    if playerscanbet <= 1:
      break
    if info[name - 1]["status"] == 'folded' or info[name -
                                                    1]['status'] == 'all in':
      i += 1
      continue
    print("Give phone to player ", name)
    input("Press enter to continue")
    os.system('clear')
    print("Player ", name, " your hand is: ", info[name - 1]['hand'])
    print("The down cards are: ", downcards, '\n')
    stayin = call - info[name - 1]['bet']
    for e in range(players):
      if e != (name - 1):
        print("Player ", str(e + 1), " has ", info[e]['chips'],
              " chips , their last action was ", info[e]['lastaction'],
              ", they have", info[e]['bet'], " in the pot, and they are ",
              info[e]['status'], "\n")
      else:
        print("You have ", info[e]['chips'], " chips, your last action was ",
              info[e]['lastaction'], " and you have", info[e]['bet'],
              " in the pot \n")
    print("The pot contains ", pot, " chips \n")
    if info[name - 1]['status'] != 'All in':
      move = input(
          "State your move, type call or press enter to call for " +
          str(stayin) +
          " chips, to fold type fold, to check type check, to raise type the amount you want to raise by.(checking when not posible will call, raising more than you have, or an invalid input will cause a fold): "
      )
      if move == 'call' or move == 'check' or move == '':
        if info[name - 1]['chips'] > stayin:
          info[name - 1]['bet'] += stayin
          pot += stayin
          info[name - 1]['chips'] -= stayin
          info[name - 1]['lastaction'] = 'call'
          info[name - 1]['status'] = 'in'
        else:
          info[name - 1]['bet'] += info[name - 1]['chips']
          info[name - 1]['callonallin'] = info[name - 1]['chips']
          pot += info[name - 1]['chips']
          info[name - 1]['chips'] = 0
          info[name - 1]['lastaction'] = 'call'
          info[name - 1]['status'] = 'all in'
          info[name - 1]['allinthishand'] = True
          info[name - 1]['maxpot'] = pot
      elif move == 'fold':
        info[name - 1]['status'] = 'folded'
        info[name - 1]['lastaction'] = 'fold'
      else:
        try:
          if info[name - 1]['chips'] > int(move) + stayin:
            info[name - 1]['bet'] += int(move) + stayin
            info[name - 1]['chips'] -= int(move) + stayin
            pot += int(move) + stayin
            info[name - 1]['lastaction'] = 'raise'
            for e in range(players):
              if info[e]['status'] == 'in':
                info[e]['status'] = 'waiting'
            info[name - 1]['status'] = 'in'
            call += int(move)
          elif info[name - 1]['chips'] == int(move) + stayin:
            info[name - 1]['bet'] += int(move) + stayin
            info[name-1]['allinthishand'] = True
            info[name - 1]['chips'] -= int(move) + stayin
            pot += int(move) + stayin
            info[name - 1]['lastaction'] = 'raise'
            for e in range(players):
              if info[e]['status'] == 'in':
                info[e]['status'] = 'waiting'
            info[name - 1]['status'] = 'all in'
            info[name - 1]['maxpot'] = pot
            call += int(move)
          else:
            info[name - 1]['lastaction'] = 'fold'
            info[name - 1]['status'] = 'folded'
        except (ValueError):
          info[name - 1]['lastaction'] = 'fold'
          info[name - 1]['status'] = 'folded'

    input("\n Press enter to continue")
    os.system('clear')
    i += 1
  for i in range(players):
    if info[i]['allinthishand']:
      info[i]['maxpot'] = pot
      info[i]['allinthishand'] = False
  return [info, pot]


def simplifycards(card):
  newcard = []
  if card[0] == 'A':
    newcard.append(14)
  elif card[0] == 'K':
    newcard.append(13)
  elif card[0] == 'Q':
    newcard.append(12)
  elif card[0] == 'J':
    newcard.append(11)
  elif card[0] == 'T':
    newcard.append(10)
  else:
    newcard.append(int(card[0]))
  if card[1] == 'S':
    newcard.append('s')
  elif card[1] == 'C':
    newcard.append('c')
  elif card[1] == 'D':
    newcard.append('d')
  elif card[1] == 'H':
    newcard.append('h')
  return newcard


def handvalue(hand):
  value = []
  a = checkstraightflush(hand)
  b = checkfourkind(hand)
  c = checkfullhouse(hand)
  d = checkflush(hand)
  e = checkstraight(hand)
  f = checkthreekind(hand)
  g = checktwopair(hand)
  h = checkpair(hand)
  i = checkhighcard(hand)
  if a[0]:
    value = [8, a[1]]
  elif b[0]:
    value = [7, b[1], b[2]]
  elif c[0]:
    value = [6, c[1], c[2]]
  elif d[0]:
    value = [5, d[1][0], d[1][1], d[1][2], d[1][3], d[1][4]]
  elif e[0]:
    value = [4, e[1]]
  elif f[0]:
    value = [3, f[1], f[2], f[3]]
  elif g[0]:
    value = [2, g[1], g[2], g[3]]
  elif h[0]:
    value = [1, h[1], h[2], h[3], h[4]]
  else:
    value = [0, i[0], i[1], i[2], i[3], i[4]]
  return value


def checkstraightflush(hand):
  teststraight = checkstraight(hand)
  if teststraight[0]:
    testflush = checkflush(teststraight[2])
    if testflush[0]:
      return [True, teststraight[1]]
  return [False, 0]


def checkstraight(hand):
  handnumbers = []
  posibilitys = 3
  for i in range(7):
    if handnumbers.count(hand[i][0]) == 0:
      handnumbers.append(hand[i][0])
    else:
      posibilitys -= 1
  handnumbers.sort()
  if handnumbers.count(14) != 0:
    handnumbers.insert(0, 1)
    posibilitys += 1
  worked = False
  startofstraightinhand = 0
  startofstraight = 0
  for i in range(posibilitys):
    if handnumbers[i] + 1 == handnumbers[
        i + 1] and handnumbers[i + 1] + 1 == handnumbers[
            i + 2] and handnumbers[i + 2] + 1 == handnumbers[
                i + 3] and handnumbers[i + 3] + 1 == handnumbers[i + 4]:
      startofstraight = handnumbers[i]
      startofstraightinhand = i
      worked = True
  b = handnumbers[startofstraightinhand:startofstraightinhand + 5]
  outputhand = []
  for i in b:
    for e in range(7):
      if hand[e][0] == i:
        outputhand.append(hand[e].copy())
  return [worked, startofstraight, outputhand]


def checkflush(hand):
  suithand = []
  outputvalues = []
  suits = ('c', 's', 'h', 'd')
  for i in range(len(hand)):
    suithand.append(hand[i][1])
  for i in suits:
    if suithand.count(i) >= 5:
      for e in range(len(hand)):
        if hand[e][1] == i:
          outputvalues.append(hand[e][0])
          outputvalues.sort()
      return [True, outputvalues[-5:]]
  return [False, []]


def checkfullhouse(hand):
  handnumbers = []
  three = 0
  two = 0
  for i in range(7):
    handnumbers.append(hand[i][0])
  for i in range(2, 15):
    if handnumbers.count(i) == 3:
      three = i
  if three == 0:
    return [False, 0, 0]
  for i in range(2, 15):
    if handnumbers.count(i) == 2 and i != three:
      two = i
  if two == 0:
    return [False, 0, 0]
  return [True, three, two]


def checkfourkind(hand):
  handnumbers = []
  for i in range(7):
    handnumbers.append(hand[i][0])
  for i in range(2, 15):
    if handnumbers.count(i) == 4:
      for e in range(4):
        handnumbers.remove(i)
      handnumbers.sort()
      return [True, i, handnumbers[-1]]
  return [False, 0, 0]


def checkthreekind(hand):
  handnumbers = []
  for i in range(7):
    handnumbers.append(hand[i][0])
  for i in range(2, 15):
    if handnumbers.count(i) == 3:
      for e in range(3):
        handnumbers.remove(i)
      handnumbers.sort()
      return [True, i, handnumbers[-1], handnumbers[-2]]
  return [False, 0, 0, 0]


def checktwopair(hand):
  a = checkpair(hand)
  if a[0]:
    b = checkpair(hand, 'twopair', a[5])
    if b[0]:
      return [True, b[1], a[1], b[2]]
  return [False, 0, 0, 0]


def checkpair(hand, type='pair', hand2=[]):
  if type == 'pair':
    handnumbers = []
    for i in range(len(hand)):
      handnumbers.append(hand[i][0])
  else:
    handnumbers = hand2
  for i in range(2, 15):
    if handnumbers.count(i) == 2:
      for e in range(2):
        handnumbers.remove(i)
      handnumbers.sort()
      return [
          True, i, handnumbers[-1], handnumbers[-2], handnumbers[-3],
          handnumbers
      ]
  return [False, 0, 0, 0, 0, []]


def checkhighcard(hand):
  handnumbers = []
  for i in range(7):
    handnumbers.append(hand[i][0])
  handnumbers.sort()
  return [
      handnumbers[-1], handnumbers[-2], handnumbers[-3], handnumbers[-4],
      handnumbers[-5]
  ]


def findbesthand(values):
  bestfoundnumber = [0]
  bestvalue = [0, 0, 0, 0, 0, 0]
  for i in range(len(values)):
    depth = 0
    found = False
    while not found:
      if values[i][depth] > bestvalue[depth]:
        bestvalue = values[i].copy()
        found = True
        bestfoundnumber = [i]
      elif values[i][depth] == bestvalue[depth]:
        depth += 1
        if depth > len(bestvalue):
          bestvalue = values[i].copy()
          bestfoundnumber.append(i)
          found = True
      else:
        found = True
  return bestfoundnumber


smallblind = int(input('How many chips is the small blind? '))
bigblind = smallblind * 2
playerinfo = how_many_players()
playerup = 1
going = True
while going:
  os.system('clear')
  playerinfo = run_hand(playerinfo, playerup)[0]
  os.system('clear')
  toberemoved = []
  for i in range(playerinfo[-1]):
    if playerinfo[i]['chips'] <= 0:
      toberemoved.append(i)
      print('Player ' + str(i + 1) + ' is out. \n')
      print('If your number was greater than ', i+1, ' your number will be one lower. \n')
  toberemoved.sort(reverse=True)
  for i in toberemoved:
    del playerinfo[i]
    playerinfo[-1] -= 1
  if playerinfo[-1] == 1:
    print('Player 1 wins!')
    going = False
    break
  playerup += 1
  if playerup > playerinfo[-1]:
    playerup = 1
  print('Player ' + str(playerup) + ' is up first' + '\n')
  input('Press enter to continue')
  os.system('clear')