import math
def djikstra(start, end, adjacency_matrix, battery_table, alpha):
    numNodes = len(battery_table)
    dist = [math.inf] * numNodes
    parent = [None] * numNodes
    dist[start] = 0
    Q = list(range(0, numNodes))
    while Q:
        u = Q[0]
        for i,element in enumerate(Q):
            if dist[element] < dist[u]:
                u = element
        Q.remove(u)
        if u is end:
            break
        for i, neighbor in enumerate(Q):
            if adjacency_matrix[u][neighbor] == 0:
                continue
            battery = battery_table[neighbor]
            if battery == -1:
                battery = 5000
            alt = dist[u] + 1 + alpha * (1 - battery / 10000.0)
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                parent[neighbor] = u
    # Find path
    path = []
    cur = end
    if parent[end] is None and cur != start:
        return []
    while cur is not None:
        path.insert(0, cur)
        cur = parent[cur]
    return path
