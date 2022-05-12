#!/usr/bin/env python

import numpy as np
import copy
import hashlib

import time

## GLOBAL VARS

goal = [['A', 'N', 'G'],
        ['E', 'L', 'I'],
        ['C', 'A', 'X']]

# For the hash function
hash_keys = {'A': 1, 'N': 2, 'G': 3, 'E': 4, 'L': 5, 'I': 6, 'C': 7, 'A': 8, 'X': 9}

# heuristics
heuristics = {'1': 'uniform', '2': 'misplaced', '3': 'manhattan'}


# define a node in the search tree
class Node:
    def __init__(self, puzzle, cost, depth):
        self.puzzle = puzzle
        self.cost = cost
        self.depth = depth


# general search algorithm
def search(root: Node, heuristic):
    frontier = [root]
    seen = {hash_function(root.puzzle): root.puzzle}

    max_frontier_size, num_expanded = 0, 0

    print('Initial State:')
    print(np.array(root.puzzle))
    print()

    while frontier and num_expanded < 150000:
        current = frontier.pop(0)

        # print(current.puzzle == goal)

        if current.puzzle == goal:
            print("Success!")
            print(f'Nodes Expanded: {num_expanded}')
            print(f'Maximum frontier size: {max_frontier_size}')
            return current, num_expanded, max_frontier_size
        
        # if not goal state, proceed
        frontier, seen = queuing_function(current, frontier, seen, heuristic)

        # update counters
        num_expanded += 1

        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

    return None, None, None


# expand current node
def queuing_function(current: Node, frontier, seen, heuristic):

    # expand the current node
    children, seen = get_children(current, seen, heuristic)
    
    frontier.extend(children)

    # sort the list based on overall cost g(n) + h(n) (depth + estimate to goal)
    frontier = sorted(frontier, key=lambda node: node.cost + node.depth)

    print('Hash:',  hash_function(frontier[0].puzzle))

    # output the node to be expanded in the next iterations cost and puzzle
    print(f'We are expanding state with g(n) = {frontier[0].depth} and f(n) = {frontier[0].cost}')
    print(np.array(frontier[0].puzzle))
    print()

    return frontier, seen


# return all valid children of node
def get_children(node: Node, seen, heuristic):

    children = []

    r, c = find(node.puzzle, 'X')

    # move a word down (or empty point up)
    if r < (len(node.puzzle) - 1):
        puzzle_down = copy.deepcopy(node.puzzle)
        puzzle_down[r][c], puzzle_down[r + 1][c] = puzzle_down[r + 1][c], puzzle_down[r][c]

        hash = hash_function(puzzle_down)

        if hash not in seen:
            seen[hash] = puzzle_down
            children.append(Node(puzzle_down, get_cost(puzzle_down, heuristic), node.depth + 1))

    # move a word up (or empty point down)
    if r > 0:
        puzzle_up = copy.deepcopy(node.puzzle)
        puzzle_up[r][c], puzzle_up[r - 1][c] = puzzle_up[r - 1][c], puzzle_up[r][c]

        hash = hash_function(puzzle_up)

        if hash not in seen:
            seen[hash] = puzzle_up
            children.append(Node(puzzle_up, get_cost(puzzle_up, heuristic), node.depth + 1))

    # move a word left (or empty point right)
    if c  < (len(node.puzzle[0]) - 1):
        puzzle_left = copy.deepcopy(node.puzzle)
        puzzle_left[r][c], puzzle_left[r][c + 1] = puzzle_left[r][c + 1], puzzle_left[r][c]

        hash = hash_function(puzzle_left)

        if hash not in seen:
            seen[hash] = puzzle_left
            children.append(Node(puzzle_left, get_cost(puzzle_left, heuristic), node.depth + 1))
    
    # move a word right (or empty point left)
    if c > 0:
        puzzle_right = copy.deepcopy(node.puzzle)
        puzzle_right[r][c], puzzle_right[r][c - 1] = puzzle_right[r][c - 1], puzzle_right[r][c]

        hash = hash_function(puzzle_right)

        if hash not in seen:
            seen[hash] = puzzle_right
            children.append(Node(puzzle_right, get_cost(puzzle_right, heuristic), node.depth + 1))

    return children, seen


## HELPERS

# return a hash of the puzzle
def hash_function(node_puzzle):
    return hashlib.sha1(np.array(node_puzzle).tobytes()).hexdigest()


# locate the empty corner
def find(puzzle, val):
    for i, row in enumerate(puzzle):
        for j, col in enumerate(row):
            if col == val:
                return i, j

    # returns -1 if value is not found
    return -1, -1


def get_cost(node_puzzle, heuristic):
    if heuristic == 'uniform':
        return 0
    elif heuristic == 'misplaced':
        return misplaced_cost(node_puzzle)
    elif heuristic == 'manhattan':
        return manhattan_cost(node_puzzle)
    
    print('Invalid Heuristic')
    return None


## HEURISTICS

def misplaced_cost(node_puzzle):
    misplaced_count = 0
    for i, row in enumerate(node_puzzle):
        for j, val in enumerate(row):
            # account for the blank corner
            if val != goal[i][j] and all(v != len(row) for v in (i, j)):
                misplaced_count += 1

    return misplaced_count


def manhattan_cost(node_puzzle): 
    manhattan_sum = 0
    for i, row in enumerate(node_puzzle):
        for j, val in enumerate(row):
            # return index of value in goal state
            r, c = find(goal, val)
            # ensures that the value was found in the puzzle
            if all(v != -1 for v in (r, c)) and val != 0:
                # sums the manhattan distance of each point
                manhattan_sum += (abs(r - i) + abs(c - j))

    return manhattan_sum


## MENU

# check inputted puzzle validity
def check_validity(puzzle):
    benchmark = np.unique(np.array(goal, dtype=object), return_counts=True)
    input = np.unique(np.array(puzzle, dtype=object), return_counts=True)
    return (benchmark[0] == input[0]).all() and (benchmark[1] == input[1]).all()


def print_menu():
    puzzle = []

    while True:
        print('Welcome to Zubair\'s Angelica Puzzle solver')
        print('Enter your puzzle, use an \'X\' for the blank')

        puzzle.append([ ch.capitalize() for ch in (input('Enter the first row, separate with spaces: ')).split(' ')])
        puzzle.append([ch.capitalize() for ch in (input('Enter the second row, separate with spaces: ')).split(' ')])
        puzzle.append([ch.capitalize() for ch in (input('Enter the third row, separate with spaces: ')).split(' ')])

        # check inputted puzzle for validity
        if not check_validity(puzzle):
            puzzle = []
            print('\nEntered an invalid puzzle, please reinput. See below for example')
            print(np.array(goal))
            print()
            continue
        else:
            break


    print('\nEnter the desired algorithm')
    print('\t1. Uniform Cost Search')
    print('\t2. A* with Misplaced Tile')
    print('\t3. A* with Manhattan Distance\n')

    heuristic = heuristics[input()]

    return puzzle, heuristic


## MAIN

if __name__ == '__main__':

    default = [ ['C', 'A', 'N'],
                ['E', 'A', 'L'],
                ['I', 'G', 'X'] ]

    puzzle, heuristic = print_menu()

    result, _, _ = search(Node(puzzle, 0, 0), heuristic)

    if result is not None:
        print('Solution found at depth: ', result.depth)
    else:
        print('No solution found after 150,000 expansions')