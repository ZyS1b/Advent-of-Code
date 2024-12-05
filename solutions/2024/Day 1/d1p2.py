import requests
import os
from collections import Counter

def fetch_input(url, session_token):
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    return response.text.strip()

def calculate_similarity_score(input_data):
    left_list, right_list = zip(*(map(int, line.split()) for line in input_data.splitlines()))
    
    right_count = Counter(right_list)
    
    similarity_score = 0
    for number in left_list:
        similarity_score += number * right_count.get(number, 0)
    
    return similarity_score

def main():
    session_token = os.getenv("AOC_SESSION_TOKEN")
    input_url = "https://adventofcode.com/2024/day/1/input"
    input_data = fetch_input(input_url, session_token)
    result = calculate_similarity_score(input_data)
    print(f"Similarity Score: {result}")

if __name__ == "__main__":
    main()
