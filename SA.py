import random
import math
import random
from collections import deque
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math
# 任务持续时间
T = [18,  6,  23,  8,  15,  7,  23,  15,  25,  1,  20,  28,  20,  16,
  1,  28,  15,  9,  27,  29,  29,  9,  8,  10,  6,  9,  24,  29,
  21,  19,  10,  9,  11,  6,  26,  17,  21,  19,  24,  11,  26,  7,
  5,  13,  3,  5,  30,  10,  28,  2,  26,  10,  25,  9,  24,  3,
  1,  1,  7,  14,  3,  15,  10,  10,  12,  6,  28,  24,  20,  20,  29,  5,  10,
  28,  19,  22,  19,  13,  8,  21,  2,  25,  1,  9,  2,  29,  16,  27,  5,  12,  13,  1,  12,  14,  21,  15,  29,  26,  5,  15]
MP =  [(1, 76),  (1, 93),  (1, 85),  (2, 89),  (2, 53),  (3, 90),
  (3, 26),  (3, 77),  (4, 53),  (4, 61),  (5, 28),  (6, 83),  (7, 29),  (7, 18),
  (8, 77),  (9, 80),  (9, 32),  (9, 49),  (10, 32),  (10, 59),  (11, 63),
  (11, 22),  (11, 38),  (12, 79),  (12, 18),  (13, 79),  (13, 82),  (14, 51),
  (14, 94),  (14, 57),  (14, 69),  (15, 34),  (15, 93),  (15, 40),  (15, 77),  (16, 29),
  (16, 100),  (16, 59),  (17, 91),  (18, 93),  (19, 41),  (19, 21),
  (19, 100),  (19, 89),  (20, 45),  (21, 86),  (21, 78),  (21, 99),  (22, 73),
  (22, 85),  (22, 60),  (22, 64),  (23, 84),  (23, 37),  (23, 41),  (24, 46),
  (24, 76),  (25, 46),  (26, 40),  (27, 98),  (27, 31),  (27, 73),  (27, 94),  (28, 76),
  (28, 49),  (28, 84),  (29, 68),  (29, 81),  (29, 95),  (30, 45),
  (31, 94),  (31, 63),  (31, 96),  (31, 38),  (32, 42),  (33, 56),  (33, 64),  (34, 41),  (35, 93),  (35, 38),(36, 92),
  (36, 52),  (36, 93),  (37, 89),  (37, 63),  (37, 74),  (38, 91),  (39, 74),
  (39, 45),  (39, 64),  (40, 56),  (40, 50),  (40, 75),  (40, 54),  (41, 88),  (41, 90),  (41, 96),  (42, 68),  (42, 65),
  (42, 61),  (43, 71),  (44, 84),  (44, 48),  (44, 66),  (45, 73),  (45, 49),  (46, 69),
  (46, 96),  (47, 77),  (47, 62),  (48, 54),  (48, 62),  (48, 71),  (48, 97),
  (49, 69),  (49, 80),  (49, 92),  (50, 88),  (51, 76),  (51, 91),  (51, 74),  (51, 89),  (52, 65),
  (52, 54),  (52, 82),  (53, 91),  (53, 65),  (53, 63),  (53, 85),  (54, 67),
  (54, 61),  (55, 61),  (55, 99),  (55, 60),  (56, 69),  (56, 72),  (56, 81),  (56, 85),  (57, 97),  (57, 95),  (58, 71),  (58, 72),  (58, 68),  (58, 80),  (59, 70),  (60, 62),
  (60, 96),  (60, 79),  (60, 70),  (61, 67),  (62, 74),  (62, 66),  (62, 67),
  (63, 94),  (63, 75),  (63, 89),  (64, 90),  (64, 86),  (64, 80),  (64, 99),
  (65, 84),  (65, 93),  (66, 68),  (66, 76),  (66, 81),  (66, 83),
  (67, 87),  (68, 76),  (68, 82),  (69, 80),  (69, 79),  (70, 78),  (70, 100),
  (71, 78),  (71, 97),  (71, 84),  (71, 94),  (72, 77),  (72, 85),  (72, 93),  (72, 75),
  (73, 82),  (74, 85),  (74, 88),  (75, 87),  (76, 95),  (77, 81),  (77, 82),  (77, 87),
  (77, 90),  (78, 86),  (79, 86),  (79, 93),  (80, 88),  (80, 89),  (80, 97),
  (80, 93),  (81, 82),  (81, 90),  (82, 94),  (83, 93),  (83, 95),  (84, 88),
  (84, 100),  (84, 97),  (84, 92),  (85, 100),  (85, 98),  (85, 99),  (86, 88),
  (86, 93),  (86, 94),  (86, 99),  (87, 97),  (87, 100),  (87, 94),  (87, 91),
  (88, 95),  (88, 99),  (88, 90),  (88, 89),  (89, 96),  (89, 93),
  (89, 94),  (90, 99),  (90, 91),  (90, 98),  (91, 100),  (91, 98),
  (92, 97),  (92, 93),  (93, 97),  (93, 98),  (93, 96),  (93, 94),  (94, 98),
  (94, 95),  (95, 99),  (95, 98),  (95, 96),  (96, 99),  (97, 100),
  (97, 99),  (98, 100),  (98, 99),  (99, 100)]

