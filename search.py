#!/usr/bin/env python

import copy

goal = [['A', 'N', 'G'],
        ['E', 'L', 'I'],
        ['C', 'A', 'X']]

# define a node in the search tree
class Node:
    def __init(self, puzzle, cost, depth):
        self.puzzle = puzzle
        self.cost = cost
        self.depth = depth


# general search algorithm
def search(root: Node, heuristic):
    frontier = [root]
    seen = [root.puzzle]

    max_frontier_size, num_expanded = 0, 0

    while frontier:
        current = frontier.pop()

        if current == goal:
            print("Success!")
            print(f'Nodes Expanded {num_expanded}')
            print(f'Maximum frontier size: {max_frontier_size}')
            return current
        
        # if not goal state, proceed
        frontier.extend(queuing_function(current, frontier, seen, heuristic))

        # update counters
        # TODO: Update max frontier size
        num_expanded += 1


    return None


# expand current node
def queuing_function(current: Node, frontier, seen, heuristic):

    # expand the current node

    children = get_children(current, seen, heuristic)

    return []


# return all valid children of node
def get_children(node: Node, seen, heuristic):

    children = []

    r, c = find(node.puzzle, 0)

    if r > 0:
        puzzle_down = copy.deepcopy(node.puzzle)
        puzzle_down[r][c], puzzle_down[r + 1][c] = puzzle_down[r + 1][c], puzzle_down[r][c]

        if puzzle_down not in seen:
            seen.append(puzzle_down)
            children.append(Node(puzzle_down, get_cost(node.depth + 1, puzzle_down, heuristic), node.depth + 1))

    if r < len(node.puzzle):
        puzzle_up = copy.deepcopy(node.puzzle)
        puzzle_up[r][c], puzzle_up[r - 1][c] = puzzle_up[r - 1][c], puzzle_up[r][c]

        if puzzle_up not in seen:
            seen.append(puzzle_up)
            children.append(Node(puzzle_up, get_cost(node.depth + 1, puzzle_up, heuristic), node.depth + 1))

    if c  > 0:
        puzzle_left = copy.deepcopy(node.puzzle)
        puzzle_left[r][c], puzzle_left[r][c + 1] = puzzle_left[r][c + 1], puzzle_left[r][c]

        if puzzle_left not in seen:
            seen.append(puzzle_left)
            children.append(Node(puzzle_left, get_cost(node.depth + 1, puzzle_left, heuristic), node.depth + 1))
    
    if c  < len(node.puzzle[0]):
        puzzle_right = copy.deepcopy(node.puzzle)
        puzzle_right[r][c], puzzle_right[r][c - 1] = puzzle_right[r][c - 1], puzzle_right[r][c]

        if puzzle_right not in seen:
            seen.append(puzzle_right)
            children.append(Node(puzzle_right, get_cost(node.depth + 1, puzzle_right, heuristic), node.depth + 1))

    return children


# returns index (row, col) of value in puzzle
def find(puzzle, val):
    for i, row in enumerate(puzzle):
        for j, col in enumerate(row):
            if col == val:
                return i, j

    # returns -1 if value is not found
    return -1, -1

def get_cost(node_depth: Node, node_puzzle, heuristic):
    if heuristic == 'uniform':
        return node_depth
    elif heuristic == 'misplaced':
        return node_depth + misplaced_cost(node_puzzle)
    elif heuristic == 'manhattan':
        return node_depth + manhattan_cost(node_puzzle)
    
    return None


# returns the number of misplaced tiles
def misplaced_cost(node_puzzle):
    misplaced_count = 0
    for i, row in enumerate(node_puzzle):
        for j, val in enumerate(row):
            # account for the blank tile
            if val != goal[i][j] and all(v != len(row) for v in (i, j)):
                misplaced_count += 1

    return misplaced_count


# returns the manhattan heuristic evaluation
def manhattan_heuristic(node_puzzle):
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

