import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_input(url, session_token):
    headers = {'Cookie': f'session={session_token}'}
    response = requests.get(url, headers=headers)
    return response.text.strip()

def calculate_total_sum(input_data):
    mul_enabled = True
    total_sum = 0

    mul_pattern = re.compile(r'mul\((\d+),(\d+)\)')
    do_pattern = re.compile(r'do\(\)')
    dont_pattern = re.compile(r"don't\(\)")

    i = 0
    while i < len(input_data):
        if do_pattern.match(input_data[i:]):
            mul_enabled = True
            i += len("do()")
        elif dont_pattern.match(input_data[i:]):
            mul_enabled = False
            i += len("don't()")
        elif mul_pattern.match(input_data[i:]):
            match = mul_pattern.match(input_data[i:])
            x, y = map(int, match.groups())
            if mul_enabled:
                total_sum += x * y
            i += len(match.group(0))
        else:
            i += 1

    return total_sum

def main():
    session_token = os.getenv('AOC_SESSION_TOKEN')
    input_url = "https://adventofcode.com/2024/day/3/input"
    input_data = fetch_input(input_url, session_token)
    result = calculate_total_sum(input_data)
    print("Total Sum:", result)

if __name__ == "__main__":
    main()
