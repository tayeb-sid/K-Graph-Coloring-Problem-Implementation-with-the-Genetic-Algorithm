import tkinter as tk
from tkinter import messagebox, filedialog
import os
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import time
from genetic_algorithm import *
from graph import *
from extra import save_graph

# === Global state ===
last_generated_graph = None
last_coloring = None
last_fitness = None
last_graph_file_name = None  # To store the base name of the graph file

# === Core functions ===
def generate_graph():
    global last_generated_graph
    try:
        n = int(entry_n.get())
        p = float(slider_p.get()) / 100.0
        if n <= 0 or not (0 <= p <= 1):
            raise ValueError("Invalid input values.")

        graph = generate_connected_random_graph(n, p)
        last_generated_graph = graph
        plot_graph(graph)
        messagebox.showinfo("Success", f"Graph with {n} nodes and probability {p*100}% generated!")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def save_current_graph():
    if last_generated_graph is None:
        messagebox.showwarning("Warning", "No graph to save. Please generate or load a graph first.")
        return
    try:
        save_graph(last_generated_graph, path_dir="graphs")
        messagebox.showinfo("Saved", "Graph successfully saved.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save graph: {e}")

def load_graph_from_file():
    global last_generated_graph, last_graph_file_name
    file_path = filedialog.askopenfilename(title="Select a graph file", filetypes=[("Pickle Files", "*.pkl")])
    if file_path:
        try:
            with open(file_path, "rb") as f:
                graph = pickle.load(f)
                last_generated_graph = graph
                last_graph_file_name = os.path.splitext(os.path.basename(file_path))[0]  # Get the base name of the file (without .pkl)
                plot_graph(graph)
                show_experiment_page(graph)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load graph:\n{e}")

def plot_graph(G, coloring=None, title=None):
    plt.figure(figsize=(6, 6))
    if coloring:
        nx.draw(G, with_labels=True, node_color=coloring, cmap=plt.cm.rainbow, node_size=500, font_size=10)
    else:
        nx.draw(G, with_labels=True, node_color="lightblue", edge_color="gray", node_size=500, font_size=10)
    if title:
        plt.title(title)
    plt.show()

def run_experiment():
    global last_coloring, last_fitness, last_generated_graph, last_graph_file_name

    if last_generated_graph is None:
        messagebox.showerror("Error", "No graph loaded. Please generate or load a graph first.")
        return

    try:
        n_generations = int(entry_gen.get())
        population_size = int(entry_pop.get())
        mutation_rate = float(slider_mutation_rate.get()) / 100.0
        selection_type = selection_method_var.get()
        crossover_method = crossover_method_var.get()

        num_selected = None
        tournament_size = None

        if selection_type in ["roulette", "rank"]:
            num_selected = int(entry_num_selected.get())
        elif selection_type == "tournament":
            num_selected = int(entry_num_selected.get())
            tournament_size = int(entry_tournament_size.get())

        start_time = time.time()

        last_coloring = genetic_algorithm(
            last_generated_graph,
            n_generations,
            population_size,
            selection_type,
            num_selected,
            tournament_size,
            mutation_rate,
            crossover_method
        )

        last_fitness, _ = fitness(last_coloring, last_generated_graph)

        execution_time = time.time() - start_time
        num_colors_used = len(set(last_coloring))  # Count the number of unique colors used

        result_text = f"Coloring: {last_coloring}\nFitness: {last_fitness}\nExecution Time: {execution_time:.2f} seconds\nNumber of Colors Used: {num_colors_used}"

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, result_text)

        show_results(last_coloring, last_fitness)

        # Log results to the experiment file
        if last_graph_file_name:
            graph_name = last_graph_file_name
        else:
            graph_name = "graph"

        log_dir = "graphs"
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"{graph_name}_experiments.txt")

        # Retrieve the last experiment number to increment it
        experiment_counter = 1
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if "==== Experiment" in line:
                        experiment_counter += 1

        # Log experiment results with a counter
        with open(log_file_path, 'a') as file:
            file.write(f"\n==== Experiment {experiment_counter} ====\n")
            file.write(f"Selection Type: {selection_type}\n")
            file.write(f"Crossover Method: {crossover_method}\n")
            file.write(f"Mutation Rate: {mutation_rate * 100}%\n")
            file.write(f"Generations: {n_generations}\n")
            file.write(f"Population Size: {population_size}\n")
            file.write(f"Execution Time: {execution_time:.2f} seconds\n")
            file.write(f"Fitness (not a valid solution if < 1): {last_fitness}\n")
            file.write(f"Number of Colors Used: {num_colors_used}\n")  # Added number of colors used
            file.write(f"Coloring: {last_coloring}\n")

    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input value: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_results(coloring, fit):
    if len(coloring) != last_generated_graph.number_of_nodes():
        messagebox.showerror("Error", "Coloring does not match the number of nodes in the graph.")
        return

    result_frame.pack_forget()
    result_frame.pack(pady=20)

def show_main_page():
    experiment_frame.pack_forget()
    result_frame.pack_forget()
    main_frame.pack(pady=50)

