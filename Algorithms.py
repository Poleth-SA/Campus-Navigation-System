# Algorithm implementations of BFS, DFS and Dijkstra's Algorithm

from collections import deque
import heapq

#BFS Algorithm
#Find the shortest path by the number of edges(Stops)
def bfs_path(graph, start, goal):
    queue = deque([(start, [start])])  # Initialize a queue with the start node and its path
    visited = set()  # Initialize an empty set to keep track of visited nodes

    while queue:  # Continue until the queue is empty
        current, path = queue.popleft()  # Remove and return the first item from the queue
        if current == goal:  # If the current node is the goal
            return path  # Return the path
        if current not in visited:  # If the current node has not been visited
            visited.add(current)  # Mark the current node as visited
            for neighbor in graph.neighbors(current):  # Iterate through the current node's neighbors
                if neighbor not in visited:  # If the neighbor has not been visited
                    queue.append((neighbor, path + [neighbor]))  # Add the neighbor and its path to the queue

    return None

# DFS Algorithm
# To explore all possible paths and perhaps find path with specific characteristics
def dfs_path(graph, source, target):
    stack = [(source, [source])]  # Initialize a stack with the source node and its path
    visited = set()  # Initialize an empty set to keep track of visited nodes

    while stack:  # Continue until the stack is empty
        (vertex, path) = stack.pop()  # Pop a node and its path from the stack
        if vertex not in visited:  # If the node has not been visited
            if vertex == target:  # If the node is the target
                return path  # Return the path
            visited.add(vertex)  # Mark the node as visited
            for neighbor in graph[vertex]:  # Iterate through the node's neighbors
                if neighbor not in visited:  # If the neighbor has not been visited
                    stack.append((neighbor, path + [neighbor]))  # Add the neighbor and its path to the stack

    return None  # Return None if no path is found


#Dijkstra's Algorithm
# for pathfinidng based on edge weigths lke distace or time
def dijkstra_path(graph, start, goal):
    min_heap = []  # Initialize an empty min-heap
    heapq.heappush(min_heap, (0, start, [start]))  # Add the start node and its path to the min-heap with a weight of 0

    visited = set()  # Initialize an empty set to keep track of visited nodes

    while min_heap:  # Continue until the min-heap is empty
        current_weight, current, path = heapq.heappop(min_heap)  # Remove and return the item with the smallest weight from the min-heap
        if current == goal:  # If the current node is the goal
            return path  # Return the path
        if current not in visited:  # If the current node has not been visited
            visited.add(current)  # Mark the current node as visited
            for neighbor, weight in graph[current].items():  # Iterate through the current node's neighbors and their weights
                if neighbor not in visited:  # If the neighbor has not been visited
                    heapq.heappush(min_heap, (current_weight + weight['weight'], neighbor, path + [neighbor]))  # Add the neighbor and its path to the min-heap with the updated weight

    return None  # Return None if no path is found