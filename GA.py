import numpy as np
import random
import matplotlib.pyplot as plt


file=open("Buxey-media.txt")#数据文件
C =47
#读取数据文件
def readfile(file):
    lines=file.readlines()
    n=int(lines[0].strip().split('\t')[0])#工序数
    print("n=",n)
    line_times=lines[1:n+1]
    lines=lines[n+1:-1]#优先关系
    row_times=len(line_times)
    rows=len(lines)#优先关系行数
    e=np.zeros((rows,2))#生成相应大小的零矩阵
    times=[0]*n
    row=0
    row_time=0
    for line in lines:
        line=line.strip().split('\t')
        line=line[0]
        line=line.split(',')
        line=[int(line[0]),int(line[1])]
        e[row,:]=line[:]
        row+=1
    for line in line_times:
        line=line.strip().split('\t')
        j=''
        for i in line:
            j=j+i
        line=int(j)
        times[row_time]=line
        row_time+=1
    relation=np.zeros((n,n))
    #print(relation)
    #print(e)
    for i in range(len(e)):
        a=int(e[i][0])-1
        b=int(e[i][1])-1
        relation[a][b]=1
    return n,relation,times#返回优先关系矩阵和工序时间列表

#自由工序
def freedots(relation,n):
    frees=[]
    for i in range(n):
        if not relation[:,i].any():
            frees.append(i)
    return frees
#产生初始种群
def initial(relation,popsize,n):#n即代表染色体长度也代表relation矩阵的维度
    pop=[]
    for i in range(popsize):
        pop.append([])
        relation_new=relation
        pre_dots=list(range(1,n+1))
        for j in range(n):
            b=len(relation_new[0])
            frees=freedots(relation_new,b)
            if len(frees)==1:
                a=frees[0]
                pop[i].append(pre_dots[a])
                pre_dots.remove(pre_dots[a])
                relation_new=np.delete(relation_new,a,0)
                relation_new=np.delete(relation_new,a,1)
            else:
                a=random.choice(frees)
                pop[i].append(pre_dots[a])
                pre_dots.remove(pre_dots[a])
                relation_new=np.delete(relation_new,a,0)
                relation_new = np.delete(relation_new, a, 1)
    return pop
#计算适应值
def calfitness(pop, times):
    time_fenpei = []  # 各工序时间
    for i in range(len(pop)):
        time_fenpei.append([])
        for j in pop[i]:
            time_fenpei[i].append(times[j - 1])
    def fenpei(job_fenpei, time_gzz, L, T):
        if sum(T) <= C:
            job_fenpei.append(L)
            time_gzz.append(T)
            return job_fenpei, time_gzz
        l = len(L)
        ret = 0
        j = 0
        while True:
            ret += T[j]
            j += 1
            if ret > C:
                break
        fenpei_1 = L[:j-1]
        time_1 = T[:j-1]
        job_fenpei.append(fenpei_1)
        time_gzz.append(time_1)
        return fenpei(job_fenpei, time_gzz, L[j-1:], T[j-1:])
    
    zong_fenpei = []  # 存储所有工作站的任务列表
    zong_time = []  # 存储所有工作站的时间列表
    for i in range(len(pop)):
        job_fenpei = []
        time_gzz = []
        c, d = fenpei(job_fenpei, time_gzz, pop[i], time_fenpei[i])
        zong_fenpei.append(c)
        zong_time.append(d)
    fitnesses = []  # 每条染色体的适应值
    for time_list in zong_time:
        total_time = 0
        for time_sublist in time_list:
            total_time += sum(time_sublist)
        fitness = total_time**2
        fitnesses.append(fitness)
    return zong_fenpei, zong_time, fitnesses


#选择操作
def select(pop,fitnesses):#选择两条染色体
    def cumsum(L):#递归求和
        if L[:-1]==[]:
            return L
        ret=cumsum(L[:-1])
        ret.append(ret[-1]+L[-1])
        return ret
    sum_fitness=sum(fitnesses)
    sel_ratio=[0]
    for i in fitnesses:
        sel_ratio.append(i/(sum_fitness))
    ret=cumsum(sel_ratio)
    sel_pop=[]


    while len(sel_pop)!=2:
        q=random.random()
        for j in range(1,len(ret)-1):
            if ret[j-1]<q<ret[j]:
                sel_pop.append(pop[j-1])
                break
    return sel_pop
#交叉操作
def crossover(sel_pop):
    l=len(sel_pop[0])
    p_1=sel_pop[0]#两个父代
    p_2=sel_pop[1]
    position=random.sample(range(1,l),2)
    position_1=min(position)
    position_2=max(position)
    head_1=p_1[:position_1]
    body_1=p_1[position_1:position_2]
    tail_1=p_1[position_2:]
    body_1_new=[]
    body_1_index=[]
    for i in body_1:
        ind=p_2.index(i)
        body_1_index.append(ind)
    body_1_index.sort()
    for j in body_1_index:
        body_1_new.append(p_2[j])
    child_1=head_1+body_1_new+tail_1
    head_2=p_2[:position_1]
    body_2=p_2[position_1:position_2]
    tail_2=p_2[position_2:]
    body_2_new=[]
    body_2_index=[]
    for i in body_2:
        ind=p_1.index(i)
        body_2_index.append(ind)
    body_2_index.sort()
    for j in body_2_index:
        body_2_new.append(p_1[j])
    child_2=head_2+body_2_new+tail_2
    return child_1,child_2
