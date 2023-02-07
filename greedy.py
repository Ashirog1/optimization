import copy
import sys
import os

m = 1
n, cap = map(int, sys.stdin.readline().strip().split())
#Q =  list(map(int, f.readline().strip().split()))
Q = list()
Q.append(cap)
T = []
for i in range(2*n+1):
    T.append(list(map(int, sys.stdin.readline().strip().split())))
  
 
def route_distance(route):
    distance = 0
    for i in range(1, len(route)):
        distance += T[route[i-1]][route[i]]
    distance += T[route[len(route)-1]][0]
    return distance
 
 
 
# Check if routes is feasible solution?
def is_feasible(route,route_id):
    if len(route) == 1:
        return True
 
    app = [0]*(2*n+1)
    # Check condition i appear before i+N
    for i in route[1:]:
        if i > n:
            if app[i - n] == 0:
                return False
        else:
            app[i] = 1
    
    for cus in range(len(route)-1, 0, -1):
        i = route[cus]
        if i < n:
            if app[i + n] == 0:
                return False
        else:
            app[i] = 1
    # Check Q_k
    cur = 0
    for i in route[1:]:
        if i <= n:
            cur += 1
        else:
            cur -= 1
        if cur > Q[route_id]:
            return False
    return True
 
 
def local_search(route, route_id):
    best = route
    while True:
        improveable = False
        for i in range(1, len(route)-1):
            for j in range(i+2, len(route)+1):
                new_route=route[:]
                new_route[i:j]=route[j-1:i-1:-1]
                # print(new_route, route_distance(new_route), is_feasible(new_route, route_id))
                if is_feasible(new_route, route_id)and route_distance(new_route)<route_distance(best):
                    best=new_route
                    improveable = True
 
        if not improveable:
            break
        route = best
    # print("route", route)
 
# Insert loc and loc+n to best location
def insertion(route, route_id, loc):
    best = route[:]
    best_obj = 10**19
    for i in range(len(route)+1, 0, -1):
        for j in range(i+1, len(route)+2):
            route.insert(i,loc)
            route.insert(j,loc+n)
            if is_feasible(route,route_id) and best_obj>route_distance(route):
                best_obj = route_distance(route)
                best=copy.deepcopy(route)
            del route[j]
            del route[i]
            
    return best_obj,best
 
# Return all neighbour feasible solution
def get_neighbour(routes):
    neighbour = []
    for route_id,route in enumerate(routes):
        pass
    
    pass
            
 
# Each vehicle route start from 0
routes = []
for i in range(m):
    routes.append([0])
 
visited = [False] * (2*n+1)
visited[0] = True
 
ans = 0
# Greedy
while not all(visited):
    best_gain = 10**18
    best_next = copy.deepcopy(routes)
    tmp = copy.deepcopy(routes)
    for route in routes:
        for cus in route:
            visited[cus] = True
    for i in range(1,n+1):
        if not visited[i]:
            for id,route in enumerate(routes):
                gain,path=insertion(route,id,i)
                if best_gain>gain:
                    routes[id]=path
                    best_next=routes
                    best_gain=gain
                routes = copy.deepcopy(tmp)
    ans += best_gain
    routes = best_next
    # print(routes)
 
# Init solution
# Vehicle 1 have path: 1, 1+n, 2, 2+n, ..., n,n+n
 
ans=0
for route in routes:
    ans += route_distance(route)
print(ans)
# print(routes)