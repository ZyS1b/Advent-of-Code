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
    """
    Parses the input map into a list of antennas with their positions and frequencies.
    """
    antennas = []
    for y, row in enumerate(input_data.splitlines()):
        for x, char in enumerate(row):
            if char.isalnum():  # Antennas are letters or digits
                antennas.append((x, y, char))
    return antennas

def calculate_resonant_antinodes(antennas, grid_width, grid_height):
    """
    Calculates all unique antinode locations using the updated resonant rules.
    """
    antinodes = set()
    grouped_by_frequency = defaultdict(list)

    # Group antennas by their frequency
    for x, y, freq in antennas:
        grouped_by_frequency[freq].append((x, y))

    # Check each frequency group
    for freq, positions in grouped_by_frequency.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):  # Avoid duplicate comparisons
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Calculate line equation differences
                dx, dy = x2 - x1, y2 - y1

                # Check all positions aligned with the line through these two antennas
                for k in range(-grid_width, grid_width + 1):  # Large enough range
                    mx, my = x1 + k * dx, y1 + k * dy
                    if 0 <= mx < grid_width and 0 <= my < grid_height:
                        antinodes.add((mx, my))

    return antinodes

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/8/input"
    input_data = fetch_input(input_url, session_token)
    antennas = parse_input(input_data)
    grid_width = len(input_data.splitlines()[0])
    grid_height = len(input_data.splitlines())
    antinodes = calculate_resonant_antinodes(antennas, grid_width, grid_height)
    print("Total unique antinode locations:", len(antinodes))

if __name__ == "__main__":
    main()
