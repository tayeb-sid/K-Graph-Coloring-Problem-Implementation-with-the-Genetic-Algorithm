import networkx as nx
import random

def generate_connected_random_graph(n, p):
    """
    genere un graphe connexe de n noeuds 
    """
    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if random.random() < p:
                G.add_edge(i, j)

    components = list(nx.connected_components(G))
    while len(components) > 1:
        comp1 = random.choice(components)
        comp2 = random.choice(components)

        node1 = random.choice(list(comp1))
        node2 = random.choice(list(comp2))

        if node1 != node2:
            G.add_edge(node1, node2)

        components = list(nx.connected_components(G))

    return G


def adjacency_matrix(graph):
    """
    juste un simple affichage de la matrice d'adjacence d'un graphe
    """
    for node, neighbors in graph.adjacency():
        print(f"Node {node}: {list(neighbors)}")


