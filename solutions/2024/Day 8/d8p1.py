import requests
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    return response.text.strip()

def parse_input(input_data):
    antennas = []
    for y, row in enumerate(input_data.splitlines()):
        for x, char in enumerate(row):
            if char.isalnum():  # Antennas are letters or digits
                antennas.append((x, y, char))
    return antennas

def calculate_antinodes(antennas, grid_width, grid_height):
    antinodes = set()
    grouped_by_frequency = defaultdict(list)

    # Group antennas by their frequency
    for x, y, freq in antennas:
        grouped_by_frequency[freq].append((x, y))

    # Check each frequency group
    for freq, positions in grouped_by_frequency.items():
        n = len(positions)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue

                # Get antenna positions
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Calculate possible midpoint (antinodes)
                dx, dy = x2 - x1, y2 - y1

                # Ensure one antenna is twice as far from the midpoint as the other
                mx1, my1 = x1 - dx, y1 - dy  # Antinode on one side
                mx2, my2 = x2 + dx, y2 + dy  # Antinode on the other side

                # Add valid antinodes within grid boundaries
                if 0 <= mx1 < grid_width and 0 <= my1 < grid_height:
                    antinodes.add((mx1, my1))
                if 0 <= mx2 < grid_width and 0 <= my2 < grid_height:
                    antinodes.add((mx2, my2))

    return antinodes

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/8/input"
    input_data = fetch_input(input_url, session_token)
    antennas = parse_input(input_data)
    grid_width = len(input_data.splitlines()[0])
    grid_height = len(input_data.splitlines())
    antinodes = calculate_antinodes(antennas, grid_width, grid_height)
    print("Total unique antinode locations:", len(antinodes))

if __name__ == "__main__":
    main()
