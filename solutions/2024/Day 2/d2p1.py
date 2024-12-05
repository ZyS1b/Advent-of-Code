import requests
import os

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    return response.text.strip()

def is_safe_report(report):
    levels = list(map(int, report.split()))
    differences = [abs(levels[i] - levels[i+1]) for i in range(len(levels) - 1)]
    if any(diff < 1 or diff > 3 for diff in differences):
        return False
    is_increasing = all(levels[i] < levels[i+1] for i in range(len(levels) - 1))
    is_decreasing = all(levels[i] > levels[i+1] for i in range(len(levels) - 1))
    return is_increasing or is_decreasing

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/2/input"
    input_data = fetch_input(input_url, session_token)
    reports = input_data.splitlines()
    safe_report_count = sum(1 for report in reports if is_safe_report(report))
    print(f"Number of safe reports: {safe_report_count}")

if __name__ == "__main__":
    main()
