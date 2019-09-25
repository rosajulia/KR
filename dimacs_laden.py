import sys
import mxklabs.dimacs  
import argparse
import random
import pickle
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
  list_true = [] # hierin opslaan welke literals allemaal true zijn

  # DPLL aanroepen
  value, total_input, list_true = solve(total_input, list_true)
  with open("output_sudoku.txt", "w") as output:
    output.write(str(list_true))

  print(len(set(list_true)))
  print(set(list_true))

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
  while len(min(total_input, key = len, default =[])) == 1:
    for clause in total_input:
      if len(clause) == 1:
        lit = clause[0]
        total_input = rem_unit_clause(total_input, lit)
        list_true = update_list(lit, list_true)
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

  # positive literal
  return (solve(rem_unit_clause(total_input, rand_lit), update_list(rand_lit, list_true)) or
            solve(rem_unit_clause(total_input, rand_lit), update_list(rand_lit, list_true)))

#### SIMPLIFICATION RULES ####
# unit clause rule
def rem_unit_clause(total_input, lit):
  total_input = deepcopy(total_input)
  for clause in copy(total_input):
    if lit in clause: 
      total_input.remove(clause)
    if -lit in clause: 
      clause.remove(-lit)
  return total_input

def update_list(lit, list_true):
  list_true = deepcopy(list_true)
  list_true.append(lit)
  return (list_true)

#### BRANCHING ####
# randomize function
def pick_var_random(total_input):
  x = random.choice(total_input)
  rand_var = random.choice(list(x))
  return rand_var

if __name__ == "__main__":
    main()
