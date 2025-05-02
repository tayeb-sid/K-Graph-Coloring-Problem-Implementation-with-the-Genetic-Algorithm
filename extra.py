import pickle
import os
from genetic_algorithm import *

def save_graph(graph, path_dir="graphs"):
    os.makedirs(path_dir, exist_ok=True)
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    base_filename = f"graph_{n}_{m}"
    filename = f"{base_filename}.pkl"
    full_path = os.path.join(path_dir, filename)
    
    # If file exists, add suffix
    counter = 1
    while os.path.exists(full_path):
        filename = f"{base_filename}_{counter}.pkl"
        full_path = os.path.join(path_dir, filename)
        counter += 1

    with open(full_path, "wb") as f:
        pickle.dump(graph, f)

    print(f"Graph saved to: {full_path}")


def load_graph(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def save_experiment(graph, coloring, params, path_dir):
    os.makedirs(path_dir, exist_ok=True)
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    base_filename = f"experiment_{n}_{m}"
    filename = f"{base_filename}.pkl"
    full_path = os.path.join(path_dir, filename)
    
    # If file exists, add suffix
    counter = 1
    while os.path.exists(full_path):
        filename = f"{base_filename}_{counter}.pkl"
        full_path = os.path.join(path_dir, filename)
        counter += 1

    data = {
        "graph": graph,
        "solution_coloring": coloring,
        "parameters": params
    }

    with open(full_path, "wb") as f:
        pickle.dump(data, f)

    print(f"Experiment saved to: {full_path}")


def load_experiment(path):
    with open(path, "rb") as f:
        data = pickle.load(f)

    graph = data["graph"]
    coloring = data["solution_coloring"]
    params = data["parameters"]

    # === Print summary ===
    fit, conflicted_pairs = fitness(coloring, graph)
    print(f"\n✅ Loaded experiment from: {path}")
    print(f"📊 Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    print("📌 Parameters:")
    for k, v in params.items():
        if k == "num_selected" and params.get("selection_methode") == "elitist":
            continue
        if k == "tournament_size" and params.get("selection_methode") != "tournament":
            continue
        if k == "crossoverP2" and params.get("crossover_methode") == "single_point":
            continue
        print(f"  {k}: {v}")
    print(f"🎯 Fitness: {fit}")
    print(f"⚠️ Conflicted pairs: {conflicted_pairs}")
    print(f"🎨 Colors used: {len(set(coloring))}")
    print("🖍️ Coloring:")
    print_coloriage(coloring, graph)
    print("=================================\n")

    return graph, coloring, params


def are_params_equal(p1, p2):
    return all(p1.get(k) == p2.get(k) for k in p1)
