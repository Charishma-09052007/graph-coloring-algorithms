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
        if coloring:
            color = get_color_for_index(coloring[node])
        else:
            color = (1, 1, 1)  # white
        plt.scatter(x, y, s=700, color=[color], edgecolors='black', zorder=2)
        plt.text(x, y, str(node), ha='center', va='center', fontsize=12)

    plt.title(title)
    plt.axis('off')
    plt.show()

# =========================
# RLF COLORING ALGORITHM
# =========================
def rlf_coloring(nodes, edges):
    # Build adjacency list
    graph = {node: set() for node in nodes}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    coloring = {}
    uncolored = set(nodes)
    color_index = 0

    while uncolored:
        # Pick the vertex with highest degree among uncolored
        start = max(uncolored, key=lambda x: len(graph[x]))
        current_color_set = {start}
        coloring[start] = color_index
        uncolored.remove(start)

        added = True
        while added:
            added = False
            # Add next vertex with no conflict with current_color_set
            candidate = None
            for node in list(uncolored):
                if all(nei not in current_color_set for nei in graph[node]):
                    candidate = node
                    break

            if candidate is not None:
                coloring[candidate] = color_index
                current_color_set.add(candidate)
                uncolored.remove(candidate)
                added = True

        color_index += 1

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
    draw_graph(nodes, edges, None, "Graph Before Coloring")

    # RLF coloring
    coloring = rlf_coloring(nodes, edges)

    # Show WITH coloring
    draw_graph(nodes, edges, coloring, "Graph After RLF Coloring")

    print("\nFinal Coloring:")
    for node in sorted(coloring):
        print(f"Node {node}: Color {coloring[node]}")

    print(f"\nTotal Colors Used: {max(coloring.values()) + 1}")
