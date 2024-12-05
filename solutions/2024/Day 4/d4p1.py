import requests
import os

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    return response.text.strip().splitlines()

def count_xmas_in_direction(grid, r, c, dr, dc, word_to_find):
    # Counts if 'XMAS' exists starting at (r, c) in direction (dr, dc)
    for i in range(len(word_to_find)):
        nr, nc = r + i * dr, c + i * dc
        if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]) or grid[nr][nc] != word_to_find[i]:
            return False
    return True

def count_xmas(grid, word_to_find):
    # Count occurrences of 'XMAS' in the grid
    count = 0
    directions = [
        (0, 1),  # Right
        (0, -1),  # Left
        (1, 0),  # Down
        (-1, 0),  # Up
        (1, 1),  # Down-right
        (-1, -1),  # Up-left
        (1, -1),  # Down-left
        (-1, 1),  # Up-right
    ]
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            for dr, dc in directions:
                if count_xmas_in_direction(grid, r, c, dr, dc, word_to_find):
                    count += 1
    return count

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/4/input"
    input_data = fetch_input(input_url, session_token)
    word_to_find = "XMAS"
    grid = [list(line) for line in input_data]
    result = count_xmas(grid, word_to_find)
    print("Total occurrences of 'XMAS':", result)

if __name__ == "__main__":
    main()
