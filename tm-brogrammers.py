import time
import csv
import sys
import copy

tm_file = sys.argv[1]
tape_file = sys.argv[2]

#process dfa file
with open(tm_file) as f:
  #title
  line1 = f.readline().strip().split(',')
  name = line1[0]
  num_tapes = int(line1[1])
  #alphabet
  f.readline()
  #states
  f.readline()
  #start state
  start = f.readline().strip()
  #accept states
  accept_reject = f.readline().strip().split(',')
  accept = accept_reject[0]
  reject = accept_reject[1]
  rule_num = 1
  lambdas = []
  for i in range(num_tapes):
    lambdas.append(f.readline().strip().split(','))
  #use dict to store rules with tuple of current state and input as key and
  #next state as value
  rules = {}
  rule_nums = {}
  for line in f:
    #print str(rule_num) + ": " + line.strip()
    rule_num += 1
    rule = line.strip().split(',')
    rules[(rule[0], rule[1])] = [rule[2], rule[3], rule[4]]
    rule_nums[(rule[0], rule[1])] = rule_num

#process inputs
with open(tape_file) as f:
  while True:
    tapes = []
    line = f.readline()
    if not line:
      break
    #read tapes and store in list of lists
    tapes.append(list(line.strip()))
    print "Tape 1:", ''.join(map(str,tapes[0]))
    for i in range(1, num_tapes):
      line = f.readline()
      tapes.append(list(line.strip()))
      print "Tape " + str(i + 1) + ": " + ''.join(map(str,tapes[i]))
    current_state = start
    current_indexes = []
    #start at left for all tapes
    for i in range(num_tapes):
      current_indexes.append(0)
    count = 1
    #simulate machine while it has neither accepted nor rejected
    while current_state != accept and current_state != reject:
      output = []
      output.append(str(count))
      heads_string = ""
      #create string containing all characters under heads
      for i in range(num_tapes):
        heads_string += tapes[i][current_indexes[i]]
      old_state = current_state
      output_head_string = heads_string
      #if no rule for current state and tape position, check for wilccard case
      #if wilcard case does not apply, reject
      if (current_state, heads_string) not in rules:
        success = True
        for state in rules.keys():
          success = True
          for i, letter in enumerate(state[1]):
            if state[0] != current_state or (heads_string[i] != letter and letter != '*'):
              success = False
              break
          if success == True:
            heads_string = state[1]
            break
          success = False
        if success != True:
          print "No rule for current state and input character defined"
          current_state = reject
          break
      #move to next state
      output.append(rule_nums[(current_state, heads_string)])
      current_state = rules[(current_state, heads_string)][0]
      for i in current_indexes:
        output.append(i)
      output.append(old_state)
      for i in output_head_string:
        output.append(i)
      output.append(current_state)
      directions = []
      #for each tape, write and move L, R, or S
      for i in range(num_tapes):
        #write new character on tape if not *
        if rules[(old_state, heads_string)][1][i] != '*':
          tapes[i][current_indexes[i]] = rules[(old_state, heads_string)][1][i]
          output.append(rules[(old_state, heads_string)][1][i])
        else:
          output.append(tapes[i][current_indexes[i]])
        #move left, right, or stay
        direction = rules[(old_state, heads_string)][2][i]
        directions.append(direction)
        if direction == 'L':
          current_indexes[i] -= 1
        elif direction == 'R':
          current_indexes[i] += 1
        #if at end of tape, add blank char
        if current_indexes[i] == len(tapes[i]):
          tapes[i] += '_'
      count += 1
      for i in directions:
        output.append(i)
      #print transition output
      print ','.join(map(str, output))
    if current_state == accept:
      print "Accept"
    else:
      print "Reject"
    #print final tapes
    for i in range(num_tapes):
      tape_string = ''.join(map(str,tapes[i]))
      print "Tape " + str(i + 1) + ": " + tape_string[:tape_string.index('_')]
