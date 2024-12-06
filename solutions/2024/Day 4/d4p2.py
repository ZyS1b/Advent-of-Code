import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_input(url, session_token):
    headers = {'Cookie': f'session={session_token}'}
    response = requests.get(url, headers=headers)
    return response.text.strip().splitlines()

def count_xmas(data):
    # Counts occurrences of 'X-MAS' shaped as specified in the problem
    rows, cols = len(data), len(data[0])
    count = 0
    _set = {"M", "S"}
    
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if data[r][c] == "A":
                if {data[r - 1][c - 1], data[r + 1][c + 1]} == _set and \
                   {data[r - 1][c + 1], data[r + 1][c - 1]} == _set:
                    count += 1
    return count

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/4/input"
    input_data = fetch_input(input_url, session_token)
    grid = [list(line) for line in input_data]
    result = count_xmas(grid)
    print("Total occurrences of 'X-MAS':", result)

if __name__ == "__main__":
    main()
