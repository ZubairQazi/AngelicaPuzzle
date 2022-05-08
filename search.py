#!/usr/bin/env python

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

    max_frontier_size, num_expanded = 0, 0

    while frontier:
        current = frontier.pop()

        if current == goal:
            print("Success!")
            print(f'Nodes Expanded {num_expanded}')
            print(f'Maximum frontier size: {max_frontier_size}')
            return current
        
        # if not goal state, proceed
        frontier.extend(queuing_function(current, frontier, heuristic))

    return None


# expand current node
def queuing_function(current: Node, frontier, heuristic):
    return []
