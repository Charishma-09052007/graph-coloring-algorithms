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
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_probability:
                edges.append((u, v))
    return nodes, edges

def generate_dense_graph(n, edge_probability=0.70):
    nodes = list(range(n))
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_probability:
                edges.append((u, v))
    return nodes, edges

def generate_random_graph(n, edge_probability=0.45):
    nodes = list(range(n))
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_probability:
                edges.append((u, v))
    return nodes, edges


# ==========================================================
# 2. BACKTRACKING WITH TIMEOUT
# ==========================================================
class TimeoutException(Exception):
    pass

def is_valid(node, color, adj, coloring):
    for neighbor in adj[node]:
        if neighbor in coloring and coloring[neighbor] == color:
            return False
    return True

def backtrack_with_k_colors(nodes, adj, coloring, node_index, k, start_time, timeout):
    if timeout and (time.perf_counter() - start_time) > timeout:
        raise TimeoutException()
    
    if node_index == len(nodes):
        return True
    
    node = nodes[node_index]
    for color in range(k):
        if is_valid(node, color, adj, coloring):
            coloring[node] = color
            if backtrack_with_k_colors(nodes, adj, coloring, node_index + 1, k, start_time, timeout):
                return True
            del coloring[node]
    return False

def optimal_backtracking_coloring(nodes, edges, timeout=10.0):
    adj = {node: [] for node in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    nodes_sorted = sorted(nodes, key=lambda x: len(adj[x]), reverse=True)
    start_time = time.perf_counter()
    
    try:
        for k in range(1, len(nodes) + 1):
            coloring = {}
            if backtrack_with_k_colors(nodes_sorted, adj, coloring, 0, k, start_time, timeout):
                return coloring, k, False
    except TimeoutException:
        return {}, 0, True
    
    return {}, 0, False


# ==========================================================
# 3. OPTIMIZED GENETIC ALGORITHM
# ==========================================================
def build_adjacency(nodes, edges):
    adj = {node: [] for node in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def fitness(chrom, adj):
    conflicts = 0
    for node in chrom:
        for neighbor in adj[node]:
            if neighbor > node and chrom[node] == chrom[neighbor]:
                conflicts += 1
    return conflicts

def greedy_coloring(nodes, adj, k):
    coloring = {}
    for node in sorted(nodes, key=lambda x: len(adj[x]), reverse=True):
        neighbor_colors = {coloring[n] for n in adj[node] if n in coloring}
        for color in range(k):
            if color not in neighbor_colors:
                coloring[node] = color
                break
        else:
            coloring[node] = random.randint(0, k - 1)
    return coloring

def generate_population(nodes, adj, pop_size, k):
    population = []
    
    for _ in range(pop_size // 2):
        chrom = greedy_coloring(nodes, adj, k)
        population.append(chrom)
    
    for _ in range(pop_size - len(population)):
        chrom = {node: random.randint(0, k - 1) for node in nodes}
        population.append(chrom)
    
    return population

def crossover(p1, p2):
    return {node: (p1[node] if random.random() < 0.5 else p2[node]) for node in p1}

def smart_mutation(chrom, adj, k):
    mutated = chrom.copy()
    conflicts = set()
    
    for node in chrom:
        for neighbor in adj[node]:
            if chrom[node] == chrom[neighbor]:
                conflicts.add(node)
                break
    
    for node in conflicts:
        if random.random() < 0.8:
            neighbor_colors = {mutated[n] for n in adj[node]}
            valid = [c for c in range(k) if c not in neighbor_colors]
            mutated[node] = random.choice(valid) if valid else random.randint(0, k - 1)
    
    for node in mutated:
        if node not in conflicts and random.random() < 0.1:
            mutated[node] = random.randint(0, k - 1)
    
    return mutated

def genetic_algorithm(nodes, edges, k_estimate, pop_size=80, max_gen=200):
    adj = build_adjacency(nodes, edges)
    
    for k in range(k_estimate, 0, -1):
        population = generate_population(nodes, adj, pop_size, k)
        best_ever = None
        best_fitness = float('inf')
        stagnation = 0
        
        for gen in range(max_gen):
            scored = [(fitness(c, adj), c) for c in population]
            scored.sort(key=lambda x: x[0])
            
            curr_fit, curr_best = scored[0]
            
            if curr_fit < best_fitness:
                best_fitness = curr_fit
                best_ever = curr_best.copy()
                stagnation = 0
            else:
                stagnation += 1
            
            if best_fitness == 0:
                break
            
            if stagnation > 30:
                break
            
            elite = [c for _, c in scored[:pop_size // 10]]
            new_pop = elite.copy()
            
            while len(new_pop) < pop_size:
                t1 = random.sample(population, 3)
                t2 = random.sample(population, 3)
                p1 = min(t1, key=lambda x: fitness(x, adj))
                p2 = min(t2, key=lambda x: fitness(x, adj))
                
                child = crossover(p1, p2) if random.random() < 0.9 else p1.copy()
                child = smart_mutation(child, adj, k)
                new_pop.append(child)
            
            population = new_pop
        
        if best_fitness == 0:
            final_coloring = best_ever
            continue
        else:
            return final_coloring if 'final_coloring' in locals() else best_ever, \
                   0 if 'final_coloring' in locals() else best_fitness, \
                   k + 1
    
    return best_ever, best_fitness, 1


# ==========================================================
# 4. VISUALIZATION
# ==========================================================
def calculate_circular_layout(n):
    positions = {}
    for i in range(n):
        angle = 2 * pi * i / n
        positions[i] = (cos(angle), sin(angle))
    return positions

def draw_graph(ax, nodes, edges, coloring, title, positions):
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
              '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']
    
    for u, v in edges:
        ax.plot([positions[u][0], positions[v][0]],
                [positions[u][1], positions[v][1]],
                'k-', linewidth=2, alpha=0.6, zorder=1)
    
    for node in nodes:
        x, y = positions[node]
        color = '#CCCCCC' if coloring is None else colors[coloring[node] % len(colors)]
        circle = plt.Circle((x, y), 0.15, color=color, ec='black', linewidth=2.5, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(node), ha='center', va='center', fontsize=14, fontweight='bold', zorder=3)
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)


def run_comparison(nodes, edges, graph_type, n):
    positions = calculate_circular_layout(n)
    
    print(f"\n  🔍 Backtracking...")
    start = time.perf_counter()
    bt_coloring, bt_colors, timed_out = optimal_backtracking_coloring(nodes, edges, timeout=10.0)
    bt_time = time.perf_counter() - start
    
    if timed_out:
        print(f"     ⏱ TIMEOUT after {bt_time:.2f}s")
        bt_status = "TIMEOUT"
    else:
        print(f"     ✓ χ(G) = {bt_colors}, Time: {bt_time:.6f}s")
        bt_status = "OK"
    
    print(f"  🧬 Genetic Algorithm...")
    adj = build_adjacency(nodes, edges)
    max_degree = max(len(adj[n]) for n in nodes)
    k_estimate = max_degree + 1
    
    start = time.perf_counter()
    ga_coloring, ga_conflicts, ga_colors = genetic_algorithm(nodes, edges, k_estimate)
    ga_time = time.perf_counter() - start
    print(f"     → {ga_colors} colors, {ga_conflicts} conflicts, Time: {ga_time:.6f}s")
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle(f'{graph_type} Graph: n={n}, |E|={len(edges)}', fontsize=16, fontweight='bold', y=0.98)
    
    draw_graph(axes[0], nodes, edges, None, 'Original', positions)
    
    if bt_status == "OK":
        draw_graph(axes[1], nodes, edges, bt_coloring, f'Backtracking\nχ(G)={bt_colors}\n{bt_time:.6f}s', positions)
    else:
        axes[1].text(0.5, 0.5, f'TIMEOUT\n{bt_time:.2f}s', ha='center', va='center', fontsize=16)
        axes[1].axis('off')
    
    if ga_conflicts == 0 and bt_status == "OK" and ga_colors == bt_colors:
        color = 'green'
        status = f'✓ OPTIMAL\n{ga_colors} colors\n{ga_time:.6f}s'
    elif ga_conflicts == 0:
        color = 'orange'
        status = f'✓ Valid\n{ga_colors} colors\n{ga_time:.6f}s'
    else:
        color = 'red'
        status = f'{ga_colors} colors\n{ga_conflicts} conflicts\n{ga_time:.6f}s'
    
    draw_graph(axes[2], nodes, edges, ga_coloring, f'Genetic Alg\n{status}', positions)
    axes[2].title.set_color(color)
    
    plt.tight_layout()
    plt.show()
    
    return {
        'type': graph_type, 'n': n, 'edges': len(edges),
        'bt_colors': bt_colors if bt_status == "OK" else None,
        'bt_time': bt_time, 'bt_timeout': timed_out,
        'ga_colors': ga_colors, 'ga_time': ga_time, 'ga_conflicts': ga_conflicts
    }


# ==========================================================
# 5. RESULTS PRINTING
# ==========================================================
def print_results(results):
    print("\n" + "="*120)
    print("COMPREHENSIVE COMPARISON: BACKTRACKING vs GENETIC ALGORITHM")
    print("="*120)
    print(f"{'Graph':<10} {'n':<4} {'|E|':<5} {'BT χ(G)':<8} {'BT Time':<12} {'GA Colors':<10} "
          f"{'GA Time':<12} {'Speedup':<12} {'Status':<15}")
    print("-"*120)
    
    for r in results:
        if r['bt_timeout']:
            bt_str = "TIMEOUT"
            speedup_str = f"GA {r['bt_time']/r['ga_time']:.1f}x faster"
            status = "GA WINS"
        else:
            bt_str = str(r['bt_colors'])
            speedup = r['bt_time'] / r['ga_time']
            
            if speedup > 1:
                speedup_str = f"BT {speedup:.2f}x faster"
                status = "BT faster"
            else:
                speedup_str = f"GA {1/speedup:.2f}x faster"
                status = "GA faster"
            
            if r['ga_conflicts'] == 0 and r['ga_colors'] == r['bt_colors']:
                status = "✓ GA OPTIMAL"
        
        print(f"{r['type']:<10} {r['n']:<4} {r['edges']:<5} {bt_str:<8} "
              f"{r['bt_time']:<12.6f} {r['ga_colors']:<10} {r['ga_time']:<12.6f} "
              f"{speedup_str:<12} {status:<15}")
    
    print("="*120)
    print("\n📊 ANALYSIS:")
    print("• Backtracking = Exponential O(k^n)")
    print("• Genetic Algorithm = Polynomial O(Gen × Pop × n)")
    print("• GA wins for n ≥ 14 because BT explodes exponentially")


# ==========================================================
# 6. MAIN EXECUTION
# ==========================================================
random.seed(42)

print("="*120)
print("GRAPH COLORING ALGORITHM COMPARISON")
print("="*120)

results = []

test_configs = [
    (10, "Small"),
    (14, "Medium"),
    (18, "Large"),
    (20, "Large+"),
    (22, "Large++"),
    (24, "Large+++"),
]

for n, category in test_configs:
    print(f"\n{'='*120}")
    print(f"Testing n={n} ({category})")
    print('='*120)
    
    for graph_type, generator in [
        ("Sparse", generate_sparse_graph),
        ("Random", generate_random_graph),
        ("Dense", generate_dense_graph)
    ]:
        print(f"\n[{graph_type}]")
        nodes, edges = generator(n)
        print(f"  {len(nodes)} nodes, {len(edges)} edges")
        
        results.append(run_comparison(nodes, edges, graph_type, n))

print_results(results)

print("\n✅ COMPLETE!")