# Initializing tasks and machines
N = list(range(1, 101))  # mission statement
K = list(range(1, 5))   # collection of machines

def topological_sort(N, MP):
    """ Returns the topological ordering of tasks """
    # Initialize the in-degree array
    in_degree = {i: 0 for i in N}
    # Record the successor tasks for each task
    adj_list = {i: [] for i in N}
    
    # Filling in degree arrays and adjacency tables
    for pre, succ in MP:
        adj_list[pre].append(succ)
        in_degree[succ] += 1

    # The queue is used to store all nodes that have an in-degree of 0
    queue = deque([i for i in N if in_degree[i] == 0])
    sorted_list = []

    while queue:
        node = queue.popleft()
        sorted_list.append(node)
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_list) != len(N):
        raise ValueError("Graph has a cycle, which invalidates the topological sort")

    return sorted_list

def initial_solution_with_topology_sort(N, K, MP):
    """ Generate an initial feasible solution using topological sorting """
    sorted_tasks = topological_sort(N, MP)
    solution = {k: [] for k in K}
    
    # Rotate tasks to machines
    k = 0
    for task in sorted_tasks:
        solution[K[k]].append(task)
        k = (k + 1) % len(K)
    return solution

def cost(solution, T, K):
    """Calculate the cost of a given solution"""
    max_time = 0
    for k in K:
        time = 0
        for i in solution[k]:
            time += T[i-1]
        max_time = max(max_time, time)
    return max_time

def validate_sequence(sequence, constraints):
    # Create graph and in-degree dictionary
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Build the graph from the constraints
    for start, end in constraints:
        graph[start].append(end)
        in_degree[end] += 1
    
    # Initialize a queue with all nodes having in-degree 0 (i.e., no prerequisites)
    queue = deque([node for node in set(graph.keys()).union(set(in_degree.keys())) 
                   if in_degree[node] == 0])
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


def is_valid_swap(solution, k1, k2, i1, i2, MP):
    """Check that all preconditions are satisfied after exchanging 
    tasks i1 and i2 between two machines k1 and k2"""
    # Assume that the new solution after the exchange
    temp_solution_k1 = [i2 if x == i1 else x for x in solution[k1]]
    temp_solution_k2 = [i1 if x == i2 else x for x in solution[k2]]
    if validate_sequence(temp_solution_k1, MP) == False:
        return False
    if validate_sequence(temp_solution_k2, MP) == False:
        return False
    else:
        return True  # Returns True if all constraints are satisfied
    

