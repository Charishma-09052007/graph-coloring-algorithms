import random
import time
import matplotlib.pyplot as plt
from math import cos, sin, pi

# ==========================================================
# 1. GRAPH GENERATORS
# ==========================================================
def generate_sparse_graph(n, p=0.25): return generate_graph(n, p)
def generate_random_graph(n, p=0.45): return generate_graph(n, p)
def generate_dense_graph(n, p=0.70):  return generate_graph(n, p)

def generate_graph(n, p):
    nodes = list(range(n))
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                edges.append((u, v))
    return nodes, edges


# ==========================================================
# 2. BACKTRACKING COLORING (WITH TIMEOUT)
# ==========================================================
class TimeoutException(Exception): pass

def is_valid(node, color, adj, coloring):
    return all(coloring.get(nei) != color for nei in adj[node])

def backtrack_search(nodes, adj, coloring, idx, k, start, timeout):
    if timeout and (time.perf_counter() - start) > timeout:
        raise TimeoutException()
    if idx == len(nodes): return True

    node = nodes[idx]
    for c in range(k):
        if is_valid(node, c, adj, coloring):
            coloring[node] = c
            if backtrack_search(nodes, adj, coloring, idx + 1, k, start, timeout):
                return True
            del coloring[node]
    return False

def optimal_backtracking_coloring(nodes, edges, timeout=10):
    adj = {n: [] for n in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    order = sorted(nodes, key=lambda x: len(adj[x]), reverse=True)
    start = time.perf_counter()

    try:
        for k in range(1, len(nodes) + 1):
            coloring = {}
            if backtrack_search(order, adj, coloring, 0, k, start, timeout):
                return coloring, k, False
    except TimeoutException:
        return None, None, True

    return None, None, False


# ==========================================================
# 3. RANDOM SEQUENTIAL ALGORITHM
# ==========================================================
def random_seq_coloring(nodes, edges):
    graph = {n: set() for n in nodes}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    order = nodes.copy()
    random.shuffle(order)

    coloring = {}
    for node in order:
        used = {coloring[n] for n in graph[node] if n in coloring}
        c = 0
        while c in used:
            c += 1
        coloring[node] = c
    return coloring, max(coloring.values()) + 1


# ==========================================================
# 4. VISUALIZATION
# ==========================================================
def circular_layout(n):
    return {i: (cos(2*pi*i/n), sin(2*pi*i/n)) for i in range(n)}

def draw(ax, nodes, edges, coloring, title, pos):
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'k-', linewidth=1)
    for node in nodes:
        x, y = pos[node]
        col = (0.87, 0.87, 0.87) if coloring is None else plt.cm.tab20(coloring[node] % 20)
        ax.scatter(x, y, s=600, color=[col], edgecolors='black')
        ax.text(x, y, str(node), ha='center', va='center')
    ax.set_title(title, fontweight='bold')
    ax.axis('off')


# ==========================================================
# 5. COMPARISON LOGIC
# ==========================================================
def run_comparison(nodes, edges, graph_type, n):
    pos = circular_layout(n)

    # ---------- Backtracking ----------
    print("\n Running Backtracking...")
    start = time.perf_counter()
    bt_coloring, bt_colors, timed_out = optimal_backtracking_coloring(nodes, edges, timeout=10)
    bt_time = time.perf_counter() - start

    if timed_out:
        print(f" Backtracking TIMEOUT ({bt_time:.2f}s)")
        bt_status = False
    else:
        print(f"✓ Backtracking χ = {bt_colors} | {bt_time:.4f}s")
        bt_status = True

    # ---------- Random Seq ----------
    print(" Running Random Sequential...")
    start = time.perf_counter()
    seq_coloring, seq_colors = random_seq_coloring(nodes, edges)
    seq_time = time.perf_counter() - start
    print(f"✓ Random Seq χ = {seq_colors} | {seq_time:.4f}s")

    # ---------- Winner decision ----------
    if not bt_status:
        winner = "Random_Seq"
    elif seq_colors < bt_colors:
        winner = "Random_Seq"
    elif bt_colors < seq_colors:
        winner = "Backtracking"
    else:
        winner = "Random_Seq" if seq_time < bt_time else "Backtracking"   # equal → faster wins

    # ---------- Plot graphs ----------
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(f"{graph_type} Graph (n={n}, edges={len(edges)})", fontsize=15)

    draw(axs[0], nodes, edges, None, "Original", pos)
    draw(axs[1], nodes, edges, bt_coloring if bt_coloring else None,
         f"Backtracking\nχ={bt_colors} | {bt_time:.4f}s", pos)
    draw(axs[2], nodes, edges, seq_coloring,
         f"Random Seq\nχ={seq_colors} | {seq_time:.4f}s", pos)
    axs[2].title.set_color("green" if winner == "Random_Seq" else "red")

    plt.tight_layout()
    plt.show()

    return {
        "type": graph_type, "n": n, "edges": len(edges),
        "bt": bt_colors, "bt_time": bt_time,
        "seq": seq_colors, "seq_time": seq_time,
        "winner": winner
    }


# ==========================================================
# 6. SUMMARY TABLE
# ==========================================================
def print_results(results):
    print("\n" + "="*110)
    print("FINAL COMPARISON — BACKTRACKING vs RANDOM SEQUENTIAL")
    print("="*110)
    print(f"{'Graph':<10} {'n':<4} {'|E|':<5} {'BT χ':<6} {'SEQ χ':<7} {'Winner':<15}")
    print("-"*110)

    seq_wins = 0
    for r in results:
        print(f"{r['type']:<10} {r['n']:<4} {r['edges']:<5} {str(r['bt']):<6} {str(r['seq']):<7} {r['winner']:<15}")
        if r['winner'] == "Random_Seq":
            seq_wins += 1

    print("="*110)
    print(f" Total Wins → Random_Seq: {seq_wins}, Backtracking: {len(results) - seq_wins}")
    print("\n Reasoning:")
    print("• Backtracking is optimal but exponential → slow / timeout for large graphs.")
    print("• Random Sequential runs in O(V + E) and completes instantly.")
    print("• If both use same chromatic number, faster time wins → Random_Seq often wins.")


# ==========================================================
# 7. MAIN
# ==========================================================
random.seed(42)
results = []

test_cfgs = [
    (10, "Small"),
    (14, "Medium"),
    (18, "Large")
]

for n, label in test_cfgs:
    for graph_name, gen in [
        ("Sparse", generate_sparse_graph),
        ("Random", generate_random_graph),
        ("Dense", generate_dense_graph)
    ]:
        nodes, edges = gen(n)
        results.append(run_comparison(nodes, edges, graph_name, n))

print_results(results)
print("\n COMPLETE!")
