#!/usr/bin/env python

import numpy as np
import copy

import time

goal = [['A', 'N', 'G'],
        ['E', 'L', 'I'],
        ['C', 'A', 'X']]

# define a node in the search tree
class Node:
    def __init__(self, puzzle, cost, depth):
        self.puzzle = puzzle
        self.cost = cost
        self.depth = depth


# general search algorithm
def search(root: Node, heuristic):
    frontier = [root]
    seen = [root.puzzle]

    max_frontier_size, num_expanded = 0, 0

    while frontier and num_expanded < 50000:
        current = frontier.pop()

        print(np.array(current.puzzle), '\n')

        time.sleep(1)

        if current == goal:
            print("Success!")
            print(f'Nodes Expanded {num_expanded}')
            print(f'Maximum frontier size: {max_frontier_size}')
            return current
        
        # if not goal state, proceed
        frontier = queuing_function(current, frontier, seen, heuristic)

        # update counters
        num_expanded += 1

        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

    return None


# expand current node
def queuing_function(current: Node, frontier, seen, heuristic):

    # expand the current node
    children = get_children(current, seen, heuristic)
    frontier.extend(children)

    # sort the list based on overall cost g(n) (depth) + h(n) (estimate to goal)
    frontier = sorted(frontier, key=lambda node: node.cost + node.depth)

    return frontier


# return all valid children of node
def get_children(node: Node, seen, heuristic):

    children = []

    r, c = find(node.puzzle, 'X')

    if r < (len(node.puzzle) - 1):
        puzzle_down = copy.deepcopy(node.puzzle)
        puzzle_down[r][c], puzzle_down[r + 1][c] = puzzle_down[r + 1][c], puzzle_down[r][c]

        if puzzle_down not in seen:
            seen.append(puzzle_down)
            children.append(Node(puzzle_down, get_cost(puzzle_down, heuristic), node.depth + 1))

    if r > 0:
        puzzle_up = copy.deepcopy(node.puzzle)
        puzzle_up[r][c], puzzle_up[r - 1][c] = puzzle_up[r - 1][c], puzzle_up[r][c]

        if puzzle_up not in seen:
            seen.append(puzzle_up)
            children.append(Node(puzzle_up, get_cost(puzzle_up, heuristic), node.depth + 1))

    if c  < (len(node.puzzle[0]) - 1):
        puzzle_left = copy.deepcopy(node.puzzle)
        puzzle_left[r][c], puzzle_left[r][c + 1] = puzzle_left[r][c + 1], puzzle_left[r][c]

        if puzzle_left not in seen:
            seen.append(puzzle_left)
            children.append(Node(puzzle_left, get_cost(puzzle_left, heuristic), node.depth + 1))
    
    if c > 0:
        puzzle_right = copy.deepcopy(node.puzzle)
        puzzle_right[r][c], puzzle_right[r][c - 1] = puzzle_right[r][c - 1], puzzle_right[r][c]

        if puzzle_right not in seen:
            seen.append(puzzle_right)
            children.append(Node(puzzle_right, get_cost(puzzle_right, heuristic), node.depth + 1))

    return children


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
            # account for the blank tile
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
                # sums the manhattan distance of each tile
                manhattan_sum += (abs(r - i) + abs(c - j))

    return manhattan_sum

if __name__ == '__main__':
    default = [['A', 'N', 'G'],
        ['E', 'L', 'I'],
        ['C', 'X', 'A']]
    

    result = search(Node(default, 0, 0), 'misplaced')
    if result is not None:
        print('Solution found at depth: ', result.depth)
    else:
        print('No solution found after 50000 expansions')

