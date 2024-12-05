import os
import requests
from collections import defaultdict, deque

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    return response.text.strip()

def parse_input(data):
    # Parse the input into rules and updates
    rules_section, updates_section = data.split("\n\n")
    rules = [tuple(map(int, rule.split("|"))) for rule in rules_section.splitlines()]
    updates = [list(map(int, update.split(","))) for update in updates_section.splitlines()]
    return rules, updates

def is_update_valid(update, rules):
    # Check if an update is in the correct order
    applicable_rules = [rule for rule in rules if rule[0] in update and rule[1] in update]
    index_map = {page: i for i, page in enumerate(update)}
    return all(index_map[x] < index_map[y] for x, y in applicable_rules)

def reorder_update(update, rules):
    # Topological sort to reorder pages
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    pages_in_update = set(update)
    for x, y in rules:
        if x in pages_in_update and y in pages_in_update:
            graph[x].append(y)
            in_degree[y] += 1
            in_degree[x]  # Ensure every page is initialized

    for page in update:
        if page not in in_degree:
            in_degree[page] = 0

    queue = deque([node for node in update if in_degree[node] == 0])
    sorted_order = []

    while queue:
        current = queue.popleft()
        sorted_order.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_order

def compute_reordered_middle_sum(rules, updates):
    # Compute the sum of middle pages for reordered incorrect updates
    total = 0
    for update in updates:
        if not is_update_valid(update, rules):
            corrected_order = reorder_update(update, rules)
            middle_page = corrected_order[len(corrected_order) // 2]
            total += middle_page
    return total

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/5/input"
    input_data = fetch_input(input_url, session_token)
    rules, updates = parse_input(input_data)
    result = compute_reordered_middle_sum(rules, updates)
    print("Sum of middle pages after reordering:", result)

if __name__ == "__main__":
    main()
