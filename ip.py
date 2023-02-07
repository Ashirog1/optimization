from ortools.linear_solver import pywraplp
import sys


M = 10000 # random large number
# Create a linear solver
solver = pywraplp.Solver('DialAndRide', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
# print('Done')

m = 1
n, cap = map(int, sys.stdin.readline().strip().split())
#Q =  list(map(int, f.readline().strip().split()))
Q = list()
Q.append(cap)
T = []
for i in range(2*n+1):
    l = list(map(int, sys.stdin.readline().strip().split()))
    l.append(l[0])
    T.append(l)
T.append([M]*(2*n+2))
    # print(n, Q, T)

# print(T) 
# print(n)
customers = [i for i in range(0, 2*n+2)]
vehicles = [i for i in range(0, m)]
start = 0
end = 2*n+1
P = range(1, n+1)
D = range(n+1, 2*n+1)
PD = range(1,2*n+1)
# print(customers)
# Define variables
load = [0] * len(customers)
for i in P :
    load[i] = 1
    load[i+n] = -1
# print('load', load)
x = {}
q = {}
b = {}
t = [[1 for i in customers] for j in customers]
for i in customers:
    for j in customers:
        for k in vehicles:
            x[i, j, k] = solver.IntVar(0, 1, 'x[%d,%d,%d]' % (i, j, k))

for i in customers:
    for k in vehicles:
        q[i, k] = solver.IntVar(0, solver.infinity(), 'q[%d,%d]' % (i, k))
# time variable
for i in customers:
    for k in vehicles:
        b[i, k] = solver.IntVar(0, solver.infinity(), 'b[%d,%d]' % (i, k))
# Served exactly one
for i in P:
    solver.Add(sum(x[i, j, k] for j in customers for k in vehicles) == 1)

# for k in vehicles:
#     solver.Add(sum(q[i, k] for i in customers) <= Q[k])


for i in customers:
    for j in customers:
        for k in vehicles:
            solver.Add(q[j, k] >= (q[i, k] + load[j]) - M * (1- x[i, j, k]))

#print(Q, 'Q')
for k in vehicles :
    for i in P :
        solver.Add(q[i, k] <= Q[k])


for i in PD:
    solver.Add(sum(x[i,i,k] for k in vehicles)==0)

# Must start at 0
for k in vehicles:
    solver.Add(sum(x[0, j, k] for j in PD)<=1)
# go to pick-up points first
for k in vehicles:
    solver.Add(sum(x[0, j, k] for j in D)==0)


# Balance
for i in PD:
    for k in vehicles:
        solver.Add(sum(x[i, j, k] - x[j, i, k] for j in customers) == 0)

# i to i+n
for i in P:
    for k in vehicles:
        solver.Add(sum(x[i,j,k]-x[i+n,j,k] for j in customers)==0)


# The vehicles must end at virtual ending point
for k in vehicles:
    solver.Add(sum(x[i, end, k] for i in range(0, 2*n+1)) == 1)

# The vehicles must not go from the end
for k in vehicles:
    solver.Add(sum(x[end, i, k] for i in customers) == 0)

# Add time variable
for k in vehicles :
    for i in P :
        solver.Add(b[i, k] - b[i+n, k] <= 0)
for i in customers:
    for j in customers:
        for k in vehicles:
            solver.Add(b[j, k] >= (b[i, k] + 1) - M * (1- x[i, j, k]))

solver.set_time_limit(60*1000)

# Define objective function
solver.Minimize(sum(T[i][j] * x[i, j, k] for i in customers for j in customers for k in vehicles))

# Solve the problem
status = solver.Solve()

if (status == solver.INFEASIBLE):
    print(0)
else:
    print(int(solver.Objective().Value()))

# print(solver.Objective().Value())

# Get the solution
go = [0] * (2*n+2)
ans = 0
for i in customers:
    for j in customers:
        for k in vehicles:
            if x[i, j, k].solution_value() == 1:
                # print(T[i][j] * x[i, j, k].solution_value())
                ans += T[i][j] * x[i, j, k].solution_value()
                # print('Vehicle %d is traveling from location %d to location %d' % (k, i, j))
                go[i] = j

with open("result.txt", "w") as w:
    pass
    # print(n, file=w)
    # u = 0
    # while u != 2*n+1:
    #     u = go[u]
    #     if u!=2*n+1:
    #         print(u, file=w, end=' ')


# print('Optimal value: ', ans)

'''
for i in customers:
    for k in vehicles:
        if q[i, k].solution_value() > 0:
            print([i, k], q[i,k].solution_value())
            print('Customer %d is picked up by vehicle %d with load %d' % (i, k, q[i, k].solution_value()))

print('Done')
'''
'''
def route_distance(route):
    distance = 0
    for i in range(1, len(route)):
        distance += T[route[i-1]][route[i]]
    return distance


print(route_distance([0,1,2,6,7,5,10,3,4,8,9,0]))
'''
