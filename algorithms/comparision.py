import time
import matplotlib.pyplot as plt
import colorsys
import math

from greedy import greedy_coloring
from random_seq import random_sequential_coloring
from rlf import rlf_coloring
from backtracking import backtracking_coloring

# color generator
def get_color_for_index(index):
    hue = (index * 0.17) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
    return (r, g, b)

# draw final graph
def draw_graph(nodes, edges, coloring, title):
    plt.figure(figsize=(6, 6))
    pos = {}
    n = len(nodes)

    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / n
        pos[node] = (math.cos(angle), math.sin(angle))

    for u, v in edges:
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        plt.plot(x, y, color="black")

    for node in nodes:
        x, y = pos[node]
        color = get_color_for_index(coloring[node]) if coloring else (1, 1, 1)
        plt.scatter(x, y, s=700, color=[color], edgecolors="black")
        plt.text(x, y, str(node), ha="center", va="center", fontsize=12)

    plt.title(title)
    plt.axis("off")
    plt.show()

# load graph from file
def load_graph(filename):
    with open(filename) as f:
        n, m = map(int, f.readline().split())
        edges = [tuple(map(int, f.readline().split())) for _ in range(m)]
    return list(range(n)), edges


if __name__ == "__main__":
    filename = input("Enter graph file name: ")  # sparse.txt, random.txt, dense.txt
    nodes, edges = load_graph(filename)

    print("\nAvailable Algorithms:")
    print("1 - Greedy")
    print("2 - Random Sequential")
    print("3 - RLF")
    print("4 - Backtracking")

    alg1 = int(input("Enter first algorithm number: "))
    alg2 = int(input("Enter second algorithm number: "))

    mapping = {
        1: ("Greedy", greedy_coloring),
        2: ("Random Sequential", random_sequential_coloring),
        3: ("RLF", rlf_coloring),
        4: ("Backtracking", backtracking_coloring),
    }

    name1, func1 = mapping[alg1]
    name2, func2 = mapping[alg2]

    # show before coloring
    draw_graph(nodes, edges, None, "Original Graph (No Coloring)")

    results = []
    for name, func in [(name1, func1), (name2, func2)]:
        start = time.time()
        coloring = func(nodes.copy(), edges.copy())
        end = time.time()

        draw_graph(nodes, edges, coloring, f"{name} Final Coloring")

        total_colors = max(coloring.values()) + 1
        exec_time = round(end - start, 6)
        results.append((name, total_colors, exec_time))

    print("\n================== COMPARISON REPORT ==================\n")
    print(f"{'Algorithm':22s} {'Colors Used':15s} {'Execution Time (sec)':20s}")
    print("-" * 65)
    for name, colors, t in results:
        print(f"{name:22s} {str(colors):15s} {str(t):20s}")

    # choose winner: lowest colors → if tie, fastest
    min_colors = min(r[1] for r in results)
    best_candidates = [r for r in results if r[1] == min_colors]
    best = min(best_candidates, key=lambda x: x[2])

    print("\n========================================================")
    print(f"Best algorithm (min colors → then min time) = {best[0]}")
    print("========================================================\n")
