import sys
import mxklabs.dimacs  
import argparse
from itertools import chain

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
  dicts = {i:-1 for i in literals} # -1 betekent unassigned. 1 = true. 0 = false, hierin alle literals opslaan + bool
  list_true = [] # hierin opslaan welke literals allemaal true zijn
  list_length = [0] # hierin de lengte van list_true bijhouden voor while loop, kan niet leeg zijn door index error

  # een keer runnen, voor index error
  total_input, list_true = unit_clause(total_input, dicts, list_true)
  remove_clause(total_input, list_true)
  print(len(set(list_true)))
  list_length.append(len(set(list_true)))

  # while there are unit clauses, do unit clause simplification function
  while list_length[-1] != list_length[-2]:
    total_input, list_true = unit_clause(total_input, dicts, list_true)
    remove_clause(total_input, list_true)
    print(len(set(list_true)))
    list_length.append(len(set(list_true)))

#### SIMPLIFICATION RULES ####
# unit clause rule
def unit_clause(total_input, dicts, list_true):
  for i in total_input:
    if len(i) == 1:
      tmp = i[0]
      dicts[tmp] = True
      list_true.append(tmp)
      del i[:] # remove all clauses containing true literal
      total_input = [x for x in total_input if x] 
  return total_input, list_true

def remove_clause(total_input, list_true):
  for true_literal in list_true:
    for clause_list in total_input:
      for index, clause in enumerate(clause_list):
        if clause == true_literal * -1: # remove all opposite forms of the true literal from clauses
          clause_list.pop(index)

if __name__ == "__main__":
    main()


# remove clauses that are in list_true
#def remove_clause(total_input, list_true):
  #for true_literal in list_true:
    #print(list(true_literal))
    #if list(true_literal) in total_input:
      #print('yes')
    # for clause_list in total_input:
    #   for index, clause in enumerate(clause_list):
    #     if clause == true_literal:
    #       print("clause_list=%s, true_literal=%i" % (clause_list, true_literal))
    #       del clause_list[:]
    #       total_input = [x for x in total_input if x]
    #     elif clause == true_literal * -1:
    #       clause_list.pop(index)


#   for i, sub_list in enumerate(total_input):
#     print(i)
#     if list_true[0] in sub_list:
#       del total_input[i]
#       break

  # for true_literal in list_true:
  #   for clause_list in total_input:
  #     for clause in clause_list:
  #       if clause == true_literal:
  #         print("clause_list=%s, true_literal=%i" % (clause_list, true_literal))
  #         del clause_list[:]
  #         total_input = [x for x in total_input if x]        
  #         for sublist in total_input:
  #           for index, item in enumerate(sublist):
  #             if item == true_literal * -1:
  #               sublist.pop(index)
 # return total_input
#print(list_true)

#### DAVIS PUTNAM ####
#### SAT ####
#if len(total_input) == 0:
#  print("Sat")

#     # remove from total_input and delete empty set 
#     i.remove(abs(tmp))
#     total_input=[e for e in total_input if e]
#     for i in list_true:
#       for j in total_input:
#         for k in j:
#           if abs(k) == i:
#             j.remove(k)
# print(list_true)

# unit clause rule
#for i in total_input:
  # unit clause: set key in dict op True
 # if len(i) == 1:
    # create integer from list
  #  tmp = i[0]
    # set on true in dict + add to list_true 
   # dicts[tmp] = True
    #list_true.append(tmp)
    # remove from total_input and delete empty set (ONLY WITH UNIT CLAUSE)
    #i.remove(abs(tmp))
    #total_input=[e for e in total_input if e]
    #for i in list_true:
    #  for j in total_input:
    #    for k in j:
    #      if abs(k) == i:
    #        j.remove(k)
#print(list_true)



#haal true clauses uit total_input


#print(total_input)

# # tautology rule 
# for i in total_input:
#   if len(i) >= 2:
#     tmp = [abs(j) for j in i]
#     # tautology: set key in dict op True
#     if (len(set(tmp)) != len(i)):
#       tmp  = list(set([x for x in tmp if tmp.count(x) > 1]))[0]
#       dicts[tmp] = True
#       list_true.append(tmp)



# print(total_input)  
  
  #for index, value in enumerate(total_input):
  #  for i in value:
  #    if abs(i) == key:
  #      total_input.pop(index)







# # set other literals with same row and column on False --> sudoku specifiek?
# for j in [x for x in range(1, 10) if x != abs(i[0]) % 10]:
# #   tmp = int((str(i[0])[:2]) + str(j))
#   dicts[tmp] = False

#for i in total_input:
#  if len(i) >= 2:
#    tmp = [abs(j) for j in i]
#    if (len(set(tmp)) != len(i)):
          

######## SIMPLIFY ##########
#### Unit clause rule
# def simplify(): 
#   for i in total_input:
#       if len(i) == 1:
#           list_true.append(i)

# #### Tautology rule
#   for i in total_input:
#     if len(i) >= 2:
#       tmp = [abs(j) for j in i]
#       if (len(set(tmp)) != len(i)):
#         list_true.append(list(set([x for x in tmp if tmp.count(x) > 1])))
#   print(list_true)

######## SPLIT ########


#keys = range(111,dimacs1.num_vars+1) # --> het is natuurlijk niet altijd 111, misschien zoeken naar laagste waarde in clauses?
#for i in keys:
#  dicts[i] = "tbd" # --> misschien niet van te voren een dict aanmaken, maar tzt literals in dict stoppen

