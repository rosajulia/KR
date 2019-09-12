#!/usr/bin/env python
# Name: Minne Schepers and Julia Jelgerhuis
# Student number: 
"""
This script solves sudoku problems based on the Boolean Satisfiability (SAT) solver. 
"""
import argparse
import numpy as np

def main():
    # initialize command-line arguments
    parser = argparse.ArgumentParser(description='SAT solver')
    parser.add_argument('SAT', type=int, help="SAT strategies: 1, 2, 3 [default: 1]")
    parser.add_argument('rules', type=argparse.FileType('r', encoding='UTF-8'), help='CNF rules for sudoku')
    parser.add_argument('sudoku', type=argparse.FileType('r', encoding='UTF-8'), help='Sudoku file')    
    args = parser.parse_args()

    # show values
    print("Strategy: %i" % args.SAT)
    print("Inputfile: %s" % args.rules.name)
    print("Sudoku file: %s" % args.sudoku.name)

    # make empty matrix
    sudoku = np.zeros(shape=(9,9))
    #print(sudoku)

    #print(args.sudoku.readlines()) #--> checken of die text file kan lezen
    # gegeven sudoku inlezen in lege sudoku
    for row in args.sudoku:
        r = int(row[0])-1
        c = int(row[1])-1
        v = int(row[2])
        sudoku[r,c] = v
    print(sudoku)

if __name__ == "__main__":
    main()


#'C:\Users\julia\Documents\School\Artificial Intelligence\Jaar 1\Knowledge Representation\SAT solver\sudoku-rules.txt'

