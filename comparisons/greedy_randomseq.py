import random
import time
import matplotlib.pyplot as plt
from math import cos, sin, pi

# ==========================================================
# GRAPH GENERATORS
# ==========================================================
def generate_sparse_graph(n): return generate_graph(n, 0.25)
def generate_random_graph(n): return generate_graph(n, 0.45)
def generate_dense_graph(n): return generate_graph(n, 0.70)

def generate_graph(n, p):
    nodes = list(range(n))
    edges = [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < p]
    return nodes, edges


# ==========================================================
# GREEDY COLORING
# ==========================================================
def greedy_coloring(nodes, edges):
    graph = {v: [] for v in nodes}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    coloring = {}
    for node in nodes:  # sequential greedy
        used = {coloring[n] for n in graph[node] if n in coloring}
        c = 0
        while c in used:
            c += 1
        coloring[node] = c

    return coloring, max(coloring.values()) + 1


# ==========================================================
# RANDOM SEQUENTIAL COLORING
# ==========================================================
def random_sequential_coloring(nodes, edges):
    graph = {v: [] for v in nodes}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

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
# VISUALIZATION
# ==========================================================
def circle_layout(n):
    return {i: (cos(2*pi*i/n), sin(2*pi*i/n)) for i in range(n)}

def draw(ax, nodes, edges, coloring, title, pos):
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'k-', linewidth=1)
    for node in nodes:
        x, y = pos[node]
        col = (0.88,0.88,0.88) if coloring is None else plt.cm.tab20(coloring[node] % 20)
        ax.scatter(x, y, s=600, color=[col], edgecolors='black')
        ax.text(x, y, str(node), va='center', ha='center', fontsize=10)
    ax.set_title(title, fontweight='bold')
    ax.axis('off')


# ==========================================================
# COMPARISON RUNNER
# ==========================================================
def run_comparison(nodes, edges, graph_type, n):
    pos = circle_layout(n)

    print(f"\n▶ Running Greedy...")
    start = time.perf_counter()
    greedy_coloring_result, greedy_colors = greedy_coloring(nodes, edges)
    greedy_time = time.perf_counter() - start
    print(f"   Greedy → χ={greedy_colors}, time={greedy_time:.4f}s")

    print(f"▶ Running Random Sequential...")
    start = time.perf_counter()
    seq_coloring_result, seq_colors = random_sequential_coloring(nodes, edges)
    seq_time = time.perf_counter() - start
    print(f"   Random Seq → χ={seq_colors}, time={seq_time:.4f}s")

    # Winner decision
    if seq_colors < greedy_colors:
        winner = "Random_Seq"
    elif greedy_colors < seq_colors:
        winner = "Greedy"
    else:
        winner = "Random_Seq" if seq_time < greedy_time else "Greedy"

    # visualization
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(f"{graph_type} Graph (n={n}, edges={len(edges)})", fontsize=16)

    draw(axs[0], nodes, edges, None, "Original", pos)
    draw(axs[1], nodes, edges, greedy_coloring_result, f"Greedy\nχ={greedy_colors} | {greedy_time:.4f}s", pos)
    draw(axs[2], nodes, edges, seq_coloring_result, f"Random Seq\nχ={seq_colors} | {seq_time:.4f}s", pos)

    axs[1].title.set_color("green" if winner == "Greedy" else "red")
    axs[2].title.set_color("green" if winner == "Random_Seq" else "red")

    plt.tight_layout()
    plt.show()

    return {
        "type": graph_type, "n": n, "edges": len(edges),
        "greedy": greedy_colors, "seq": seq_colors, "winner": winner
    }


# ==========================================================
# RESULTS TABLE
# ==========================================================
def print_results(results):
    print("\n" + "="*110)
    print("FINAL COMPARISON: GREEDY vs RANDOM SEQUENTIAL")
    print("="*110)
    print(f"{'Graph':<10} {'n':<4} {'|E|':<5} {'Greedy χ':<10} {'Seq χ':<10} {'Winner':<15}")
    print("-"*110)

    seq_wins = 0
    for r in results:
        print(f"{r['type']:<10} {r['n']:<4} {r['edges']:<5} {str(r['greedy']):<10} {str(r['seq']):<10} {r['winner']:<15}")
        if r['winner'] == "Random_Seq":
            seq_wins += 1

    print("="*110)
    print(f"🏆 Total Wins → Greedy: {len(results) - seq_wins}, Random_Seq: {seq_wins}")
    print("\n📌 Notes:")
    print("• Greedy is deterministic → usually fewer colors when good ordering occurs.")
    print("• Random Sequential depends on random order → sometimes worse, sometimes better.")
    print("• If colors equal, faster execution time determines winner → no ties.")


# ==========================================================
# MAIN EXECUTION
# ==========================================================
random.seed(42)
results = []

test_configs = [(10, "Small"), (14, "Medium"), (18, "Large")]

for n, label in test_configs:
    for graph_type, generator in [
        ("Sparse", generate_sparse_graph),
        ("Random", generate_random_graph),
        ("Dense", generate_dense_graph)
    ]:
        nodes, edges = generator(n)
        results.append(run_comparison(nodes, edges, graph_type, n))

print_results(results)
print("\n COMPLETE!")
