# Knowledge Representation
Minne Schepers and Julia Jelgerhuis <br />
SAT Solver <br />
Building a SAT solver and use it to solve Sudoku problems.

## Framework of code
The framework of our code is as follows:
* Input arguments: clauseset, heuristic
* Davis–Putnam–Logemann–Loveland (DPLL) algorithm:
- Simplification function
- Splitting function
- Recursive backtracking
* Several branching heuristics for the splitting function:
- Random
- Jeroslaw-Wang one-sided
- Jeroslaw-Wang two-sided
- Dynamic Largest Individual Sum
- Dynamic Largest Combined Sum

## Use of program
**Input**<br />
Usage: SATsolver.py [-h [int]] [input1] [input2]<br />
<br />
Command-line arguments:<br />
* [h], [--heuristic]: Define which branching heuristic you want to use: 1; random, 2; JW one-sided, 3; JW two-sided, 4; DLCS, 5; DLIS [default: 1]
* [input1]: Filepath to CNF file, in this case sudoku-rules. At least one inputfile is required.
* [input2]: Filepath to CNF file, in this case sudoku-example. At least one infputfile is required. 
<br />

**Output**<br />
When the problem is satisfiable, a text file will be produced with the solution. Furthermore, a CSV file will be made consisting of the name of the input file, branching heuristic that was used, and some metrics of the algorithm (splits, simplify, backtracking). When the problem is unsatisfiable, no files will be made and the code will return "UNSAT".
