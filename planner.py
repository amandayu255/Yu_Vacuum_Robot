import sys
import heapq
from collections import deque

# dictionary storing moves with row and column changes
moves = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
vacuum = 'V'

# reads the grid world from provided file
def read_world(filename):
    with open(filename, 'r') as f:
        cols = int(f.readline().strip())  # number of columns
        rows = int(f.readline().strip())  # number of rows
        grid = [list(f.readline().strip()) for _ in range(rows)] # grid representation

    start = None  # starting position
    dirt = set()  # hold dirt locations
    # find starting position (@) and all dirt locations (*)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                start = (r, c)
            elif grid[r][c] == '*':
                dirt.add((r, c))
    return grid, start, frozenset(dirt)

# checks if a given position is within grid boundaries and not blocked by an obstacle
def is_valid(pos, grid):
    r, c = pos
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != '#'

# generates next possible states from the current position and dirt state
def get_successors(pos, dirt, grid):
    successors = []
    r, c = pos

    # check all four possible move directions
    # cr = change in row, cc = change in column
    for a, (cr, cc) in moves.items():
        new_pos = (r + cr, c + cc)
        if is_valid(new_pos, grid):  # only valid moves
            successors.append((a, new_pos, dirt))

    # vacuum dirt if current cell is dirty and update the dirt state
    if pos in dirt:
        new_dirt = set(dirt)
        new_dirt.remove(pos)
        successors.append((vacuum, pos, frozenset(new_dirt)))

    return successors

# find optimal path to vacuum all dirt spots
def uniform_cost(start, dirt, grid):
    frontier = [(0, start, dirt, [])]  # priority queue sort by cost
    visited = set()
    gen = exp = 0  # counters for nodes generated and expanded

    while frontier:
        cost, pos, dirt, path = heapq.heappop(frontier)
        state = (pos, dirt)

        if state in visited:  # skip visited states
            continue
        visited.add(state)
        exp += 1

        # if no dirt remains
        if not dirt:
            for act in path:
                print(act)
            print(f"{gen} nodes generated")
            print(f"{exp} nodes expanded")
            return

        # add successors to priority queue with updated costs and paths
        for action, new_pos, new_dirt in get_successors(pos, dirt, grid):
            new_state = (new_pos, new_dirt)
            if new_state not in visited:
                gen += 1
                heapq.heappush(frontier, (cost + 1, new_pos, new_dirt, path + [action]))

# find a path (not necessarily optimal) to vacuum all dirt spots
def depth_first(start, dirt, grid):
    stack = [(start, dirt, [])]  # stack
    visited = set()
    gen = exp = 0

    while stack:
        pos, dirt, path = stack.pop()
        state = (pos, dirt)

        if state in visited:  # skip visited states
            continue
        visited.add(state)
        exp += 1

        # if no dirt remains
        if not dirt:
            for act in path:
                print(act)
            print(f"{gen} nodes generated")
            print(f"{exp} nodes expanded")
            return

        # generate successors in reverse order
        for action, new_pos, new_dirt in reversed(get_successors(pos, dirt, grid)):
            new_state = (new_pos, new_dirt)
            if new_state not in visited:
                gen += 1
                stack.append((new_pos, new_dirt, path + [action]))

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [uniform-cost|depth-first] [world-file]")
        return

    algo = sys.argv[1]
    file = sys.argv[2]
    grid, start, dirt = read_world(file)

    if algo == 'uniform-cost':
        uniform_cost(start, dirt, grid)
    elif algo == 'depth-first':
        depth_first(start, dirt, grid)
    else:
        print("Use 'uniform-cost' or 'depth-first'.")

if __name__ == '__main__':
    main()
