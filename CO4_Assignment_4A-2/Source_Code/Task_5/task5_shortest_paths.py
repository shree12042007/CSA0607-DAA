"""
Task 5: Shortest Path Algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall)
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
"""

import math

def dijkstra(vertices, edges, source):
    dist = {v: math.inf for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0
    visited = set()

    while len(visited) < len(vertices):
        u = None
        min_d = math.inf
        for v in vertices:
            if v not in visited and dist[v] < min_d:
                min_d = dist[v]
                u = v
        if u is None:
            break
        visited.add(u)

        for src, dst, w in edges:
            if src == u and dst not in visited:
                if dist[u] + w < dist[dst]:
                    dist[dst] = dist[u] + w
                    pred[dst] = u
    return dist, pred

def bellman_ford(vertices, edges, source):
    dist = {v: math.inf for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0

    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                updated = True
        if not updated:
            break

    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, pred, has_negative_cycle

def floyd_warshall(vertices, edges):
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    D = [[math.inf] * n for _ in range(n)]

    for i in range(n):
        D[i][i] = 0
    for u, v, w in edges:
        D[idx[u]][idx[v]] = min(D[idx[u]][idx[v]], w)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] != math.inf and D[k][j] != math.inf:
                    if D[i][k] + D[k][j] < D[i][j]:
                        D[i][j] = D[i][k] + D[k][j]
    return D

if __name__ == "__main__":
    print("=== TASK 5: GRAPH SHORTEST PATHS ===")
    V = ["A", "B", "C", "D", "E"]
    E = [
        ("A", "B", 4),
        ("A", "C", 7),
        ("B", "C", 2),
        ("B", "D", 6),
        ("C", "D", 1),
        ("D", "E", 3),
        ("C", "E", 8),
    ]

    d_dist, d_pred = dijkstra(V, E, "A")
    print("\n[5.1 Dijkstra from Source A]")
    for v in V:
        print(f"  Vertex {v}: Distance = {d_dist[v]}, Predecessor = {d_pred[v]}")

    E_neg = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("C", "B", -3),
        ("B", "D", 6),
        ("C", "D", 1),
        ("D", "E", 3),
        ("C", "E", 8),
    ]
    bf_dist, bf_pred, neg_cyc = bellman_ford(V, E_neg, "A")
    print("\n[5.2 Bellman-Ford with Negative Edge (C->B = -3)]")
    print(f"  Negative Cycle Detected: {neg_cyc}")
    for v in V:
        print(f"  Vertex {v}: Distance = {bf_dist[v]}, Predecessor = {bf_pred[v]}")

    fw_matrix = floyd_warshall(V, E)
    print("\n[5.3 Floyd-Warshall All-Pairs Shortest Path Matrix]")
    print("     " + " ".join(f"{v:>4s}" for v in V))
    for i, u in enumerate(V):
        row_str = " ".join(f"{fw_matrix[i][j]:4.0f}" if fw_matrix[i][j] != math.inf else " inf" for j in range(len(V)))
        print(f"  {u}: {row_str}")
