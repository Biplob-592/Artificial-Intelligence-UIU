# A* Search Algorithm Implementation for Romania Road Map

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Romania map edges with distances
ROMANIA_EDGES = [
    ('Eforie', 'Hirsova', 86),
    ('Hirsova', 'Eforie', 86), ('Hirsova', 'Urziceni', 98),
    ('Urziceni', 'Hirsova', 98), ('Urziceni', 'Vaslui', 142), ('Urziceni', 'Bucharest', 85),
    ('Vaslui', 'Iasi', 92), ('Vaslui', 'Urziceni', 142),
    ('Iasi', 'Neamt', 87), ('Iasi', 'Vaslui', 92),
    ('Neamt', 'Iasi', 87),
    ('Bucharest', 'Giurgiu', 90), ('Bucharest', 'Urziceni', 85), ('Bucharest', 'Pitesti', 101), ('Bucharest', 'Fagaras', 211),
    ('Giurgiu', 'Bucharest', 90),
    ('Fagaras', 'Bucharest', 211), ('Fagaras', 'Sibiu', 99),
    ('Pitesti', 'Bucharest', 101), ('Pitesti', 'Craiova', 138), ('Pitesti', 'Rimnicu Vilcea', 97),
    ('Craiova', 'Rimnicu Vilcea', 146), ('Craiova', 'Pitesti', 138), ('Craiova', 'Drobeta', 120),
    ('Rimnicu Vilcea', 'Pitesti', 97), ('Rimnicu Vilcea', 'Craiova', 146), ('Rimnicu Vilcea', 'Sibiu', 80),
    ('Sibiu', 'Fagaras', 99), ('Sibiu', 'Rimnicu Vilcea', 80), ('Sibiu', 'Oradea', 151), ('Sibiu', 'Arad', 140),
    ('Drobeta', 'Craiova', 120), ('Drobeta', 'Mehadia', 75),
    ('Mehadia', 'Drobeta', 75), ('Mehadia', 'Lugoj', 70),
    ('Lugoj', 'Mehadia', 70), ('Lugoj', 'Timisoara', 111),
    ('Timisoara', 'Lugoj', 111), ('Timisoara', 'Arad', 118),
    ('Arad', 'Timisoara', 118), ('Arad', 'Sibiu', 140), ('Arad', 'Zerind', 75),
    ('Zerind', 'Arad', 75), ('Zerind', 'Oradea', 71),
    ('Oradea', 'Zerind', 71), ('Oradea', 'Sibiu', 151)
]

# Calculating Bucharest's heuristic
student_id = "0112230592"
last_two = int(student_id[-2:])
bucharest_h = (last_two ** 2) + 1

h_SLD = {
    'Arad': 366, 'Bucharest': bucharest_h, 'Craiova': 160, 'Drobeta': 242,
    'Eforie': 161, 'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226,
    'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100,
    'Rimnicu Vilcea': 193, 'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80,
    'Vaslui': 199, 'Zerind': 374
}

def heuristic(city):
    # Returns the straight-line heuristic for the city
    return h_SLD.get(city, 0)

# NetworkX graph creation
def build_romania_graph(edge_list):
    G = nx.Graph()
    for city_from, city_to, dist in edge_list:
        G.add_edge(city_from, city_to, weight=dist)
    return G

G = build_romania_graph(ROMANIA_EDGES)

# A* Search implementation
def astar(G, start, goal, heuristic_func):
    visited = set()
    open_set = {start}
    g_costs = {start: 0}
    parents = {start: None}
    while open_set:
        current = min(open_set, key=lambda x: g_costs.get(x, float('inf')) + heuristic_func(x))
        if current == goal:
            node = current
            seq = []
            while node:
                seq.append(node)
                node = parents[node]
            return seq[::-1]
        open_set.remove(current)
        visited.add(current)
        for neighbor in G.neighbors(current):
            if neighbor in visited:
                continue
            tentative = g_costs[current] + G[current][neighbor]['weight']
            if neighbor not in g_costs or tentative < g_costs[neighbor]:
                parents[neighbor] = current
                g_costs[neighbor] = tentative
                open_set.add(neighbor)
    return None

# Determining SL_NO from my student ID
SL_NO = (int(student_id) % 10) + 1
start_city, end_city = None, None
if SL_NO == 3:
    start_city = "Lugoj"
    end_city = "Neamt"

# Run search and show output
result_path = astar(G, start_city, end_city, heuristic)
print(f"Shortest Path from {start_city} to {end_city}:", result_path)

# Animation of the path finding process
def animate_path(G, path, heuristic_func):
    if not path:
        print("No path to animate!")
        return
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(10, 8))
    edges_on_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
    def update(step):
        ax.clear()
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1200, ax=ax,
                edge_color="gray", width=1, font_weight='bold')
        # heuristic value for each city
        for n, (x, y) in pos.items():
            ax.text(x, y + 0.07, f"h={heuristic_func(n)}", color="green", ha='center', fontsize=12)
        # Highlight current path nodes and edges
        nx.draw_networkx_nodes(G, pos, nodelist=path[:step+1], node_color="orange", node_size=1200, ax=ax)
        if step > 0:
            nx.draw_networkx_edges(G, pos, edgelist=edges_on_path[:step], edge_color="orange", width=3, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"),
                                    font_color="red", font_size=10, ax=ax)
        ax.set_title(f"A* Search: Step {step + 1}/{len(path)} ({path[step]})")
        ax.axis('off')
    anim = FuncAnimation(fig, update, frames=len(path), interval=1800, repeat=False)
    plt.show()

if result_path:
    animate_path(G, result_path, heuristic)