def show_experiment_page(graph):
    main_frame.pack_forget()
    label_graph_info.config(text=f"Graph loaded with:\n\u2022 {graph.number_of_nodes()} nodes\n\u2022 {graph.number_of_edges()} edges")
    experiment_frame.pack(pady=20)

def update_ui_for_selection_method(*args):
    label_num_selected.grid_remove()
    entry_num_selected.grid_remove()
    label_tournament_size.grid_remove()
    entry_tournament_size.grid_remove()

    method = selection_method_var.get()
    if method in ["roulette", "rank"]:
        label_num_selected.grid(row=5, column=0, sticky="e")
        entry_num_selected.grid(row=5, column=1)
    elif method == "tournament":
        label_num_selected.grid(row=5, column=0, sticky="e")
        entry_num_selected.grid(row=5, column=1)
        label_tournament_size.grid(row=6, column=0, sticky="e")
        entry_tournament_size.grid(row=6, column=1)

# === GUI Setup ===
root = tk.Tk()
root.title("Graph Coloring GUI")

main_frame = tk.Frame(root)

label_n = tk.Label(main_frame, text="Number of Nodes (n):")
label_n.grid(row=0, column=0, padx=10, pady=10)
entry_n = tk.Entry(main_frame)
entry_n.grid(row=0, column=1, padx=10, pady=10)

label_p = tk.Label(main_frame, text="Edge Probability (p) (%):")
label_p.grid(row=1, column=0, padx=10, pady=10)
slider_p = tk.Scale(main_frame, from_=0, to=100, orient="horizontal")
slider_p.set(50)
slider_p.grid(row=1, column=1)

generate_button = tk.Button(main_frame, text="Generate Graph", command=generate_graph)
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

save_button = tk.Button(main_frame, text="Save Graph", command=save_current_graph)
save_button.grid(row=3, column=0, columnspan=2, pady=10)

load_button = tk.Button(main_frame, text="Load Graph", command=load_graph_from_file)
load_button.grid(row=4, column=0, columnspan=2, pady=10)

experiment_frame = tk.Frame(root)

label_graph_info = tk.Label(experiment_frame, text="", font=("Arial", 12))
label_graph_info.grid(row=0, column=0, columnspan=2, pady=10)

entry_gen = tk.Entry(experiment_frame)
entry_pop = tk.Entry(experiment_frame)
slider_mutation_rate = tk.Scale(experiment_frame, from_=0, to=100, orient="horizontal")
slider_mutation_rate.set(40)

selection_method_var = tk.StringVar()
selection_method_var.set("elitist")
crossover_method_var = tk.StringVar()
crossover_method_var.set("single_point")

fields = [
    ("Generations:", entry_gen),
    ("Population Size:", entry_pop),
    ("Mutation Rate (%):", slider_mutation_rate),
    ("Selection Method:", tk.OptionMenu(experiment_frame, selection_method_var, "elitist", "tournament", "roulette", "rank")),
]

for idx, (label_text, widget) in enumerate(fields, 1):
    tk.Label(experiment_frame, text=label_text).grid(row=idx, column=0, sticky="e")
    widget.grid(row=idx, column=1)

# Dynamic fields (above crossover method)
label_num_selected = tk.Label(experiment_frame, text="Number Selected:")
entry_num_selected = tk.Entry(experiment_frame)
label_num_selected.grid(row=5, column=0, sticky="e")
entry_num_selected.grid(row=5, column=1)
label_num_selected.grid_remove()
entry_num_selected.grid_remove()

label_tournament_size = tk.Label(experiment_frame, text="Tournament Size:")
entry_tournament_size = tk.Entry(experiment_frame)
label_tournament_size.grid(row=6, column=0, sticky="e")
entry_tournament_size.grid(row=6, column=1)
label_tournament_size.grid_remove()
entry_tournament_size.grid_remove()

# Crossover method field (after dynamic selection fields)
tk.Label(experiment_frame, text="Crossover Method:").grid(row=7, column=0, sticky="e")
tk.OptionMenu(experiment_frame, crossover_method_var, "single_point", "two_point").grid(row=7, column=1)

selection_method_var.trace("w", update_ui_for_selection_method)

tk.Button(experiment_frame, text="Run Experiment", command=run_experiment).grid(row=8, column=0, columnspan=2, pady=10)
tk.Button(experiment_frame, text="Back", command=show_main_page).grid(row=9, column=0, columnspan=2, pady=5)

result_frame = tk.Frame(root)

text_frame = tk.Frame(result_frame)
text_frame.grid(row=2, column=0, columnspan=2, pady=10)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(text_frame, height=10, width=80, wrap="word", yscrollcommand=scrollbar.set)
text_output.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=text_output.yview)

tk.Button(result_frame, text="Show Colored Graph", command=lambda: plot_graph(last_generated_graph, last_coloring, f"Fitness (not a valid solution if < 1): {last_fitness}")).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(result_frame, text="Back", command=show_main_page).grid(row=4, column=0, columnspan=2, pady=5)

main_frame.pack(pady=50)
root.mainloop()
