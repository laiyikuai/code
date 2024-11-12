from gurobipy import *

mod=Model('LBP-cycle time')
import time

K=list(range(1,5))      
N=list(range(1,101))     
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

