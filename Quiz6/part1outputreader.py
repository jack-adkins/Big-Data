# Code to analyze the output for Part1
from collections import defaultdict

def average_query_repetitions(file_path):
    sender_query_counts = defaultdict(lambda: defaultdict(int))
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            sender = parts[3]
            query = parts[-1]
            
            sender_query_counts[sender][query] += 1
    
    for sender, queries in sender_query_counts.items():
        total_repetitions = sum(queries.values())
        unique_queries = len(queries)
        average_repetitions = total_repetitions / unique_queries if unique_queries > 0 else 0
        print(f"{sender}: Average repetitions per query = {average_repetitions:.2f}")

# Printing the Average:
average_query_repetitions("part1output.txt")
