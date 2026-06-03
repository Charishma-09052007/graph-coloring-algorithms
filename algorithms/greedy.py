import matplotlib.pyplot as plt
import colorsys
import math

# Unlimited color generator
def get_color_for_index(index):
    hue = (index * 0.17) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
    return (r, g, b)

# Draw graph
def draw_graph(nodes, edges, coloring=None, title="Graph"):
    plt.figure(figsize=(6,6))
    pos = {}
    n = len(nodes)

    # Position nodes in a circle
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / n
        pos[node] = (math.cos(angle), math.sin(angle))

    # Draw edges
    for u, v in edges:
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        plt.plot(x, y, color='black')

    # Draw nodes
    for node in nodes:
        x, y = pos[node]
        if coloring is not None:
            color = get_color_for_index(coloring[node])
        else:
            color = (1, 1, 1)  # white
        plt.scatter(x, y, s=700, color=[color], edgecolors='black', zorder=2)
        plt.text(x, y, str(node), ha='center', va='center', fontsize=12)

    plt.title(title)
    plt.axis('off')
    plt.show()


# =========================
# GREEDY COLORING ALGORITHM
# =========================
def greedy_coloring(nodes, edges):

    # Build adjacency list
    graph = {node: [] for node in nodes}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    coloring = {}

    # Greedy algorithm (same as your original)
    for node in nodes:
        used_colors = set(coloring[n] for n in graph[node] if n in coloring)
        color = 0
        while color in used_colors:
            color += 1
        coloring[node] = color

    return coloring


# MAIN PART
def load_graph(filename):
    with open(filename) as f:
        n, m = map(int, f.readline().split())
        edges = []
        for _ in range(m):
            u, v = map(int, f.readline().split())
            edges.append((u, v))
    return list(range(n)), edges


if __name__ == "__main__":
    filename = input("Enter graph file: ")

    nodes, edges = load_graph(filename)

    # Show WITHOUT coloring
    draw_graph(nodes, edges, None, "Graph Before Greedy Coloring")

    # Run GREEDY coloring
    coloring = greedy_coloring(nodes, edges)

    # Show WITH coloring
    draw_graph(nodes, edges, coloring, "Graph After Greedy Coloring")

    print("\nFinal Coloring:")
    for node in sorted(coloring):
        print(f"Node {node}: Color {coloring[node]}")

    print(f"\nTotal Colors Used: {max(coloring.values()) + 1}")