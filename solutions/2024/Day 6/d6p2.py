import requests
import os

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text.strip()

def simulate_with_obstruction(grid, obstruction_pos):
    # Direction mappings
    DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    TURN_RIGHT = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

    rows, cols = len(grid), len(grid[0])
    visited_states = set()

    # Copy the grid and add the obstruction
    grid = [list(row) for row in grid]
    grid[obstruction_pos[0]][obstruction_pos[1]] = '#'

    # Find the guard's starting position and direction
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in DIRECTIONS:
                guard_pos = (r, c)
                guard_dir = grid[r][c]
                break

    while True:
        # Record the current state
        state = (guard_pos, guard_dir)
        if state in visited_states:
            # Loop detected
            return True
        visited_states.add(state)

        r, c = guard_pos
        dr, dc = DIRECTIONS[guard_dir]
        next_pos = (r + dr, c + dc)

        # Check if the guard leaves the grid
        if not (0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols):
            return False

        # Check the next cell
        if grid[next_pos[0]][next_pos[1]] == '#':
            # Turn right if there's an obstacle
            guard_dir = TURN_RIGHT[guard_dir]
        else:
            # Move forward
            guard_pos = next_pos

def find_valid_obstruction_positions(grid):
    rows, cols = len(grid), len(grid[0])
    valid_positions = 0

    # Locate the guard's starting position
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in {'^', '>', 'v', '<'}:  # Direction mappings moved here
                guard_start_pos = (r, c)

    # Test every possible empty position
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '.' and (r, c) != guard_start_pos:
                if simulate_with_obstruction(grid, (r, c)):
                    valid_positions += 1

    return valid_positions

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/6/input"
    input_data = fetch_input(input_url, session_token)
    grid = [list(line) for line in input_data.splitlines()]
    
    result = find_valid_obstruction_positions(grid)
    print(f"Number of valid obstruction positions: {result}")

if __name__ == "__main__":
    main()
