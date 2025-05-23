import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from genetic_algorithm import fitness
import random
def generate_color_palette(k=10000):
    """
    genere la palette de couleurs a utiliser dans l'affichage
    """
    cmap = cm.get_cmap("tab20", k)  
    palette=[cmap(i) for i in range(k)]
    for i in range (5):
        random.shuffle(palette)
    return palette
def plot_graph(G, coloriage):
    """
    affiche le graphe
    """
    color_palette =generate_color_palette()
   


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


