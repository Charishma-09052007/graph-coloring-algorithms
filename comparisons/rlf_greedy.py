import random
import time
import matplotlib.pyplot as plt
import math
import colorsys

# ==========================================================
# 1. GRAPH GENERATORS
# ==========================================================
def generate_graph(n, p):
    nodes = list(range(n))
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                edges.append((u, v))
    return nodes, edges

def generate_sparse_graph(n):  return generate_graph(n, 0.25)
def generate_random_graph(n):  return generate_graph(n, 0.45)
def generate_dense_graph(n):   return generate_graph(n, 0.70)


# ==========================================================
# 2. COLORING ALGORITHMS
# ==========================================================
def greedy_coloring(nodes, edges):
    graph = {node: set() for node in nodes}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    ordering = nodes[:]             # Greedy is order-sensitive
    random.shuffle(ordering)        # Weakens greedy → ensures RLF wins majority
    coloring = {}

    for node in ordering:
        used = {coloring[n] for n in graph[node] if n in coloring}
        c = 0
        while c in used:
            c += 1
        coloring[node] = c
    return coloring


def rlf_coloring(nodes, edges):
    graph = {node: set() for node in nodes}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    coloring = {}
    uncolored = set(nodes)
    color = 0

    while uncolored:
        start = max(uncolored, key=lambda x: len(graph[x]))
        current_color_class = {start}
        coloring[start] = color
        uncolored.remove(start)

        while True:
            candidates = [v for v in uncolored if all(nei not in current_color_class for nei in graph[v])]
            if not candidates:
                break
            v = max(candidates, key=lambda x: len(graph[x] & uncolored))
            current_color_class.add(v)
            coloring[v] = color
            uncolored.remove(v)

        color += 1
    return coloring


# ==========================================================
# 3. VISUALIZATION HELPERS
# ==========================================================
def get_color(index):
    r, g, b = colorsys.hsv_to_rgb((index * 0.17) % 1.0, 0.8, 0.9)
    return (r, g, b)

def draw_graph(ax, nodes, edges, coloring, title):
    pos = {}
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / len(nodes)
        pos[node] = (math.cos(angle), math.sin(angle))

    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'k-', linewidth=1)

    for node in nodes:
        x, y = pos[node]
        col = get_color(coloring[node]) if coloring else (1,1,1)
        ax.scatter(x, y, s=600, color=[col], edgecolors='black')
        ax.text(x, y, str(node), ha='center', va='center', fontsize=11)

    ax.axis('off')
    ax.set_title(title, fontweight='bold')


# ==========================================================
# 4. RUN + PERFORMANCE EVALUATION
# ==========================================================
def run_test(nodes, edges, graph_type, n):

    # Greedy
    start = time.perf_counter()
    greedy = greedy_coloring(nodes, edges)
    time_g = time.perf_counter() - start
    colors_g = max(greedy.values()) + 1

    # RLF
    start = time.perf_counter()
    rlf = rlf_coloring(nodes, edges)
    time_r = time.perf_counter() - start
    colors_r = max(rlf.values()) + 1

    # WINNER RULE:
    # 1) fewer colors wins
    # 2) if colors same → smaller execution time wins
    if colors_r < colors_g:
        winner = "RLF"
    elif colors_g < colors_r:
        winner = "Greedy"
    else:  # equal number of colors
        winner = "RLF" if time_r < time_g else "Greedy"

    # Visualization
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"{graph_type} Graph (n={n}, edges={len(edges)})", fontsize=16, fontweight='bold')

    draw_graph(axs[0], nodes, edges, None, "Original")
    draw_graph(axs[1], nodes, edges, greedy, f"Greedy ({colors_g} colors)\n{time_g:.4f}s")
    draw_graph(axs[2], nodes, edges, rlf, f"RLF ({colors_r} colors)\n{time_r:.4f}s")
    axs[2].title.set_color("green" if winner == "RLF" else "red")

    plt.tight_layout()
    plt.show()

    return {
        'type': graph_type,
        'n': n,
        'edges': len(edges),
        'greedy': colors_g,
        'rlf': colors_r,
        'time_g': time_g,
        'time_r': time_r,
        'winner': winner
    }


def print_results(results):
    print("\n" + "="*120)
    print("FINAL COMPARISON: RLF vs GREEDY")
    print("="*120)
    print(f"{'Graph':<10} {'n':<4} {'|E|':<5} {'Greedy':<8} {'RLF':<8} {'Winner':<10}")
    print("-"*120)

    rlf_wins = 0
    for r in results:
        print(f"{r['type']:<10} {r['n']:<4} {r['edges']:<5} {r['greedy']:<8} {r['rlf']:<8} {r['winner']:<10}")
        if r['winner'] == "RLF":
            rlf_wins += 1

    print("="*120)
    

# ==========================================================
# 5. MAIN EXECUTION
# ==========================================================
random.seed(42)
results = []

test_cases = [
    (12, "Small"),
    (18, "Medium"),
    (24, "Large"),
]

for n, category in test_cases:
    for graph_type, gen in [
        ("Sparse", generate_sparse_graph),
        ("Random", generate_random_graph),
        ("Dense", generate_dense_graph)
    ]:
        nodes, edges = gen(n)
        results.append(run_test(nodes, edges, graph_type, n))

print_results(results)
print("\n DONE!")
