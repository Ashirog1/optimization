import copy
import sys
 
def route_distance(route:list):
    distance = 0
    if len(route) == 1:
        return 0
    for i in range(1, len(route)):
        distance += T[route[i-1]][route[i]]
    distance += T[route[len(route)-1]][0]
    return distance
 
 
def routes_distance(routes):
    distance = 0
    for route in routes:
        distance += route_distance(route)
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
    route=copy.deepcopy(best)
    return route
 
# Return all neighbour feasible solution
def get_neighbour(routes):
    neighbour = []
    copy_routes = copy.deepcopy(routes)
    # outra route
    # for route_id,route in enumerate(routes):
    #     for i in range(1,len(route)):
    #         if route[i]<=n:
    #             # Move i and i+n to other route
    #             routes=copy.deepcopy(copy_routes)
    #             copy_route = copy.deepcopy(route)
    #             cus=route[i]
    #             route.remove(cus)
    #             route.remove(cus+n)
    #             for j in range(route_id+1, len(routes)):
    #                 copy_routes2 = copy.deepcopy(routes)
    #                 routes[j]=insertion(routes[j],j,cus)
    #                 yield routes
    #                 # cover back before insert to j
    #                 routes=copy.deepcopy(copy_routes2)
    #             route = copy_route
    # intra route
    for i in range(1, len(routes[0])):
        for j in range(i+1, len(routes[0])):
            cusi=routes[0][i]
            cusj=routes[0][j]
            routes[0][i], routes[0][j] = cusj, cusi
            if (is_feasible(routes, 0) and routes_distance(routes) < routes_distance(copy_routes)):
                yield routes
            routes = copy.deepcopy(copy_routes)
            
    return neighbour

m = 1
n, cap = map(int, sys.stdin.readline().strip().split())
#Q =  list(map(int, f.readline().strip().split()))
Q = list()
Q.append(cap)
T = []
for i in range(2*n+1):
    T.append(list(map(int, sys.stdin.readline().strip().split())))



# Each vehicle route start from 0
routes = []
for i in range(m):
    routes.append([0])

visited = [False] * (2*n+1)
visited[0] = True

ans = 0
# Greedy

# Init solution
# Vehicle 1 have path: 1, 1+n, 2, 2+n, ..., n,n+n
for i in range(1,n+1):
    routes[0]=insertion(routes[0],0,i)

# Local search, go to best solution in each step
ans = routes_distance(routes)
while True:
    improvable=False
    for nxt in get_neighbour(routes):
        if routes_distance(nxt)<ans:
            routes=nxt
            ans=route_distance(nxt)
            improvable=True
    if not improvable:
        break
    # print(routes)

print(routes_distance(routes))
