from graphviz import Digraph 
import os
def visualize(nfa_json , filename : str):
    # Create a new directed graph
    dot = Digraph(format='png')
    
    # Set global graph attributes for visual clarity
    dot.attr(rankdir='LR')  # Left to right layout

    # Add states to the graph
    start_state = nfa_json.get("startingState")
    print("inside visualize :",start_state)
    for state_name, state_info in nfa_json.items():
        if state_name == "startingState":
            continue

        # Determine if this state is an accepting state
        is_accepting = state_info["isTerminatingState"]

        # Customize node style based on state type
        if state_name == start_state:
            dot.node(state_name, shape='circle', color='green', label=state_name)  # Start state
        elif is_accepting:
            dot.node(state_name, shape='doublecircle', color='blue', label=state_name)  # Accepting state
        else:
            dot.node(state_name, shape='circle', label=state_name)

    # Add transitions
    for state_name, state_info in nfa_json.items():
        if state_name == "startingState":
            continue

        # Iterate over transitions and add them as edges
        for input_symbol, destinations in state_info.items():
            if input_symbol == "isTerminatingState":
                continue
            
            if isinstance(destinations, list):
                # If there are multiple destinations, create separate edges for each
                for destination in destinations:
                    label = "ε" if input_symbol == "~" else input_symbol  # Represent epsilon with 'ε'
                    dot.edge(state_name, destination, label=label)
            else:
                # Single destination, normal case
                label = "ε" if input_symbol == "~" else input_symbol  # Represent epsilon with 'ε'
                dot.edge(state_name, destinations, label=label)

# Ensure the output folder exists
    output_folder = 'output_files'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Specify the filepath to save the graph
    path = os.path.join(output_folder, filename)
    dot.render(path, view=True)