#变异操作
def mutation(relation,child):
    l=len(child)
    m=random.choice(range(0,l-2))
    pre_dots=list(range(1,l+1))
    front=child[0:m+1]
    fornt_index=[]
    for i in front:
        fornt_index.append(i-1)
    after=child[m+1:]
    relation_new=relation
    relation_new=np.delete(relation_new,fornt_index,0)
    relation_new=np.delete(relation_new,fornt_index,1)
    after_mut=[]
    for i in front:
        pre_dots.remove(i)
    while len(after_mut)!=len(after):
        b=len(relation_new[0])
        frees=freedots(relation_new,b)
        if len(frees)==1:
            a=frees[0]
            after_mut.append(pre_dots[a])
        else:
            a=random.choice(frees)
            after_mut.append(pre_dots[a])
        pre_dots.remove(pre_dots[a])
        relation_new=np.delete(relation_new,a,0)
        relation_new = np.delete(relation_new, a, 1)
    mut_child=front+after_mut
    return mut_child
#最优保留
def celue(pop,times,better_ind):
    fitness=calfitness(pop,times)[2]
    min_fit=min(fitness)
    min_index=fitness.index(min_fit)
    pop[min_index]=better_ind
    return pop
#SALBP-I遗传迭代
def GA (Generation,Pc,Pm,popsize,file):
    n,relation,times=readfile(file)
    pop=initial(relation,popsize,n)
    better_fitness=[]
    better_pop=[]
    better_fenpei=[]
    better_time=[]
    for i in range(Generation):
        pop_new=[]
        zong_fenpei,zong_time,fitnesses=calfitness(pop,times)
        max_fitness=max(fitnesses)
        max_index=fitnesses.index(max_fitness)
        better_fitness.append(max_fitness)
        better_ind=pop[max_index]
        better_pop.append(better_ind)
        better_fenpei.append(zong_fenpei[max_index])
        better_time.append(zong_time[max_index])
        pop.remove(better_ind)
        fitnesses.remove(max_fitness)
        while len(pop_new)!=popsize:
            ret=select(pop,fitnesses)
            p=random.random()
            if p<Pc:
                c1,c2=crossover(ret)
            else:
                c1=ret[0]
                c2=ret[1]
            pop_new.append(c1)
            pop_new.append(c2)
        mut_number=round(Pm*popsize)
        for j in range(mut_number):
            k=random.choice(range(0,popsize))
            mut_child=mutation(relation,pop_new[k])
            pop_new[k]=mut_child
        pop=celue(pop_new,times,better_ind)
    best_fitness=max(better_fitness)
    best_index=better_fitness.index(best_fitness)
    best_pop=better_pop[best_index]
    best_fenpei=better_fenpei[best_index]
    best_time=better_time[best_index]
    # Calculate Production Balance Rate
    total_times = [sum(times) for times in best_time]
    min_time = min(total_times)
    max_time = max(total_times)
    PBR = (min_time / max_time) * 100
    return best_fitness,best_pop,best_fenpei,best_time,better_fitness,pop,PBR




def plot_fitness_curve(better_fitness):
    plt.figure(figsize=(10, 5))
    plt.plot(better_fitness, marker='o', linestyle='-', color='b')
    plt.title('Fitness Curve over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.grid(True)
    plt.show()


def plot_gantt_chart(best_fenpei, best_time):
    plt.figure(figsize=(10, 6))
    colors = plt.cm.tab20(np.linspace(0, 1, len(best_fenpei)))
    for i, (tasks, times) in enumerate(zip(best_fenpei, best_time)):
        start_time = 0
        for task, duration in zip(tasks, times):
            # 绘制条形图
            plt.barh(i, duration, left=start_time, color=colors[task % len(colors)], edgecolor='black')
            # 在条形图中心添加文本标签
            mid_point = start_time + duration / 2  # 计算条形图中点位置
            plt.text(mid_point, i, str(task), ha='center', va='center', color='black', fontweight='bold')
            start_time += duration
    plt.title('Gantt Chart of Task Assignments')
    plt.xlabel('Time')
    plt.ylabel('Workstation')
    plt.yticks(range(len(best_time)), ["Station " + str(i+1) for i in range(len(best_time))])
    plt.show()




if __name__ == "__main__":
    best_fitness, best_pop, best_fenpei, best_time, better_fitness, pop,PBR = GA(100, 0.8, 0.05, 100, file)
    print('最优适应值：', best_fitness)
    print('最优适应值对应的染色体：', best_pop)
    print('工作站数：', len(best_time))
    print('对应的工作站分配：', best_fenpei)
    print('每个工作站的时间：', best_time)
    #print('生产平衡率（PBR）：', PBR)
    for i in range(0,8):
        print("工作站",i+1,"的总时间：",sum(best_time[i]))
    

    # Plotting
    #plot_fitness_curve(better_fitness)
    plot_gantt_chart(best_fenpei, best_time)
















