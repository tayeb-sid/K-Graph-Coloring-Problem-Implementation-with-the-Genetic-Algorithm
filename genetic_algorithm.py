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
    
    used_colors=len(set(coloriage))
    nb_conflicts=len(conflicted_pairs)
    if nb_conflicts==0:
        f=1+(1/used_colors)
    else:
        f=1/(1+nb_conflicts)
    return round(f,3),conflicted_pairs

def generer_coloriage(n_nodes):
    """
        genere un coloriage aleatoire pour un graphe de n noeuds avec k couleurs
        un coloriage est un tableau dont les indices+1 sont les numeros de noeuds (indice 0 => noeud numero 1) et la valeur de chaque case est une couleur (de 0 a k-1)
    """
    if n_nodes < 1:
        raise ValueError("Le nombre de couleurs doit être au moins 1.")
    return [random.randint(0, n_nodes - 1) for _ in range(n_nodes)]

def generer_population(p_size,n_nodes):
    """
    genere une population de taille p 
    une population est une matrice dont chaque ligne est un coloriage 
    """
    if p_size < 1:
        raise ValueError("Le nombre d'individus doit être au moins 1.")
    population=[]
    for i in range(p_size):
        population.append(generer_coloriage(n_nodes))
    return population
def selection(population, graph, method, num_selected=None, tournament_size=None):
    if method == "elitist":
        return elitist_selection(population, graph)
    elif method == "roulette":
        return roulette_selection(population, graph, num_selected)
    elif method == "rank":
        return rank_selection(population, graph, num_selected)
    elif method == "tournament":
        return tournament_selection(population, graph, num_selected, tournament_size)
    else:
        raise ValueError("Méthode de sélection inconnue")

def elitist_selection(population,graph):
    return sorted(population, key=lambda genome: fitness(genome, graph), reverse=True)[:2]

def roulette_selection(population,graph, num_selected):
    # Calcul du fitness pour chaque individu
    fitnesses = [fitness(genome, graph)[0] for genome in population] 
    
    # Calcul des probabilités de sélection
    total_fitness = sum(fitnesses)
    probabilities = [f / total_fitness for f in fitnesses]
    
    # Sélection par roue de la roulette
    selected = random.choices(population, weights=probabilities, k=num_selected)
    
    return selected

def rank_selection(population, graph, num_selected) :
    # Calcul des fitness pour chaque individu
    fitnesses = [fitness(genome, graph)[0] for genome in population]
    
    # Tri des individus selon leur fitness
    sorted_population = sorted(zip(fitnesses, population), reverse=True)
    
    # Extraction des individus triés
    sorted_individuals = [ind for _, ind in sorted_population]
    
    # Attribuer un rang à chaque individu (de 1 à N)
    ranks = list(range(1, len(population) + 1))
    
    # Calculer la probabilité de sélection pour chaque individu
    total_rank = sum(ranks)
    probabilities = [rank / total_rank for rank in ranks]
    
    # Sélectionner les individus en fonction de leurs rangs
    selected = random.choices(sorted_individuals, weights=probabilities, k=num_selected)
    
    return selected

def tournament_selection(population, graph, num_selected, tournament_size=3):
    selected = []

    for _ in range(num_selected):
        # Sélectionner un sous-ensemble aléatoire de la population pour le tournoi
        tournament = random.sample(population, tournament_size)
        
        # Calculer les fitness pour chaque individu du tournoi
        tournament_fitnesses = [fitness(individual, graph)[0] for individual in tournament]

        # Trouver l'individu avec le meilleur fitness (le gagnant du tournoi)
        winner = tournament[tournament_fitnesses.index(max(tournament_fitnesses))]

        # Ajouter le gagnant du tournoi à la liste des sélectionnés
        selected.append(winner)

    return selected

def crossover(parent1, parent2, method,crossoverPoint1):
    if method=="one_point":
        return single_point_crossover(parent1,parent2,crossoverPoint1)
    else :
        return two_point_crossover(parent1,parent2)

def single_point_crossover(parent1, parent2,point):
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def two_point_crossover(parent1, parent2):
    # Choisir deux points de croisement aléatoires
    point1 = random.randint(1, len(parent1) - 1)  # Première position (entre 1 et len-1)
    print("point1",point1)
    point2 = random.randint(point1, len(parent1))  # Deuxième position (entre point1 et len)
    print("point2",point2)
    # Créer les enfants en échangeant les segments
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    return child1, child2

def mutation(genome, mutation_rate):
    if random.random() > mutation_rate:
        i, j = random.sample(range(len(genome)), 2)
        genome[i], genome[j] = genome[j], genome[i]
    return genome

def genetic_algorithm(graph, n_generations, population_size,selection_type,num_selected,tournament_size,mutation_rate,crossover_methode,crossoverPoint1):
    population=generer_population(population_size,graph.number_of_nodes())
    population= sorted(population, key=lambda genome: fitness(genome, graph), reverse=True)
    print("*****population initiale*****")
    print_population(population,graph)
    best=population[0]
    print("--------------")
    print("best individual: ")
    print_coloriage(best,graph)
    for i in range(n_generations):
        print("-------------iteration ",i+1,"--------------")
        parents=selection(population,graph,selection_type,num_selected,tournament_size)
        p1=parents[0]
        p2=parents[1]
        print("parents: ")
        print_coloriage(p1,graph)
        print_coloriage(p2,graph)
        c1,c2=crossover(p1,p2,crossover_methode,crossoverPoint1)
        print("children: ")
        print_coloriage(c1,graph)
        print_coloriage(c2,graph)
        c1=mutation(c1,mutation_rate)
        c2=mutation(c2,mutation_rate)
        print("mutated children: ")
        print_coloriage(c1,graph)
        print_coloriage(c2,graph)
        population.append(c1)
        population.append(c2)
        population= sorted(population, key=lambda genome: fitness(genome, graph), reverse=True)
        print("*****Population ",i+1,"*****")
        print_population(population,graph)
        print()
        print("best: ")
        print_coloriage(best,graph)
        if fitness(population[0],graph)[0]>fitness(best,graph)[0]:
            print("new best: ")
            best=population[0]
            print_coloriage(best,graph)
        print("********************\n")

        
    return best



def print_coloriage(coloriage,graph):
    print(coloriage,'|',fitness(coloriage,graph)[0])


def print_population(population,graph):
    """
    affiche la population
    """
    for coloriage in population:
        print_coloriage(coloriage,graph)