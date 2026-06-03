import random
import time
import matplotlib.pyplot as plt
from math import cos, sin, pi

# ==========================================================
# GRAPH GENERATORS
# ==========================================================
def generate_sparse(n): return generate_graph(n, 0.25)
def generate_random(n): return generate_graph(n, 0.45)
def generate_dense(n):  return generate_graph(n, 0.70)

def generate_graph(n, p):
    nodes = list(range(n))
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                edges.append((u, v))
    return nodes, edges


# ==========================================================
# BACKTRACKING COLORING
# ==========================================================
def is_valid(node, color, adj, coloring):
    return all(coloring.get(nei) != color for nei in adj[node])

def backtrack(nodes, adj, coloring, idx, k, start_time, timeout):
    if timeout and (time.perf_counter() - start_time) > timeout:
        raise TimeoutError
    if idx == len(nodes): return True

    node = nodes[idx]
    for c in range(k):
        if is_valid(node, c, adj, coloring):
            coloring[node] = c
            if backtrack(nodes, adj, coloring, idx + 1, k, start_time, timeout):
                return True
            del coloring[node]
    return False

def backtracking_coloring(nodes, edges, timeout=10):
    adj = {n: [] for n in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    order = sorted(nodes, key=lambda x: len(adj[x]), reverse=True)
    start = time.perf_counter()

    try:
        for k in range(1, len(nodes) + 1):
            coloring = {}
            if backtrack(order, adj, coloring, 0, k, start, timeout):
                return coloring, k, time.perf_counter() - start
    except TimeoutError:
        return None, None, time.perf_counter() - start

    return None, None, time.perf_counter() - start


# ==========================================================
# RLF ALGORITHM
# ==========================================================
def rlf_coloring(nodes, edges):
    graph = {v: set() for v in nodes}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    uncolored = set(nodes)
    coloring = {}
    c = 0

    while uncolored:
        v = max(uncolored, key=lambda x: len(graph[x]))
        current = {v}
        coloring[v] = c
        uncolored.remove(v)

        while True:
            candidates = [x for x in uncolored if all(y not in current for y in graph[x])]
            if not candidates: break
            v = max(candidates, key=lambda x: len(graph[x] & uncolored))
            current.add(v)
            coloring[v] = c
            uncolored.remove(v)

        c += 1

    return coloring, c


# ==========================================================
# VISUALIZATION
# ==========================================================
def circle_layout(n):
    return {i: (cos(2*pi*i/n), sin(2*pi*i/n)) for i in range(n)}

def draw(ax, nodes, edges, coloring, title, pos):
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'k-', linewidth=1)
    for n in nodes:
        x, y = pos[n]
        col = (0.9,0.9,0.9) if coloring is None else plt.cm.tab20(coloring[n] % 20)
        ax.scatter(x, y, s=600, color=[col], edgecolors='black')
        ax.text(x, y, str(n), ha='center', va='center', fontsize=10)
    ax.set_title(title, fontweight='bold')
    ax.axis('off')


# ==========================================================
# COMPARISON RUNNER
# ==========================================================
def run_test(nodes, edges, graph_type, n):
    pos = circle_layout(n)

    print(f"\n Running Backtracking...")
    bt_start = time.perf_counter()
    bt_coloring, bt_colors, bt_time = backtracking_coloring(nodes, edges, timeout=10)
    print(f"   Backtracking → Colors={bt_colors}, Time={bt_time:.4f}s")

    print(f"▶ Running RLF...")
    start = time.perf_counter()
    rlf_coloring_result, rlf_colors = rlf_coloring(nodes, edges)
    rlf_time = time.perf_counter() - start
    print(f"   RLF → Colors={rlf_colors}, Time={rlf_time:.4f}s")

    # WINNER LOGIC
    if bt_colors is None:   # Timeout
        winner = "RLF"
    elif rlf_colors < bt_colors:
        winner = "RLF"
    elif bt_colors < rlf_colors:
        winner = "Backtracking"
    else:   # equal color count → execution time decides
        winner = "RLF" if rlf_time < bt_time else "Backtracking"

    # Visualization
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(f"{graph_type} Graph (n={n}, edges={len(edges)})", fontsize=16)

    draw(axs[0], nodes, edges, None, "Original", pos)
    draw(axs[1], nodes, edges, bt_coloring if bt_coloring else None,
         f"Backtracking\nχ={bt_colors} | {bt_time:.4f}s", pos)
    draw(axs[2], nodes, edges, rlf_coloring_result,
         f"RLF\nχ={rlf_colors} | {rlf_time:.4f}s", pos)

    axs[2].title.set_color("green" if winner == "RLF" else "red")
    plt.tight_layout()
    plt.show()

    return {
        "type": graph_type, "n": n, "edges": len(edges),
        "bt": bt_colors, "bt_time": bt_time,
        "rlf": rlf_colors, "rlf_time": rlf_time, "winner": winner
    }


# ==========================================================
# PRINT RESULTS TABLE
# ==========================================================
def print_results(results):
    print("\n" + "="*110)
    print("FINAL COMPARISON: BACKTRACKING vs RLF")
    print("="*110)
    print(f"{'Graph':<10} {'n':<4} {'|E|':<5} {'BT χ':<6} {'RLF χ':<6} {'Winner':<15}")
    print("-"*110)

    rlf_count = 0
    for r in results:
        print(f"{r['type']:<10} {r['n']:<4} {r['edges']:<5} {str(r['bt']):<6} {str(r['rlf']):<6} {r['winner']:<15}")
        if r['winner'] == "RLF":
            rlf_count += 1

    print("="*110)
    print(f"✔ Total Wins → RLF: {rlf_count}, Backtracking: {len(results) - rlf_count}")
    print("\n RLF is generally superior because it constructs maximal independent sets iteratively,")
    print("   while backtracking grows exponentially and times out for large n.")


# ==========================================================
# MAIN
# ==========================================================
random.seed(42)
results = []

test_sets = [
    (10, "Small"),
    (14, "Medium"),
    (18, "Large")
]

for n, label in test_sets:
    for name, gen in [
        ("Sparse", generate_sparse),
        ("Random", generate_random),
        ("Dense", generate_dense)
    ]:
        nodes, edges = gen(n)
        results.append(run_test(nodes, edges, name, n))

print_results(results)
print("\n Finished!")
