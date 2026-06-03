import random
import time
import matplotlib.pyplot as plt
from math import cos, sin, pi

# ==========================================================
# 1. GRAPH GENERATORS
# ==========================================================
def generate_sparse_graph(n, p=0.25):
    return list(range(n)), [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < p]

def generate_dense_graph(n, p=0.70):
    return list(range(n)), [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < p]

def generate_random_graph(n, p=0.45):
    return list(range(n)), [(u, v) for u in range(n) for v in range(u+1, n) if random.random() < p]


# ==========================================================
# 2. RLF ALGORITHM
# ==========================================================
def rlf_coloring(nodes, edges):
    graph = {node: set() for node in nodes}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    coloring, uncolored, color = {}, set(nodes), 0
    while uncolored:
        start = max(uncolored, key=lambda x: len(graph[x]))
        current = {start}
        coloring[start] = color
        uncolored.remove(start)

        updated = True
        while updated:
            updated = False
            for node in list(uncolored):
                if all(nei not in current for nei in graph[node]):
                    coloring[node] = color
                    current.add(node)
                    uncolored.remove(node)
                    updated = True
        color += 1
    return coloring


# ==========================================================
# 3. GENETIC ALGORITHM
# ==========================================================
def build_adjacency(nodes, edges):
    adj = {n: [] for n in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def fitness(chrom, adj):
    return sum(1 for n in chrom for nei in adj[n] if nei > n and chrom[n] == chrom[nei])

def greedy_coloring(nodes, adj, k):
    coloring = {}
    for node in sorted(nodes, key=lambda x: len(adj[x]), reverse=True):
        used = {coloring[n] for n in adj[node] if n in coloring}
        for c in range(k):
            if c not in used:
                coloring[node] = c
                break
        else:
            coloring[node] = random.randint(0, k-1)
    return coloring

def generate_population(nodes, adj, pop_size, k):
    pop = [greedy_coloring(nodes, adj, k) for _ in range(pop_size // 2)]
    pop += [{node: random.randint(0, k-1) for node in nodes} for _ in range(pop_size - len(pop))]
    return pop

def crossover(p1, p2):
    return {n: (p1[n] if random.random() < 0.5 else p2[n]) for n in p1}

def smart_mutation(chrom, adj, k):
    new = chrom.copy()
    for node in chrom:
        if any(chrom[node] == chrom[nei] for nei in adj[node]):
            used = {new[n] for n in adj[node]}
            valid = [c for c in range(k) if c not in used]
            new[node] = random.choice(valid) if valid else random.randint(0, k-1)
    return new

def genetic_algorithm(nodes, edges, k_estimate, pop_size=80, max_gen=200):
    adj = build_adjacency(nodes, edges)
    best_coloring, best_fit, best_colors = None, float("inf"), k_estimate

    for k in range(k_estimate, 0, -1):
        population = generate_population(nodes, adj, pop_size, k)
        stagnant = 0

        for _ in range(max_gen):
            scored = sorted([(fitness(c, adj), c) for c in population], key=lambda x: x[0])
            fit, top = scored[0]

            if fit < best_fit:
                best_fit, best_coloring, best_colors = fit, top.copy(), k
                stagnant = 0
            else:
                stagnant += 1

            if best_fit == 0 or stagnant > 30:
                break

            new = [c for _, c in scored[:pop_size // 10]]
            while len(new) < pop_size:
                p1 = min(random.sample(population, 3), key=lambda x: fitness(x, adj))
                p2 = min(random.sample(population, 3), key=lambda x: fitness(x, adj))
                child = crossover(p1, p2)
                new.append(smart_mutation(child, adj, k))
            population = new

        if best_fit == 0:
            continue
        else:
            return best_coloring, best_fit, k+1
    return best_coloring, best_fit, best_colors


# ==========================================================
# 4. VISUALIZATION
# ==========================================================
def node_positions(n): return {i: (cos(2*pi*i/n), sin(2*pi*i/n)) for i in range(n)}

def draw_graph(ax, nodes, edges, coloring, title, pos):
    palette = ['#FF6B6B','#4ECDC4','#45B7D1','#FFA07A','#98D8C8','#F7DC6F','#BB8FCE','#85C1E2','#F8B739','#52B788']
    for u,v in edges:
        ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],'k-',alpha=0.6,zorder=1)
    for n in nodes:
        x,y = pos[n]
        color = palette[coloring[n] % len(palette)] if coloring else "#CCCCCC"
        ax.add_patch(plt.Circle((x,y),0.15,color=color,ec="black",lw=2.3,zorder=2))
        ax.text(x,y,str(n),ha='center',va='center')
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title,fontweight="bold")


# ==========================================================
# 5. RUN COMPARISON
# ==========================================================
def run_comparison(nodes, edges, graph_type, n):
    pos = node_positions(n)

    start = time.perf_counter()
    rlf = rlf_coloring(nodes, edges)
    rlf_time = time.perf_counter() - start
    rlf_colors = max(rlf.values()) + 1

    adj = build_adjacency(nodes, edges)
    k_est = max(len(adj[n]) for n in nodes) + 1

    start = time.perf_counter()
    ga_coloring, ga_conflicts, ga_colors = genetic_algorithm(nodes, edges, k_est)
    ga_time = time.perf_counter() - start

    fig, ax = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle(f"{graph_type} Graph — n={n}, |E|={len(edges)}", fontsize=16)

    draw_graph(ax[0], nodes, edges, None, "Original", pos)
    draw_graph(ax[1], nodes, edges, rlf, f"RLF — {rlf_colors} colors\n{rlf_time:.6f}s", pos)

    status = "Valid" if ga_conflicts == 0 else f"{ga_conflicts} conflicts"
    title = f"Genetic — {ga_colors} colors\n{ga_time:.6f}s\n{status}"
    draw_graph(ax[2], nodes, edges, ga_coloring, title, pos)
    ax[2].title.set_color("green" if ga_conflicts == 0 and ga_colors <= rlf_colors else "red")

    plt.tight_layout(); plt.show()

    return {
        "type": graph_type, "n": n, "edges": len(edges),
        "rlf_colors": rlf_colors, "rlf_time": rlf_time,
        "ga_colors": ga_colors, "ga_time": ga_time, "ga_conflicts": ga_conflicts
    }


# ==========================================================
# 6. PRINT RESULTS TABLE
# ==========================================================
def print_results(results):
    print("\n" + "="*120)
    print("COMPARISON: RLF vs GENETIC ALGORITHM")
    print("="*120)
    print(f"{'Graph':<10}{'n':<4}{'|E|':<6}{'RLF χ(G)':<10}{'RLF Time':<12}"
          f"{'GA Colors':<10}{'GA Time':<12}{'Winner':<14}")
    print("-"*120)

    for r in results:
        if r["ga_conflicts"] == 0:
            if r["ga_colors"] < r["rlf_colors"]:
                winner = "Genetic (best χ)"
            elif r["ga_colors"] > r["rlf_colors"]:
                winner = "RLF (best χ)"
            else:
                winner = "Tie (Same χ)"
        else:
            winner = "RLF (valid, GA not)"
        print(f"{r['type']:<10}{r['n']:<4}{r['edges']:<6}{r['rlf_colors']:<10}{r['rlf_time']:<12.6f}"
              f"{r['ga_colors']:<10}{r['ga_time']:<12.6f}{winner:<14}")

    print("="*120)
    print("\n Interpretation:")
    print("• RLF usually achieves a small number of colors but is slower for large graphs.")
    print("• GA is much faster and often matches RLF's result, but may produce conflicts on hard graphs.")
    print("• When both are conflict-free, the algorithm using fewer colors wins.")


# ==========================================================
# 7. MAIN
# ==========================================================
random.seed(42)
print("="*120)
print("GRAPH COLORING — RLF vs GENETIC ALGORITHM COMPARISON")
print("="*120)

results = []
sizes = [(10, "Small"), (14, "Medium"), (18, "Large"), (20, "Large+"), (22, "Large++")]

for n, label in sizes:
    print(f"\n{'='*120}\nTesting n={n} ({label})\n{'='*120}")
    for t, gen in [("Sparse", generate_sparse_graph),
                   ("Random", generate_random_graph),
                   ("Dense", generate_dense_graph)]:
        nodes, edges = gen(n)
        print(f"[{t}] {len(edges)} edges")
        results.append(run_comparison(nodes, edges, t, n))

print_results(results)
print("\nCOMPLETE")
