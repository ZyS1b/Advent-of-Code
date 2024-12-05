import re
import requests
import os

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    return response.text.strip()

def calculate_total_multiplication(input_data):
    mul_pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(mul_pattern, input_data)
    total_sum = sum(int(x) * int(y) for x, y in matches)
    return total_sum

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/3/input"
    input_data = fetch_input(input_url, session_token)
    result = calculate_total_multiplication(input_data)
    print(f"Total Sum: {result}")

if __name__ == "__main__":
    main()
