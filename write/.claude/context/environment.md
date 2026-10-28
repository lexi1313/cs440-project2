# Vacuum Robot Environment

## Grid Layout
Row 0 is the top row.

|       | col 0 | col 1 | col 2 | col 3 |
|-------|-------|-------|-------|-------|
| row 0 | start | 0     | 0     | 0     |
| row 1 | 0     | X     | 0     | 0     |
| row 2 | 0     | 0     | 0     | 0     |
| row 3 | 0     | -1    | 0     | 10    |

- `start`: robot's starting cell
- `X`: obstacle, the robot cannot enter it
- `-1`: penalty cell
- `10`: goal cell
- `0`: normal cell with no reward

## Coordinate Mapping to AIMA
AIMA's GridMDP uses (x, y), where x = column and y increases upward.
Conversion: x = col, y = 3 - row.

| Cell     | (row, col) | AIMA (x, y) |
|----------|------------|-------------|
| Start    | (0, 0)     | (0, 3)      |
| Obstacle | (1, 1)     | (1, 2)      |
| Penalty  | (3, 1)     | (1, 0)      |
| Goal     | (3, 3)     | (3, 0)      |

GridMDP takes the grid as a list of rows from top to bottom and flips it internally. Use `None` for the obstacle.
- `terminals`: (1, 0), (3, 0)
- `init`: (0, 3)
- Use `-0.04` instead of `0` for normal cells. GridMDP skips 0-reward cells, so with 0s the start state wouldn't exist.

## Actions
- North (0, 1), South (0, -1), East (1, 0), West (-1, 0)
- Moving into a wall or the obstacle leaves the robot in place.

## What the Agent Knows
The agent does not know T or R. It only observes its current state and the reward it receives after each move.
