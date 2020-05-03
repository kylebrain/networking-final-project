import math
def djikstra(start, end, adjacency_matrix, battery_table, battery_weight):
    """
    Parameters
        start - source node
        end - destination node
        adjacency_matrix - 1 for a connection, 0 for no connection
        battery_weight - Higher the battery_weight, the more the path avoids low battery. How many more nodes a path would take to avoid a node with 0 battery.
    """
    numNodes = len(battery_table)
    dist = [math.inf] * numNodes
    parent = [None] * numNodes
    dist[start] = 0
    Q = list(range(0, numNodes))
    while Q:
        u = Q[0]
        for element in Q:
            if dist[element] < dist[u]:
                u = element
        Q.remove(u)
        if u is end:
            break
        for neighbor in Q:
            if adjacency_matrix[u][neighbor] == 0:
                continue
            battery = battery_table[neighbor]
            if battery == -1:
                battery = 5000
            alt = dist[u] + 1 + battery_weight * (1 - battery / 10000.0)
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
