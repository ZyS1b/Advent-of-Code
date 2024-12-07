import requests
import os
from dotenv import load_dotenv
from itertools import product

load_dotenv()

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    return response.text.strip()

def parse_input(input_data):
    equations = []
    for line in input_data.splitlines():
        target, numbers = line.split(":")
        target = int(target.strip())
        numbers = list(map(int, numbers.strip().split()))
        equations.append((target, numbers))
    return equations

def evaluate_expression(numbers, operators):
    result = numbers[0]
    for i, operator in enumerate(operators):
        if operator == '+':
            result += numbers[i + 1]
        elif operator == '*':
            result *= numbers[i + 1]
        elif operator == '||':
            # Concatenate digits from left and right inputs
            result = int(f"{result}{numbers[i + 1]}")
    return result

def find_valid_equations(equations):
    total_calibration_result = 0
    for target, numbers in equations:
        n = len(numbers)
        # Generate all combinations of `+`, `*`, and `||` for n-1 positions
        for operators in product(['+', '*', '||'], repeat=n-1):
            if evaluate_expression(numbers, operators) == target:
                total_calibration_result += target
                break  # Stop checking further if a solution is found
    return total_calibration_result

def main():
    input_url = "https://adventofcode.com/2024/day/7/input"
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_data = fetch_input(input_url, session_token)
    equations = parse_input(input_data)
    total_calibration_result = find_valid_equations(equations)
    print(f"Total Calibration Result: {total_calibration_result}")

if __name__ == "__main__":
    main()
