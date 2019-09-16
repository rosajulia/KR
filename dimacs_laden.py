import sys
import mxklabs.dimacs  
import argparse

if __name__ == "__main__":
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

##### CREATE DICT OF LITERALS #####
# dict maken waarin je alle mogelijke literals opslaat en een boolean waarde geeft
dicts = {}
keys = range(111,1000)
for i in keys:
  dicts[i] = "tbd"

#### DEFINE LIST OF CLAUSES #####
total_input = dimacs1.clauses + dimacs2.clauses

#### Unit clause rule + tautology rule ####
for i in total_input:
  if len(i) == 1:
    dicts[i[0]] = True
    for j in [x for x in range(1, 10) if x != abs(i[0]) % 10]:
      tmp = int((str(i[0])[:2]) + str(j))
      dicts[tmp] = False
      
for i in total_input:
  if len(i) >= 2:
    tmp = [abs(j) for j in i]
    if (len(set(tmp)) != len(i)):
      dicts[list(set([x for x in tmp if tmp.count(x) > 1]))[0]] = True
      for j in [x for x in range(1, 10) if x != abs(i[0]) % 10]:
        tmp = int((str(i[0])[:2]) + str(j))
        dicts[tmp] = False
  
print(dicts)



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



