import matplotlib.pyplot as plt
import colorsys
import math

# Unlimited color generator
def get_color_for_index(index):
    hue = (index * 0.17) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
    return (r, g, b)

# Draw graph (NO step-by-step)
def draw_graph(nodes, edges, coloring=None, title="Graph"):
    plt.figure(figsize=(6, 6))
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
        plt.plot(x, y, color="black")

    # Draw nodes
    for node in nodes:
        x, y = pos[node]

        if coloring and node in coloring:
            color = get_color_for_index(coloring[node])
        else:
            color = (1, 1, 1)  # white

        plt.scatter(x, y, s=700, color=[color], edgecolors="black")
        plt.text(x, y, str(node), ha="center", va="center", fontsize=12)

    plt.title(title)
    plt.axis("off")
    plt.show()

# ------------------------------
# OPTIMAL BACKTRACKING (Chromatic Number)
# ------------------------------

def is_valid(node, color, adj, coloring):
    for neighbor in adj[node]:
        if neighbor in coloring and coloring[neighbor] == color:
            return False
    return True


def backtrack_with_k_colors(nodes, adj, coloring, node_index, k):
    if node_index == len(nodes):
        return True

    node = nodes[node_index]

    for color in range(k):
        if is_valid(node, color, adj, coloring):
            coloring[node] = color

            if backtrack_with_k_colors(nodes, adj, coloring, node_index + 1, k):
                return True

            del coloring[node]  # backtrack

    return False


def backtracking_coloring(nodes, edges):
    # Build adjacency list
    adj = {node: [] for node in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Node ordering optimization → decreasing degree (fewer branches)
    nodes_sorted = sorted(nodes, key=lambda x: len(adj[x]), reverse=True)

    # Try colours from 1 to n and stop when success
    for k in range(1, len(nodes) + 1):
        coloring = {}
        if backtrack_with_k_colors(nodes_sorted, adj, coloring, 0, k):
            # Remap sorted-order result back to original node ordering
            final_coloring = {}
            for node in nodes:
                final_coloring[node] = coloring[node]  # ensures drawing compatibility
            return final_coloring

    return {}  # should never reach here


# Load graph from file
def load_graph(filename):
    with open(filename) as f:
        n, m = map(int, f.readline().split())
        edges = []
        for _ in range(m):
            u, v = map(int, f.readline().split())
            edges.append((u, v))
    return list(range(n)), edges

# MAIN
if __name__ == "__main__":
    filename = input("Enter graph file (sparse.txt/random.txt/dense.txt): ")

    nodes, edges = load_graph(filename)

    # BEFORE coloring
    draw_graph(nodes, edges, None, "Graph Before Coloring")

    # Run Backtracking
    coloring = backtracking_coloring(nodes, edges)

    # AFTER coloring
    draw_graph(nodes, edges, coloring, "Graph After Backtracking Coloring")

    print("\nFinal Coloring:")
    for node in sorted(coloring):
        print(f"Node {node}: Color {coloring[node]}")

    # TOTAL COLORS USED
    total_colors = max(coloring.values()) + 1
    print(f"\nTotal Minimum Colors Used: {total_colors}")
    