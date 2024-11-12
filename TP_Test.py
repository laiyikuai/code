from collections import defaultdict, deque

def validate_sequence(sequence, constraints):
    # Create graph and in-degree dictionary
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Build the graph from the constraints
    for start, end in constraints:
        graph[start].append(end)
        in_degree[end] += 1
    
    # Initialize a queue with all nodes having in-degree 0 (i.e., no prerequisites)
    queue = deque([node for node in set(graph.keys()).union(set(in_degree.keys())) if in_degree[node] == 0])
    # List to hold the topological order
    topo_order = []
    
    # Process the graph
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if topological sort is possible (i.e., all nodes are processed)
    if len(topo_order) != len(set(graph.keys()).union(set(in_degree.keys()))):
        # Cycle detected or not all nodes were processed
        return False
    
    # Create a position map from the topological order
    position = {value: idx for idx, value in enumerate(topo_order)}
    
    # Validate the sequence against the topological order
    for i in range(len(sequence) - 1):
        for j in range(i + 1, len(sequence)):
            if sequence[i] in position and sequence[j] in position:
                if position[sequence[i]] > position[sequence[j]]:
                    return False  # Wrong order in the sequence based on topological sort
    
    return True

# Example data
temp_solution_k1 = [1,6,5,8,18,20,29,4]
MP = [(1, 25), (1, 3), (2, 6), (2, 26), (3, 4), (4, 5), (5, 13), (5, 8), (6, 8), (7, 25),
      (7, 9), (7, 12), (8, 11), (9, 10), (10, 14), (10, 15), (11, 17), (12, 15), (13, 17),
      (14, 16), (15, 19), (16, 18), (17, 20), (18, 22), (19, 21), (20, 23), (21, 22), 
      (22, 23), (23, 24), (23, 28), (24, 29), (25, 29), (26, 27), (27, 29), (28, 29)]

print(validate_sequence(temp_solution_k1, MP))
