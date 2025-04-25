# Vacuum Robot

This project solves a random Vacuum World grid using search algorithms such as depth-first search and uniform-cost.

## Example Usage

### Create a random world:

```bash
python3 make_vacuum_world.py 5 7 0.15 3 > world-5x7.txt
```

### Run Uniform-Cost Search:

```bash
python3 planner.py uniform-cost world-5x7.txt
```

### Run Depth-First Search:

```bash
python3 planner.py depth-first world-5x7.txt
```

## Grid Legend
- `_`: Empty cell
- `#`: Blocked cell
- `*`: Dirty cell
- `@`: Robot's starting position

