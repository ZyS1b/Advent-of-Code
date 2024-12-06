import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    return response.text.strip()

def parse_input(data):
    rules_section, updates_section = data.split("\n\n")
    rules = [tuple(map(int, rule.split("|"))) for rule in rules_section.splitlines()]
    updates = [list(map(int, update.split(","))) for update in updates_section.splitlines()]
    return rules, updates

def is_update_valid(update, rules):
    # Check if an update is in the correct order
    applicable_rules = [rule for rule in rules if rule[0] in update and rule[1] in update]
    index_map = {page: i for i, page in enumerate(update)}
    return all(index_map[x] < index_map[y] for x, y in applicable_rules)

def compute_middle_page_sum(rules, updates):
    # Compute the sum of middle pages from valid updates
    total = 0
    for update in updates:
        if is_update_valid(update, rules):
            middle_page = update[len(update) // 2]
            total += middle_page
    return total

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/5/input"
    input_data = fetch_input(input_url, session_token)
    rules, updates = parse_input(input_data)
    result = compute_middle_page_sum(rules, updates)
    print("Sum of middle pages:", result)

if __name__ == "__main__":
    main()
