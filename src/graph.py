import csv
from collections import defaultdict

class Graph:
    def __init__(self):
        # Initialize an empty adjacency list for the graph
        self.adj_list = defaultdict(dict)

    def add_edge(self, start, end, distance, time, accessible):
        """Adds an undirected edge between 'start' and 'end' nodes."""
        self.adj_list[start][end] = {
            'distance': distance,
            'time': time,
            'accessible': accessible
        }
        self.adj_list[end][start] = {
            'distance': distance,
            'time': time,
            'accessible': accessible
        }

    def load_from_csv(self, file_path):
        """Loads the graph from a CSV file."""
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    print(row)  # This will print each row of the CSV file
                    start = row['start']
                    end = row['end']
                    try:
                        # Remove commas from the 'distance' field and convert to float
                        distance = float(row['distance'].replace(',', ''))
                        time = float(row['time'])
                        accessible = row['accessible'].lower() == 'true'
                    except ValueError:
                        print(f"Error: Invalid data in row {row}. Skipping this row.")
                        continue
                    self.add_edge(start, end, distance, time, accessible)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"Error: An unexpected error occurred while loading the CSV: {e}")



    def get_neighbors(self, node):
        """Returns the neighbors of the given node."""
        return self.adj_list.get(node, {})

    def has_edge(self, start, end):
        """Checks if an edge exists between 'start' and 'end' nodes."""
        return end in self.adj_list[start]
