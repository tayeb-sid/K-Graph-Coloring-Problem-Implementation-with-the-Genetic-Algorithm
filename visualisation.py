import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def generate_color_palette(k):
    """
    genere la palette de couleurs a utiliser dans l'affichage
    """
    cmap = cm.get_cmap("tab20", k)  
    return [cmap(i) for i in range(k)]
def plot_graph(G, coloriage, color_palette):
    """
    affiche le graphe
    """
    node_colors = [color_palette[color-1] for color in coloriage]
    plt.figure(figsize=(6, 6))
    nx.draw(G, with_labels=True, node_color=node_colors, edge_color="gray", node_size=500, font_size=10)
    plt.show()

def describe_coloriage(coloring):
    """
    juste une simple description du coloriage ex: [1,0,1]=> noeud 1 couleur 1 , noeud 2 couleur 0  et noeud 3 couleur 1
    """
    for node, color in enumerate(coloring):
        print(f"Node {node + 1}: Color {color}")

def print_population(population):
    """
    affiche la population
    """
    for coloriage in population:
        print(coloriage)