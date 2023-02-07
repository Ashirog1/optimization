import numpy as np

def distance(x1, y1, x2, y2):
    # Euclidean distance between two points
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def ClarkeWright(n, x, y, demand):
    savings = []
    for i in range(n):
        for j in range(i + 1, n):
            savings.append((i, j, distance(x[i], y[i], x[0], y[0]) + distance(x[j], y[j], x[0], y[0]) - distance(x[i], y[i], x[j], y[j])))
    savings.sort(key=lambda x: x[2], reverse=True)

    route = [0] * (n + 1)
    route[0], route[1] = 0, 1
    for i, j, s in savings:
        if demand[i] + demand[j] <= 0:
            route[1] = j
            for k in range(2, n + 1):
                if route[k] == i:
                    route[k] = j
                    break
            demand[j] += demand[i]

    return route

if __name__ == "__main__":
    n = 5
    x = [0, 10, 20, 30, 40]
    y = [0, 10, 20, 30, 40]
    demand = [0, -1, 1, -1, 1]
    route = ClarkeWright(n, x, y, demand)
    print("Route:", route)