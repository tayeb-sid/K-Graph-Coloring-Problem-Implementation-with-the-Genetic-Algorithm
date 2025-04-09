import random

def fitness(coloriage,graph):
    """
    fitness =1/1+nb_conflits (+1 /nb_couleurs_utilisées à ajouter plus tard)
    cette fonction retourne la fitness d'un coloriage et les noeuds qui sont en conflit si y'en a 
    """
    conflicted_pairs=set()
    for node,color in enumerate(coloriage):
        node_neighbors=list(graph.neighbors(node+1))
        for neighbor in node_neighbors:
            if coloriage[node]==coloriage[neighbor-1]:
                conflicted_pairs.add(tuple(sorted([node + 1, neighbor])))
    
    return round(1/(1+len(conflicted_pairs)),3),conflicted_pairs

def generer_coloriage(n_nodes,k):
    """
        genere un coloriage aleatoire pour un graphe de n noeuds avec k couleurs
        un coloriage est un tableau dont les indices+1 sont les numeros de noeuds (indice 0 => noeud numero 1) et la valeur de chaque case est une couleur (de 0 a k-1)
    """
    if k < 1:
        raise ValueError("Le nombre de couleurs doit être au moins 1.")
    return [random.randint(0, k - 1) for _ in range(n_nodes)]

def generer_population(p_size,n_nodes,k):
    """
    genere une population de taille p 
    une population est une matrice dont chaque ligne est un coloriage 
    """
    population=[]
    for i in range(p_size):
        population.append(generer_coloriage(n_nodes,k))
    return population

def selection(population,graph,method="elitist"):
    pass

def elitist_selection(population,graph):
    return sorted(population, key=lambda genome: fitness(genome, graph), reverse=True)[:2]


def crossover(parent1, parent2, method="single_point"):
    pass

def mutation(genome, mutation_rate):
    pass

def genetic_algorithm(graph, n_generations, population_size, mutation_rate, k):
    pass