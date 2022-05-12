#!/usr/bin/env python

import matplotlib.pyplot as plt

from IPython.utils import io

from search import search, Node

depth_24 = [['X', 'C', 'N'],
            ['E', 'I', 'A'],
            ['G', 'L', 'A']]

depth_20 = [['C', 'A', 'N'],
            ['E', 'A', 'L'],
            ['I', 'G', 'X']]

depth_16 = [['A', 'I', 'C'],
            ['L', 'X', 'G'],
            ['E', 'A', 'N']]

depth_12 = [['A', 'G', 'I'],
            ['L', 'X', 'C'],
            ['E', 'A', 'N']]

depth_08 = [['A', 'G', 'I'],
            ['L', 'X', 'N'],
            ['E', 'C', 'A']]

depth_04 = [['A', 'N', 'G'],
            ['L', 'X', 'I'],
            ['E', 'C', 'A']]

depth_00 = [['A', 'N', 'G'],
            ['E', 'L', 'I'],
            ['C', 'A', 'X']]

heuristics = ['uniform', 'misplaced', 'manhattan']

X = [0, 4, 8, 12, 16, 20, 24]

puzzles = [depth_00, depth_04, depth_08, depth_12, depth_16, depth_20, depth_24]

if __name__ == '__main__':

    all_expansions, all_frontier_sizes = [], []
    for heur in heuristics:
        nodes_expanded, frontier_sizes = [], []
        # get variables for all puzzles with heuristic
        for idx, puzzle in enumerate(puzzles):
            print(f'Running puzzle with solution @ depth {idx * 4} with {heur} heuristic')
            with io.capture_output() as captured:
                result, exp_count, front_size = search(Node(puzzle, 0, 0), heur)
            print(f'\tNodes expanded: {exp_count}, Maximum frontier size: {front_size}', '\n')
            nodes_expanded.append(exp_count)
            frontier_sizes.append(front_size)

        all_expansions.append(nodes_expanded)
        all_frontier_sizes.append(frontier_sizes)
    
    plt.subplot(2, 1, 1)
    for idx, expansions in enumerate(all_expansions):
        plt.plot(X, expansions, label=heuristics[idx])
    
    plt.xticks(X)
    plt.title('Nodes Expanded vs. Solution Depth')
    plt.legend()

    plt.subplot(2, 1, 2)
    for idx, front_size in enumerate(all_frontier_sizes):
        plt.plot(X, front_size, label=heuristics[idx])
    
    plt.xticks(X)
    plt.title('Max Queue Size vs. Solution Depth')
    plt.legend()

    plt.tight_layout()
    plt.show()

    plt.savefig('results')

