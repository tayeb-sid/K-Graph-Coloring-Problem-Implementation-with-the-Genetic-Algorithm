from visualisation import *
from genetic_algorithm import *
from graph import *

n_nodes=5
proba=0.6
k=4
color_palette=generate_color_palette(k)

graph=generate_connected_random_graph(n_nodes,proba)
coloriage=generer_coloriage(n_nodes,k)

print("coloriage: ",coloriage)
f,conflicted_pairs=fitness(coloriage,graph)
print("fitness : ",f," conflicted_pairs ",conflicted_pairs)
describe_coloriage(coloriage)
plot_graph(graph,coloriage,color_palette)
