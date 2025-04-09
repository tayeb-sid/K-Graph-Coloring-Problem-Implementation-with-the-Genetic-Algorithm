from visualisation import *
from genetic_algorithm import *
from graph import *

n_nodes=5
proba=0.6
k=4
color_palette=generate_color_palette(k)

graph=generate_connected_random_graph(n_nodes,proba)

pop= generer_population(5,n_nodes,k)
print_population(pop,graph)

p1,p2=elitist_selection(pop,graph)

print(p1,fitness(p1,graph)[0],p2,fitness(p1,graph)[0])