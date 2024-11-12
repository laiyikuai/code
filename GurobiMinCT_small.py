from gurobipy import *

mod=Model('LBP-cycle time')


K=list(range(1,5))      
N=list(range(1,30))     
T = [7, 19, 15, 5, 12, 10, 8, 16, 2, 6, 21, 10, 9, 4, 14,
     7, 14, 17, 10, 16, 1, 9, 25, 14, 14,2, 10, 7, 20]

MP = [(1, 25), (1, 3), (2, 6), (2, 26), (3, 4), (4, 5),
        (5, 13), (5, 8), (6, 8), (7, 25), (7, 9), (7, 12), 
        (8, 11), (9, 10), (10, 14), (10, 15), (11, 17), 
        (12, 15), (13, 17), (14, 16), (15, 19), (16, 18), 
        (17, 20), (18, 22), (19, 21), (20, 23), (21, 22), 
        (22, 23), (23, 24), (23, 28), (24, 29), (25, 29),
        (26, 27), (27, 29), (28, 29)]


a = []
for i in N:
    for k in K:
        a.append((i, k))
  


x=mod.addVars(a,vtype=GRB.BINARY)     

CT=mod.addVar(vtype=GRB.CONTINUOUS)   


mod.modelSense=GRB.MINIMIZE    
mod.setObjective(CT)           




for i, j in MP:
    expr = 0
    for k in K:
        expr += k * x[j, k] - k * x[i, k]
    mod.addConstr(expr >= 0)



for i in N:
    expr = 0
    for k in K:
        expr += x[i, k]
    mod.addConstr(expr == 1)



for k in K:
    expr = 0
    for i in N:
        expr += T[i - 1] * x[i, k]
    mod.addConstr(expr <= CT)



mod.optimize()



print("Optimal Objective Value", mod.objVal)

import matplotlib.pyplot as plt
import matplotlib.patches as patches


assignments = {(i, j): x[i, j].X for (i, j) in a if x[i, j].X > 0.5}

start_times = {}
for j in K:
    time = 0
    for i in N:
        if (i, j) in assignments:
            start_times[(i, j)] = time
            time += T[i - 1]

fig, ax = plt.subplots()
for (i, j), value in assignments.items():
    if value > 0.5:
        start = start_times[(i, j)]
        duration = T[i - 1]
        rect = patches.Rectangle((start, j - 1), duration, 0.6, edgecolor='black', 
                                 facecolor='skyblue')
        ax.add_patch(rect)
        ax.text(start + duration / 2, j - 1 + 0.3, str(i), ha='center', va='center')

ax.set_xlim(0, max(start_times.values()) + max(T))
ax.set_ylim(0, len(K))
ax.set_yticks([k + 0.3 for k in range(len(K))])
ax.set_yticklabels(['Station ' + str(k + 1) for k in range(len(K))])
ax.set_xlabel('Time')
ax.set_ylabel('Workstation')
plt.savefig('gantt_chart.png', dpi=500)
plt.show()





bottleneck_station = None
max_processing_time = 0
for j in K:
    total_processing_time = sum(T[i-1] * x[i,j].x for i in N)
    if total_processing_time > max_processing_time:
        max_processing_time = total_processing_time
        bottleneck_station = j


total_processing_time_all = sum(T[i-1] for i in N)


production_balance_rate = (total_processing_time_all / (len(K) * 
                                    max_processing_time)) * 100

print("Production Balance Rate:", production_balance_rate)

