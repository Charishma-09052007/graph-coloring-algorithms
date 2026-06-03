import random

def generate_graph_file(filename, n, density):
    edges = set()

    # max possible edges for an undirected graph without self-loops
    max_edges = n * (n - 1) // 2
    m = int(max_edges * density)

    while len(edges) < m:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v:
            edges.add(tuple(sorted((u, v))))

    with open(filename, "w") as f:
        f.write(f"{n} {len(edges)}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")


# -------------------------
# USER INPUTS
# -------------------------
n_sparse = int(input("Enter number of nodes for SPARSE graph: "))
n_random = int(input("Enter number of nodes for RANDOM graph: "))
n_dense  = int(input("Enter number of nodes for DENSE graph: "))

# -------------------------
# GRAPH GENERATION
# -------------------------
generate_graph_file("sparse.txt", n_sparse, 0.1)   # 10% density
generate_graph_file("random.txt", n_random, 0.3)   # 30% density
generate_graph_file("dense.txt",  n_dense,  0.6)   # 60% density

print("\nGenerated graphs successfully:")
print(f"  sparse.txt → {n_sparse} nodes (10% density)")
print(f"  random.txt → {n_random} nodes (30% density)")
print(f"  dense.txt  → {n_dense} nodes (60% density)")
