import sys
import mxklabs.dimacs  
import argparse
import random
from itertools import chain
from copy import copy, deepcopy

def main():
  # inladen dicams
  ARGV_LEN = len(sys.argv)
  if ARGV_LEN == 3:
    try:
      # Read the DIMACS file "simple.cnf".
      dimacs1 = mxklabs.dimacs.read(sys.argv[1])
      dimacs2 = mxklabs.dimacs.read(sys.argv[2])
      # Print some stats.
      print("num_vars=%d, num_clauses=%d" % (dimacs1.num_vars, dimacs1.num_clauses))
      print("num_vars=%d, num_clauses=%d" % (dimacs2.num_vars, dimacs2.num_clauses))
    except Exception as e:
      # Report error.
      print(e)
  else:
    if ARGV_LEN > 0:
      print("usage error: {} <file>".format(sys.argv[0]))
    else:
      print("usage error")

  #### DEFINE LIST OF CLAUSES #####
  total_input = dimacs1.clauses + dimacs2.clauses
  literals = list(chain((*total_input))) # alle literals
  #dicts = {i:-1 for i in literals} # -1 betekent unassigned. 1 = true. 0 = false, hierin alle literals opslaan + bool
  list_true = [] # hierin opslaan welke literals allemaal true zijn

  # DPLL aanroepen
  value, total_input, list_true = solve(total_input, list_true)
  print(len(set(list_true)))
  print(set(list_true))
  print(total_input)

def solve(total_input, list_true):
  print("SAT CHECK \n------------")
  if len(total_input) == 0:
    print("sat")
    return True, total_input, list_true

  print("UNSAT CHECK \n------------")
  if [] in total_input:
    print("unsat")
    return False

  print("SIMPLIFY \n------------")
  #list_true = deepcopy(list_true)

  while len(min(total_input, key = len, default =[])) == 1:
    for clause in total_input:
      if len(clause) == 1:
        lit = clause[0]
        total_input, list_true = rem_unit_clause(total_input, lit, list_true)
        print(len(set(list_true)))
  
  print("SAT CHECK \n------------")
  if len(total_input) == 0:
    print("sat")
    return True, total_input, list_true

  print("UNSAT CHECK \n------------")
  if [] in total_input:
    print("unsat")
    return False

  # Split on an arbitrarily decided literal
  print("SPLITTING \n--------------")
  rand_lit = pick_var_random(total_input)
  print("BACKTRACKING \n------------")

  return (solve(rem_unit_clause(total_input, rand_lit, list_true), list_true) or
  solve(rem_unit_clause(total_input, -rand_lit, list_true), list_true))

#### SIMPLIFICATION RULES ####
# unit clause rule
def rem_unit_clause(total_input, lit, list_true):
  total_input = deepcopy(total_input)
  list_true = deepcopy(list_true)
  for clause in copy(total_input):
    if lit in clause: 
      total_input.remove(clause)
      list_true.append(lit)
    if -lit in clause: 
      clause.remove(-lit)
  return total_input, list_true

#### BRANCHING ####
# randomize function
def pick_var_random(total_input):
  #x = [literal for literal, value in dicts.items() if value == -1] # get list of undetermined literals
  x = random.choice(total_input)
  rand_var = random.choice(list(x))
  return rand_var





  # DPLL aanroepen net zo lang tot sat of unsat --> NOG GEEN BACKTRACKING HIERIN
  # while len(total_input) != 0 or [] not in total_input:
  #   print("DPLL")
  #   total_input, dicts, list_true = DPLL(total_input, dicts, list_true)

  #   print("SAT check")
  #   if len(total_input) == 0:
  #     print("sat")
  #     return total_input, dicts, list_true
  #   elif [] in total_input:
  #     print("unsat")
  #     return total_input, dicts, list_true

  # total_input, list_true, dicts = simplify(total_input, list_true, dicts)

  # print("BRANCHING \n------------")
  # dicts, rand_var = pick_var_random(dicts)

  # if solve(total_input_orig, total_input + [[rand_var]], dicts, list_true) is len(total_input) == 0:
  #   return "satisfiable"
  # else:
  #   return (solve(total_input_orig, total_input + [[-rand_var]], dicts, list_true))



  # # simplify
  # print("SIMPLIFY")
  # total_input, list_true, dicts = simplify(total_input, list_true, dicts)

  # # Randomize
  # print("RANDOMIZE")
  # dicts, rand_var = pick_var_random(dicts)
  # #total_input.append([rand_var])

  # # Backtracking
  # print("BACKTRACKING")
  # if solve(total_input_orig, total_input + [[rand_var]], dicts, list_true) is len(total_input) == 0:
  #   return solve(total_input_orig, total_input + [[rand_var]], dicts, list_true)
  # else:
  #   print('not true')
  #   print(total_input_orig)
  #   return solve(total_input_orig, total_input + [[rand_var * -1]], dicts, list_true)
    # rand_var = rand_var * -1
    # print(rand_var)
    # print(total_input_orig)
    # total_input = total_input_orig
    # total_input.append([rand_var])
    # #total_input = total_input_orig.append([rand_var])
    # return solve(total_input_orig, total_input, dicts, list_true)
    
  # if len(total_input) == 0:
  #   print("sat")
  #   return total_input, dicts, list_true
  # elif [] in total_input:
  #   print(total_input)
  #   print("unsat")
  #   return total_input, dicts, list_true



# combine simplify function + randomize function
# def DPLL(total_input, dicts, list_true):
#   # simplify
#   print("SIMPLIFY")
#   total_input, list_true, dicts = simplify(total_input, list_true, dicts)

#   # randomize
#   print("RANDOMIZE")
#   dicts, total_input = pick_var_random(dicts, total_input)

#   return total_input, dicts, list_true





if __name__ == "__main__":
    main()




# remove clauses
# def remove_clause(total_input, list_true):
#   for true_literal in list_true:
#     for clause_list in total_input:
#       for index, clause in enumerate(clause_list):
#         if clause == true_literal * -1: # remove all opposite forms of the true literal from clauses
#           clause_list.pop(index)
#   return total_input, list_true



# combine unit_clause + remove_clause function
# def simplify(total_input, lit):
#   # while there are unit clauses, do unit clause simplification function  
#   while len(min(total_input, key = len)) == 1:
#     total_input = rem_unit_clause(total_input, lit)
#   return total_input 