from visualisation import *
from genetic_algorithm import *
from graph import *
from extra import * 

n_nodes=45
proba=0.5
# graph=generate_connected_random_graph(n_nodes,proba)

# save_graph(graph)
graph=load_graph('graphs/graph_45_50.pkl')
n_generations=80
population_size=50
mutation_rate=0.5
selection_methode="elitist"
crossover_methode="single_point"
num_selected= 3
tournament_size= 3

optimal_coloring = genetic_algorithm(graph,n_generations,population_size,selection_methode,num_selected,tournament_size,mutation_rate,crossover_methode)
f,conflicted_pairs = fitness(optimal_coloring,graph)
if f<1 :
    print("PAS DE SOLUTION VALABLE") 


print_coloriage(optimal_coloring,graph)
print("conflicted pairs: ",conflicted_pairs)
print("colors used: ", len(set(optimal_coloring)))
#  plot_graph(graph,optimal_coloring)

params = {
    "n_generations": n_generations,
    "population_size": population_size,
    "mutation_rate": mutation_rate,
    "selection_methode": selection_methode,
    "crossover_methode": crossover_methode,
    "num_selected": num_selected,
    "tournament_size": tournament_size
}

save_experiment(graph, optimal_coloring, params, path_dir="experiments", n=n_nodes, p=proba)
