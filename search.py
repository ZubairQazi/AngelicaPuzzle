#!/usr/bin/env python

import numpy as np
import copy
import hashlib

import time

goal = [['A', 'N', 'G'],
        ['E', 'L', 'I'],
        ['C', 'A', 'X']]

# For the hash function
hash_keys = {'A': 1, 'N': 2, 'G': 3, 'E': 4, 'L': 5, 'I': 6, 'C': 7, 'A': 8, 'X': 9}

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

    while frontier and num_expanded < 50000:
        current = frontier.pop(0)

        # print(current.puzzle == goal)

        if current.puzzle == goal:
            print("Success!")
            print(f'Nodes Expanded: {num_expanded}')
            print(f'Maximum frontier size: {max_frontier_size}')
            return current
        
        # if not goal state, proceed
        frontier, seen = queuing_function(current, frontier, seen, heuristic)

        # update counters
        num_expanded += 1

        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

    return None


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

if __name__ == '__main__':

    depth_24 = [['X', 'C', 'N'],
                ['E', 'I', 'A'],
                ['G', 'L', 'A']]

    # default = [['A', 'N', 'G'],
    #             ['E', 'L', 'I'],
    #             ['C', 'X', 'A']]

    result = search(Node(depth_24, 0, 0), 'misplaced')
    if result is not None:
        print('Solution found at depth: ', result.depth)
    else:
        print('No solution found after 50000 expansions')

# 1: A  2: N  3: G     4: E    5: L    6: I    7: C    8: A     9:X

# depth_20 = [['C', 'A', 'N'],
    #         ['E', 'A', 'L'],
    #         ['I', 'G', 'X']]