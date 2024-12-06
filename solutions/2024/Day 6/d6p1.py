import requests
import os

# Direction mappings
DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
TURN_RIGHT = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

# Fetch input from Advent of Code
def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text.strip()

def simulate_guard(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()

    # Locate the guard's starting position and direction
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in DIRECTIONS:
                guard_pos = (r, c)
                guard_dir = grid[r][c]
                break

    while True:
        visited.add(guard_pos)
        r, c = guard_pos
        dr, dc = DIRECTIONS[guard_dir]
        next_pos = (r + dr, c + dc)

        # Check if the guard leaves the map
        if not (0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols):
            break

        # Check the cell in front
        if grid[next_pos[0]][next_pos[1]] == '#':
            # Turn right if there's an obstacle
            guard_dir = TURN_RIGHT[guard_dir]
        else:
            # Move forward
            guard_pos = next_pos

    return len(visited)

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/6/input"
    input_data = fetch_input(input_url, session_token)
    grid = [list(line) for line in input_data.splitlines()]
    result = simulate_guard(grid)
    print(f"Distinct positions visited: {result}")

if __name__ == "__main__":
    main()
