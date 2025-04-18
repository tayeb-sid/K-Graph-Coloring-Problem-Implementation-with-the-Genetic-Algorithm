from visualisation import *
from genetic_algorithm import *
from graph import *

n_nodes=4
proba=0.5
graph=generate_connected_random_graph(n_nodes,proba)

n_generations=5
population_size=5
mutation_rate=0.6
selection_methode="roulette"
crossover_methode="two_point"
crossoverP1=n_nodes//2
num_selected= 3
tournament_size= 3

optimal_coloring = genetic_algorithm(graph,n_generations,population_size,selection_methode,num_selected,tournament_size,mutation_rate,crossover_methode,crossoverP1)
f,conflicted_pairs = fitness(optimal_coloring,graph)
if f<1 :
    print("PAS DE SOLUTION VALABLE") 
print_coloriage(optimal_coloring,graph)
print("conflicted pairs: ",conflicted_pairs)
print("colors used: ", len(set(optimal_coloring)))
plot_graph(graph,optimal_coloring)

