import requests
import os

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    return response.text.strip()

def parse_input(input_data):
    left_list, right_list = zip(*(map(int, line.split()) for line in input_data.splitlines()))
    return list(left_list), list(right_list)

def calculate_total_distance(left_list, right_list):
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)
    return sum(abs(l - r) for l, r in zip(left_sorted, right_sorted))

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/1/input"
    input_data = fetch_input(input_url, session_token)
    left_list, right_list = parse_input(input_data)
    result = calculate_total_distance(left_list, right_list)
    print(f"Total Distance: {result}")

if __name__ == "__main__":
    main()
