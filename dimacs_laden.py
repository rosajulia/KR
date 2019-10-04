import sys
import mxklabs.dimacs  
import argparse
import random
import os
from itertools import chain
from copy import copy, deepcopy
from collections import Counter 
import csv


def main():
  # inladen dicams
  ARGV_LEN = len(sys.argv)
  if ARGV_LEN == 4:
    try:
      # Read the DIMACS file "simple.cnf" + heuristic
      dimacs1 = mxklabs.dimacs.read(sys.argv[1])
      dimacs2 = mxklabs.dimacs.read(sys.argv[2])
      heuristic = int(sys.argv[3])
      # Print some stats
      print("num_vars=%d, num_clauses=%d" % (dimacs1.num_vars, dimacs1.num_clauses))
      print("num_vars=%d, num_clauses=%d" % (dimacs2.num_vars, dimacs2.num_clauses))
    except Exception as e:
      # Report error
      print(e)
  else:
    if ARGV_LEN > 0:
      print("usage error: {} <file>".format(sys.argv[0]))
    else:
      print("usage error")
  
  # define heuristic and add name to list
  if heuristic == 1:
    heuristicName.append("random")
  elif heuristic == 2:
    heuristicName.append("JW one-sided")
  elif heuristic == 3:
    heuristicName.append("JW two-sided")
  elif heuristic == 4:
    heuristicName.append("DLCS")
  elif heuristic == 5:
    heuristicName.append("DLIS")
  # Initialize command-line arguments
  # parser = argparse.ArgumentParser(description="SAT solver")
  # parser.add_argument("heuristic", type=int, help="SAT strategies: 1; random, 2;\
  #   JW one-sided, 3; JW two-sided, 4; DLCS, 5; DLIS [default: 1]")
  # parser.add_argument("input1", type=argparse.FileType("r", encoding="UTF-8"),\
  #   help="Filepath rules for sudoku")
  # parser.add_argument("input2", type=argparse.FileType("r", encoding="UTF-8"),\
  #   help="Filepath Sudoku file")    
  # args = parser.parse_args()

  # print("Thanks for using our SAT solver!\nYou chose strategy {}\nInputfile:\
  #   \n{}\n{}".format(args.heuristic, args.input1.name, args.input2.name))
  
  # Read dimacs files and print stats --> verwijzen naar Rick
  # dimacs1 = mxklabs.dimacs.read(args.input1.name)
  # dimacs2 = mxklabs.dimacs.read(args.input2.name)
  # print("Some DIMACS statistics:\nDimacs 1: numVars = {}, numClauses = {}\n\
  #   Dimacs 2: numVars = {}, numClauses = {}".format(dimacs1.num_vars,\
  #     dimacs1.num_clauses, dimacs2.num_vars, dimacs2.num_clauses))
  
  # Concatenate inputfiles
  totalInput = dimacs1.clauses + dimacs2.clauses

  # Define chosen heuristic and list to store true literals
  #heuristic = int(args.heuristic)
  listTrue = [] 

  # Call DPLL function
  DPLL(totalInput, listTrue, heuristic)
  output_tup = (sys.argv[2], heuristicName[0], len(splits), len(simplification), len(backtracking))
  with open("output_SATsolver.csv","a", newline="") as out:
    csv_out=csv.writer(out)
    #for row in output_tup:
    csv_out.writerow(output_tup)
  print(output_tup)
  print("Finished!\nHeuristic = {}\nSplits = {}\nSimplification steps = {}\nBacktracking steps = {}"\
    .format(heuristicName[0], len(splits), len(simplification), len(backtracking)))

def DPLL (totalInput, listTrue, heuristic):
  # Check once for tautology in the clauseset
  tautology(totalInput)
  # Execute DPLL algorithm with heuristic specified
  solve(totalInput, listTrue, heuristic)