def neighbor(solution, N, K, T, MP):
    """Generate a neighbor solution to the current solution by 
    swapping the positions of the two tasks that are allowed to be swapped"""
    new_solution = {k: solution[k][:] for k in K}
    k1, k2 = random.sample(K, 2)
    if new_solution[k1] and new_solution[k2]:
        i1, i2 = random.choice(new_solution[k1]), random.choice(new_solution[k2])
        # Checking the legality of the exchange
        if is_valid_swap(new_solution, k1, k2, i1, i2, MP):
            new_solution[k1]=[i2 if x == i1 else x for x in solution[k1]]

            new_solution[k2]=[i1 if x == i2 else x for x in solution[k2]]
            return new_solution
    return solution  # If the exchange is not legal, return to the original solution


def calculate_start_times(solution, T, K):
    """计算每个任务的开始时间"""
    start_times = {k: {} for k in K}
    for k in solution:
        current_time = 0
        for i in sorted(solution[k], key=lambda x: solution[k].index(x)):
            start_times[k][i] = current_time
            current_time += T[i-1]
    return start_times


def simulated_annealing(N, K, T, MP, max_iter=1000, initial_temp=100, cooling_rate=0.999):
    current_solution = initial_solution_with_topology_sort(N, K,MP)
    current_cost = cost(current_solution, T, K)
    temperature = initial_temp

    for _ in range(max_iter):
        new_solution = neighbor(current_solution, N, K, T, MP)
        new_cost = cost(new_solution, T, K)
        
        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
            current_solution, current_cost = new_solution, new_cost
        temperature *= cooling_rate

    return current_solution, current_cost



def plot_gantt(solution, T, K, title='Gantt Chart'):
    start_times = calculate_start_times(solution, T, K)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['red', 'green', 'blue', 'purple']
    
    for k in K:
        for i, start in start_times[k].items():
            ax.add_patch(patches.Rectangle((start, k-1), T[i-1], 0.8, color=random.choice(colors)))
            ax.text(start + T[i-1]/2, k - 1 + 0.4, str(i), ha='center', va='center', color='white')

    ax.set_ylim(0, len(K))
    ax.set_xlim(0, max(sum(T[i-1] for i in solution[k]) for k in K))
    ax.set_yticks([k - 0.1 for k in K])
    ax.set_yticklabels(['Machine ' + str(k) for k in K])
    ax.set_xlabel('Time')
    ax.set_title(title)
    plt.gca().invert_yaxis()
    plt.show()
import time
start_time = time.time()  # 开始时间
best_solution = None
best_cost = float('inf')
for _ in range(100):
    final_solution, final_cost = simulated_annealing(N, K, T, MP)
    if final_cost < best_cost:
        best_cost = final_cost
        best_solution = final_solution


end_time = time.time()  # 结束时间

# 计算运行时间
runtime = end_time - start_time
def calculate_bottleneck_process(solution, T, K):
    """Calculate the total processing time for each machine and identify the bottleneck process."""
    workshop_times = {k: sum(T[i-1] for i in solution[k]) for k in K}
    max_k = max(workshop_times, key=workshop_times.get)
    print(f"The bottleneck process is Machine {max_k}, the time taken is {workshop_times[max_k]:.2f} seconds")

def calculate_production_balance_rate(solution, T, K):
    """Calculate and print the production balance rate."""
    workshop_times = {k: sum(T[i-1] for i in solution[k]) for k in K}
    total_processing_time_all = sum(workshop_times.values())
    max_processing_time = max(workshop_times.values())
    production_balance_rate = (total_processing_time_all / (len(K) * max_processing_time)) * 100
    print(f"Production Balance Rate: {production_balance_rate:.2f}%")
# Plotting the Gantt chart for visualization
plot_gantt(best_solution, T, K, title='Final Gantt Chart')

# Output the bottleneck process time and the production balance rate
calculate_bottleneck_process(best_solution, T, K)
calculate_production_balance_rate(best_solution, T, K)

print(f"Overall runtime: {runtime:.2f} seconds")

plot_gantt(best_solution, T, K)