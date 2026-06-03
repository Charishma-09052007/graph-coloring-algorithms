import random
import time
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi

# ==========================================================
# 1. GRAPH GENERATORS
# ==========================================================
def generate_sparse_graph(n, edge_probability=0.25):
    nodes = list(range(n))
    edges = [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < edge_probability]
    return nodes, edges

def generate_dense_graph(n, edge_probability=0.70):
    nodes = list(range(n))
    edges = [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < edge_probability]
    return nodes, edges

def generate_random_graph(n, edge_probability=0.45):
    nodes = list(range(n))
    edges = [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < edge_probability]
    return nodes, edges


# ==========================================================
# 2. RLF COLORING
# ==========================================================
def rlf_coloring(nodes, edges):
    graph = {node: set() for node in nodes}
    for u, v in edges: graph[u].add(v); graph[v].add(u)

    coloring = {}
    uncolored = set(nodes)
    color = 0

    while uncolored:
        start = max(uncolored, key=lambda x: len(graph[x]))
        current_set = {start}
        coloring[start] = color
        uncolored.remove(start)

        updated = True
        while updated:
            updated = False
            for node in list(uncolored):
                if all(nei not in current_set for nei in graph[node]):
                    coloring[node] = color
                    current_set.add(node)
                    uncolored.remove(node)
                    updated = True

        color += 1

    return coloring


# ==========================================================
# 3. RANDOM SEQUENTIAL COLORING
# ==========================================================
def random_sequential_coloring(nodes, edges):
    graph = {node: set() for node in nodes}
    for u, v in edges: graph[u].add(v); graph[v].add(u)

    order = nodes.copy()
    random.shuffle(order)

    coloring = {}
    for node in order:
        neighbor_colors = {coloring[n] for n in graph[node] if n in coloring}
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[node] = color

    return coloring


# ==========================================================
# 4. VISUALIZATION
# ==========================================================
def circular_layout(n):
    return {i: (cos(2*pi*i/n), sin(2*pi*i/n)) for i in range(n)}

def draw(ax, nodes, edges, coloring, title, pos):
    palette = [
        '#FF6B6B','#4ECDC4','#45B7D1','#FFA07A','#98D8C8',
        '#F7DC6F','#BB8FCE','#85C1E2','#F8B739','#52B788'
    ]
    for u,v in edges:
        ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],'k-',alpha=0.6,zorder=1)
    for node in nodes:
        x,y = pos[node]
        color = palette[coloring[node] % len(palette)] if coloring else "#CCCCCC"
        ax.add_patch(plt.Circle((x,y),0.15,color=color,ec="black",lw=2.5,zorder=2))
        ax.text(x,y,str(node),ha='center',va='center',fontsize=12,zorder=3)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title,fontsize=13,fontweight='bold')


# ==========================================================
# 5. RUN COMPARISON
# ==========================================================
def run_comparison(nodes, edges, graph_type, n):
    pos = circular_layout(n)

    start = time.perf_counter()
    rlf = rlf_coloring(nodes, edges)
    rlf_time = time.perf_counter() - start
    rlf_colors = max(rlf.values()) + 1

    start = time.perf_counter()
    rs = random_sequential_coloring(nodes, edges)
    rs_time = time.perf_counter() - start
    rs_colors = max(rs.values()) + 1

    fig, ax = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle(f'{graph_type} Graph — n={n}, |E|={len(edges)}', fontsize=16, fontweight='bold', y=0.98)

    draw(ax[0], nodes, edges, None, 'Original', pos)
    draw(ax[1], nodes, edges, rlf, f'RLF — {rlf_colors} colors\n{rlf_time:.6f}s', pos)

    color_status = "OPTIMAL" if rs_colors == rlf_colors else "Suboptimal"
    title = f'RandomSeq — {rs_colors} colors\n{rs_time:.6f}s\n({color_status})'
    draw(ax[2], nodes, edges, rs, title, pos)
    ax[2].title.set_color("green" if rs_colors == rlf_colors else "red")

    plt.tight_layout()
    plt.show()

    return {
        "type": graph_type, "n": n, "edges": len(edges),
        "rlf_colors": rlf_colors, "rlf_time": rlf_time,
        "rs_colors": rs_colors, "rs_time": rs_time
    }


# ==========================================================
# 6. RESULTS TABLE
# ==========================================================
def print_results(results):
    print("\n" + "="*115)
    print("RLF vs RANDOM SEQUENTIAL — PERFORMANCE SUMMARY")
    print("="*115)
    print(f"{'Graph':<12} {'n':<4} {'|E|':<6} {'RLF Colors':<11} {'RLF Time':<12} "
          f"{'RS Colors':<10} {'RS Time':<12} {'Speedup':<12} {'Winner':<12}")
    print("-"*115)

    for r in results:
        if r["rs_colors"] == r["rlf_colors"]:
            winner = "DRAW (same χ)"
        elif r["rs_colors"] < r["rlf_colors"]:
            winner = "RandomSeq"
        else:
            winner = "RLF"

        speed = r["rlf_time"] / r["rs_time"]
        speed_str = f"RS {speed:.2f}x faster" if speed > 1 else f"RLF {(1/speed):.2f}x faster"

        print(f"{r['type']:<12} {r['n']:<4} {r['edges']:<6} {r['rlf_colors']:<11} "
              f"{r['rlf_time']:<12.6f} {r['rs_colors']:<10} {r['rs_time']:<12.6f} "
              f"{speed_str:<12} {winner:<12}")

    print("="*115)
    print("\n📌 INSIGHTS:")
    print("• RLF aggressively reduces coloring, usually using fewer colors.")
    print("• Random Sequential is much faster but may use more colors.")
    print("• For dense graphs, the gap between RLF and RS typically increases.")
    print("• For large n, RLF scales poorly because of repeated set operations.")


# ==========================================================
# 7. MAIN
# ==========================================================
random.seed(42)
print("="*120)
print("GRAPH COLORING COMPARISON — RLF vs RANDOM SEQUENTIAL")
print("="*120)

results = []
test_cases = [
    (10, "Small"),
    (14, "Medium"),
    (18, "Large"),
    (20, "Large+"),
    (22, "Large++"),
]

for n, label in test_cases:
    print(f"\n{'='*120}\nTesting n={n} ({label})\n{'='*120}")
    for graph_type, gen in [("Sparse", generate_sparse_graph),
                            ("Random", generate_random_graph),
                            ("Dense", generate_dense_graph)]:
        nodes, edges = gen(n)
        print(f"[{graph_type}] {len(edges)} edges")
        results.append(run_comparison(nodes, edges, graph_type, n))

print_results(results)

print("\n✅ COMPLETE")
