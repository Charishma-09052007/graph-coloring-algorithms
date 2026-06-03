import random
import time
import matplotlib.pyplot as plt
from math import cos, sin, pi

# ==========================================================
# 1. GRAPH GENERATORS
# ==========================================================
def generate_sparse_graph(n, p=0.25):
    nodes = list(range(n))
    edges = [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < p]
    return nodes, edges

def generate_random_graph(n, p=0.45):
    nodes = list(range(n))
    edges = [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < p]
    return nodes, edges

def generate_dense_graph(n, p=0.70):
    nodes = list(range(n))
    edges = [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < p]
    return nodes, edges


# ==========================================================
# 2. BACKTRACKING (Optimal Coloring)
# ==========================================================
class TimeoutException(Exception):
    pass

def is_valid(node, color, adj, coloring):
    return all(not (neighbor in coloring and coloring[neighbor] == color) for neighbor in adj[node])

def backtrack(nodes, adj, coloring, idx, k, start, timeout):
    if timeout and time.perf_counter() - start > timeout:
        raise TimeoutException()
    if idx == len(nodes):
        return True
    node = nodes[idx]
    for c in range(k):
        if is_valid(node, c, adj, coloring):
            coloring[node] = c
            if backtrack(nodes, adj, coloring, idx+1, k, start, timeout):
                return True
            del coloring[node]
    return False

def optimal_backtracking(nodes, edges, timeout=10.0):
    adj = {node: [] for node in nodes}
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    order = sorted(nodes, key=lambda x: len(adj[x]), reverse=True)
    start = time.perf_counter()
    try:
        for k in range(1, len(nodes)+1):
            coloring = {}
            if backtrack(order, adj, coloring, 0, k, start, timeout):
                return coloring, k, False
    except TimeoutException:
        return {}, 0, True
    return {}, 0, False


# ==========================================================
# 3. GREEDY ALGORITHM
# ==========================================================
def greedy_coloring(nodes, edges):
    adj = {node: [] for node in nodes}
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)

    coloring = {}
    for node in nodes:
        used = {coloring[n] for n in adj[node] if n in coloring}
        color = 0
        while color in used:
            color += 1
        coloring[node] = color
    return coloring, max(coloring.values()) + 1


# ==========================================================
# 4. DRAW GRAPH
# ==========================================================
def layout(n):
    return {i: (cos(2*pi*i/n), sin(2*pi*i/n)) for i in range(n)}

def draw(ax, nodes, edges, coloring, title, pos):
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'k-', alpha=0.55)
    for node in nodes:
        x, y = pos[node]
        c = "#CCCCCC" if coloring is None else plt.get_cmap("tab20")(coloring[node] % 20)
        ax.scatter(x, y, s=450, color=c, edgecolor='black')
        ax.text(x, y, str(node), ha='center', va='center', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold'); ax.axis('off')


# ==========================================================
# 5. COMPARISON FUNCTION
# ==========================================================
def compare(nodes, edges, gtype, n):
    pos = layout(n)

    print("\n🔍 Running Backtracking...")
    t1 = time.perf_counter()
    bt_col, bt_k, timeout = optimal_backtracking(nodes, edges)
    t1 = time.perf_counter() - t1

    print("🔍 Running Greedy...")
    t2 = time.perf_counter()
    gr_col, gr_k = greedy_coloring(nodes, edges)
    t2 = time.perf_counter() - t2

    fig, ax = plt.subplots(1, 3, figsize=(18, 6))
    draw(ax[0], nodes, edges, None, "Original Graph", pos)

    if timeout:
        ax[1].text(0.5, 0.5, f"TIMEOUT\n{t1:.2f}s", fontsize=14, ha='center'); ax[1].axis('off')
    else:
        draw(ax[1], nodes, edges, bt_col, f"Backtracking\nχ={bt_k}\n{t1:.4f}s", pos)

    draw(ax[2], nodes, edges, gr_col, f"Greedy\nColors={gr_k}\n{t2:.4f}s", pos)

    plt.tight_layout(); plt.show()

    return {
        "Graph": gtype, "Nodes": n, "Edges": len(edges),
        "BT_Colors": bt_k if not timeout else None,
        "BT_Time": t1, "Timeout": timeout,
        "GR_Colors": gr_k, "GR_Time": t2,
        "Winner": "Backtracking" if not timeout and bt_k < gr_k else "Greedy"
    }


# ==========================================================
# 6. MAIN LOOP
# ==========================================================
print("\n===== BACKTRACKING vs GREEDY — GRAPH COLORING EXPERIMENT =====")

results = []
sizes = [(10, "Small"), (14, "Medium"), (18, "Large")]

for n, label in sizes:
    print(f"\n--- Testing Graph size {n} ({label}) ---")
    for t, fn in [("Sparse", generate_sparse_graph),
                  ("Random", generate_random_graph),
                  ("Dense", generate_dense_graph)]:
        nodes, edges = fn(n)
        results.append(compare(nodes, edges, t, n))


print("\n===== FINAL REPORT =====")
print(f"{'Graph':<10} {'n':<4} {'Edges':<6} {'BT_χ':<6} {'GR':<6} {'Winner':<12}")
print("-"*60)
for r in results:
    bt = r['BT_Colors'] if r['BT_Colors'] is not None else "TIMEOUT"
    print(f"{r['Graph']:<10} {r['Nodes']:<4} {r['Edges']:<6} {bt:<6} {r['GR_Colors']:<6} {r['Winner']:<12}")

print("="*60)
print("✔ Experiment Complete")
