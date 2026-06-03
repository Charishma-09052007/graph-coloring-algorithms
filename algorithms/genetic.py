import random

# ---------------------------------------------------------
# Generate a random graph
# ---------------------------------------------------------
def generate_graph(n, edge_prob=0.3):
    edges = []
    for u in range(n):
        for v in range(u+1, n):
            if random.random() < edge_prob:
                edges.append((u, v))
    return edges

# ---------------------------------------------------------
# Build adjacency list
# ---------------------------------------------------------
def build_adj(n, edges):
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

# ---------------------------------------------------------
# Fitness = number of conflicts
# ---------------------------------------------------------
def fitness(chrom, adj):
    conflicts = 0
    for u in adj:
        for v in adj[u]:
            if chrom[u] == chrom[v]:
                conflicts += 1
    return conflicts

# ---------------------------------------------------------
# Crossover
# ---------------------------------------------------------
def crossover(p1, p2):
    point = random.randint(1, len(p1)-1)
    return p1[:point] + p2[point:]

# ---------------------------------------------------------
# Mutation
# ---------------------------------------------------------
def mutate(chrom, k):
    idx = random.randint(0, len(chrom)-1)
    chrom[idx] = random.randint(0, k-1)

# ---------------------------------------------------------
# Genetic Algorithm for Graph Coloring
# ---------------------------------------------------------
def GA_color_graph(n, edges, k=4, pop_size=40, generations=200):
    adj = build_adj(n, edges)

    # Initial population
    population = [[random.randint(0, k-1) for _ in range(n)] for _ in range(pop_size)]

    for gen in range(generations):

        # Sort by fitness
        population.sort(key=lambda c: fitness(c, adj))

        # If perfect coloring found
        if fitness(population[0], adj) == 0:
            return population[0], 0

        # New population
        new_pop = population[:5]  # Keep best 5

        while len(new_pop) < pop_size:
            p1 = random.choice(population[:20])
            p2 = random.choice(population[:20])
            child = crossover(p1, p2)

            if random.random() < 0.2:
                mutate(child, k)

            new_pop.append(child)

        population = new_pop

    # Return best even if not perfect
    return population[0], fitness(population[0], adj)

# ---------------------------------------------------------
# RUN SIMPLE EXAMPLE
# ---------------------------------------------------------
n = 12
edges = generate_graph(n, 0.3)

coloring, conflicts = GA_color_graph(n, edges, k=4)

print("Edges:", edges)
print("Coloring:", coloring)
print("Conflicts:", conflicts)