def solve(totalInput, listTrue, heuristic):
  # Simplify 
  simplification.append(1)

  # Unit propagation and unit clause removal
  while len(min(totalInput, key = len, default =[])) == 1:
    for clause in totalInput:
      if len(clause) == 1:
        lit = clause[0]
        newTotalInput = RemUnitClause(totalInput, lit)
        newListTrue = UpdateList(lit, listTrue)
        print(len(set(listTrue)))
  
  # Satisfiability check
  if len(totalInput) == 0:
    with open("output_SATsolver.txt", "w") as output:
      output.write(str([n for n in set(listTrue) if n > 0]))
    return "SAT"
  elif [] in totalInput:
    return "UNSAT"

  # Deepcopy and copy variables for backtracking
  newTotalInput = deepcopy(totalInput)
  newListTrue = copy(listTrue)

  # Pick a heuristic based on input argument
  # Choose random literal based on heuristic
  if heuristic == 1:
    randLit = rand(newTotalInput)
  elif heuristic == 2:
    randLit = JW_OS(newTotalInput)
  elif heuristic == 3:
    randLit = JW_TS(newTotalInput)
  elif heuristic == 4:
    randLit = DLCS(newTotalInput)
  elif heuristic == 5:
    randLit = DLCS(newTotalInput)
  else:
    return "Not a valid heuristic"
  splits.append(randLit)

  # Unit propagation and unit clause removal with random literal
  RemUnitClause(newTotalInput, randLit)
  UpdateList(randLit, newListTrue)

  # Recursively execute DPLL
  # Check satisfiability 
  if solve(newTotalInput, newListTrue, heuristic) == "UNSAT":
    backtracking.append(1)
    newTotalInput = deepcopy(totalInput)
    newListTrue = copy(listTrue)
    # If unsatisfiable, change polarity of random literal
    if solve(RemUnitClause(newTotalInput, -randLit), UpdateList(-randLit,\
      newListTrue), heuristic) == "UNSAT":
      return "UNSAT"
    else:
      return "SAT"
  else:
    return "SAT"  

#### SIMPLIFICATION RULES ####
# Unit propogation
def RemUnitClause(totalInput, lit):
  for clause in copy(totalInput):
    if lit in clause: 
      # Remove all unit clauses 
      totalInput.remove(clause)
    if -lit in clause: 
      # Remove all instances of literal
      clause.remove(-lit)
  return totalInput

def UpdateList(lit, listTrue):
  # Keep track of true literals
  listTrue.append(lit)
  return (listTrue)

def tautology(totalInput):
  # Check if clauseset contains tautologies
  # Remove clauses with tautologies
  for clause in copy(totalInput):
    for lit in clause:
      if -lit in clause:
        RemUnitClause(totalInput, lit)
  return totalInput

#### BRANCHING ####
def rand(totalInput):
  # Random heuristic
  # Pick random literal from clauseset
  x = random.choice(totalInput)
  randLit = random.choice(list(x))
  return randLit

def JW_OS (totalInput):
  # One-sided Jeroslaw-Wang heuristic
  # Pick a literal based on their polarity
  counter = {}
  for clause in totalInput:
      for lit in clause:
          if lit in counter:
              counter[lit] = 2 ** -len(clause) + counter[lit]
          else:
            counter[lit] = 2 ** -len(clause)
  if len(counter) > 0:
    randLit = random.choice(list(counter.keys()))
  return randLit

def JW_TS (totalInput):
  # Two-sided Jeroslaw-Wang heuristic
  # Same as one-sided, but add negative and positive polarities together
  counter = {}
  for clause in totalInput:
      for lit in clause:
          if lit in counter:
              counter[abs(lit)] = 2 ** -len(clause) + counter[abs(lit)]
          else:
            counter[abs(lit)] = 2 ** -len(clause)
  if len(counter) > 0:
    randLit = random.choice(list(counter.keys()))
  return randLit

def DLCS(totalInput):
  # Dynamic Largest Combined Sum
  # Pick an abs(literal) based on their occurence in clauseset
  literals = list(chain((*totalInput)))
  occurenceCount = Counter([abs(lit) for lit in literals])
  mostCommon = occurenceCount.most_common(1)[0][0] 

  totalPositive = literals.count(mostCommon)
  totalNegative = literals.count(-mostCommon)

  if totalPositive >= totalNegative:
    randLit = mostCommon
  else:
    randLit = -mostCommon
  
  return randLit

def DLIS(totalInput):
  # Dynamic Largest Individual Sum
  # Pick a literal based on their occurence in clauseset
  literals = list(chain((*totalInput)))
  occurenceCount = Counter(literals)
  mostCommon = occurenceCount.most_common(1)[0][0] 

  totalPositive = literals.count(mostCommon)
  totalNegative = literals.count(-mostCommon)

  if totalPositive >= totalNegative:
    randLit = mostCommon
  else:
    randLit = -mostCommon
  
  return randLit

if __name__ == "__main__":
  global splits
  splits = []

  global simplification
  simplification = []

  global backtracking
  backtracking = []

  global heuristicName
  heuristicName = []

  main()