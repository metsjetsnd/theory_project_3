import time
import csv
import sys
import copy

fa_file = sys.argv[1]
inputs_file = sys.argv[2]

#process dfa file
with open(fa_file) as f:
  #title
  print f.readline().strip()
  #alphabet
  f.readline()
  #states
  f.readline()
  #start state
  start = f.readline().strip()
  #accept states
  accept = set(f.readline().strip().split(','))
  rule_num = 1
  #use dict to store rules with tuple of current state and input as key and
  #next state as value
  rules = {}
  rule_nums = {}
  for line in f:
    print str(rule_num) + ": " + line.strip()
    rule_num += 1
    rule = line.strip().split(',')
    rules[(rule[0], rule[1])] = rule[2]
    rule_nums[(rule[0], rule[1])] = rule_num

#process inputs
with open(inputs_file) as f:
  for line in f:
    current_state = start
    reject = False
    count = 1
    print "String: " + line.strip()
    for char in line.strip():
      #if tuple of current state and input not in rules dict, assume trap
      #state
      if (current_state, char) not in rules:
        reject = True
        break
      #traverse to next state
      print str(count) + "," + str(rule_nums[(current_state, char)]) + "," + current_state + "," + char + "," + rules[(current_state, char)]
      current_state = rules[(current_state, char)]
      count += 1
    if reject is True or current_state not in accept:
      print "Reject"
    else:
      print "Accept"
