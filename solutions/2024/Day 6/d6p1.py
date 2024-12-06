import requests
import os

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text.strip()

def locate_guard(grid):
    # Locate the guard's starting position and direction
    DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in DIRECTIONS:
                return (r, c), grid[r][c]
    return None, None  # Return None if guard is not found

def simulate_guard(grid, starting_position, starting_direction):
    # Simulate the guard's movement on the grid
    DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    TURN_RIGHT = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

    visited = set()
    guard_pos = starting_position
    guard_dir = starting_direction

    while True:
        visited.add(guard_pos)
        r, c = guard_pos
        dr, dc = DIRECTIONS[guard_dir]
        next_pos = (r + dr, c + dc)

        # Check if the guard leaves the map
        if not (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0])):
            break

        # Check the cell in front
        if grid[next_pos[0]][next_pos[1]] == '#':
            # Turn right if there's an obstacle
            guard_dir = TURN_RIGHT[guard_dir]
        else:
            # Move forward
            guard_pos = next_pos

    return len(visited)

def main(session_token):
    input_url = "https://adventofcode.com/2024/day/6/input"
    input_data = fetch_input(input_url, session_token)
    grid = [list(line) for line in input_data.splitlines()]
    
    starting_position, starting_direction = locate_guard(grid)
    result = simulate_guard(grid, starting_position, starting_direction)
    print(f"Distinct positions visited: {result}")

if __name__ == "__main__":
    session_token = os.getenv("AOC_SESSION_TOKEN")
    main(session_token)
