from gurobipy import *

mod=Model('LBP-cycle time')
import time

K=list(range(1,5))      
N=list(range(1,61))     
T = [4,  25,  10,  3,  2,  23,  27,  15,  3,  14,  6,
  30,  5,  7,  13,  17,  1,  12,  16,  25,  13,
  30,  12,  20,  3,  9,  5,  19,  11,  7,  24,
  20,  17,  17,  13,  5,  15,  16,  9,  30,  30,
  8,  24,  14,  23,  16,  7,  3,  15,  17,  7,  1,
  25,  11,  29,  23,  11,  22,  9,  30]
MP =  [(1, 5),  (2, 38),  (3, 55),  (3, 10),  (3, 38),  (4, 53),  (4, 21),
  (4, 8),  (4, 39),  (5, 51),  (5, 38),  (5, 6),  (6, 17),  (6, 37),  (7, 42),
  (8, 10),  (8, 45),  (8, 12),  (8, 44),  (9, 36),  (9, 55),  (9, 48),  (10, 26),
  (10, 58),  (10, 15),  (10, 12),  (11, 46),  (11, 28),  (12, 23),  (12, 31),
  (12, 43),  (12, 53),  (13, 50),  (13, 29),  (13, 30),  (14, 52),  (15, 27),
  (15, 38),  (15, 50),  (16, 27),  (16, 35),  (16, 19),  (17, 26),  (17, 44),
  (17, 42),  (17, 57),  (18, 52),  (18, 41),  (18, 37),  (19, 31),  (20, 57),
  (20, 45),  (20, 28),  (20, 39),  (21, 30),  (21, 22),  (22, 47),  (23, 25),
  (23, 34),  (23, 35),  (24, 58),  (24, 57),  (25, 47),  (25, 55),  (25, 37),
  (26, 43),  (26, 53),  (27, 50),  (27, 60),  (27, 51),  (27, 30),  (28, 33),
  (29, 32),  (29, 46),  (29, 42),  (29, 44),  (30, 46),  (31, 50),  (31, 44),
  (32, 59),  (33, 55),  (33, 34),  (33, 42),  (34, 58),  (34, 37),  (34, 48),
  (35, 38),  (36, 47),  (37, 41),  (38, 49),  (38, 52),  (38, 56),  (39, 45),
  (39, 58),  (39, 55),  (39, 48),  (40, 59),  (40, 44),  (40, 51),  (40, 53),
  (41, 43),  (41, 47),  (41, 46),  (41, 51),  (42, 47),  (42, 54),  (43, 48),
  (43, 53),  (44, 50),  (44, 47),  (44, 55),  (44, 45),  (45, 60),  (46, 50),  (46, 49),
  (46, 52),  (47, 54),  (47, 50),  (47, 57),  (48, 59),  (49, 56),  (49, 59),  (49, 55),
  (50, 57),  (50, 51),  (51, 58),  (51, 60),  (51, 54),  (51, 56),  (52, 56),  (53, 54),
  (53, 58),  (53, 57),  (53, 55),  (54, 57),  (54, 55),  (55, 56),  (55, 57),  (55, 58),
  (56, 57),  (57, 59),  (57, 58),  (58, 60),  (59, 60)]


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

start_time = time.time()  # 开始时间
mod.optimize()
end_time = time.time()  # 结束时间

# 计算运行时间
runtime = end_time - start_time
print(f"Running time: {runtime:.2f} sec")

# 计算每个工序的总时间并找出用时最长的工序
workshop_times = {k: sum(T[i-1] * x[i, k].X for i in N) for k in K}
max_k = max(workshop_times, key=workshop_times.get)
print(f"The bottleneck process is {max_k} ,the time taken is {workshop_times[max_k]:.2f} ")

# 输出最优目标值
print("Optimal Objective Value:", mod.objVal)

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

fig, ax  =plt.subplots()
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

print("Production Balance Rate: %.2f%%" % (production_balance_rate))

