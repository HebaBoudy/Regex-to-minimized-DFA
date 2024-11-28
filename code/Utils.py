from graphviz import Digraph 
import os 
import json
def is_alphanumeric(char):
    return char.isalnum() or char == '_' or char == '.' or len(char) > 1

def read_input_file(file_name):
    with open(file_name) as f:
        return f.read().strip()  
    
def write_output_to_file(file_name, content):
   
    output_dir = 'output_files/json_files'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_path = os.path.join(output_dir, file_name)
    json.dump(content.to_dict(),fp=open(file_path, 'w'),indent=4)
    with open(file_path, 'w') as f:
        f.write(str(content))

def rename(dfa) :
    counter = 1 #TODO : LET THIS COUNTER =0 ANA 3MLTO KDA BS 3SHAN BA TEST 
    for state in dfa.states : 
        state.state_name = 'S'+ str(counter) 
        counter += 1
    return dfa 

def validate_input(input:str) : 
    if not input : 
        return False
    # check for the substring () or [] 
    if input.find('()') != -1 or input.find('[]') != -1 : 
        return False
    for i,char in enumerate(input) : 
        if not is_alphanumeric(char) : 
            if char =='-' : 
                if i == 0 or i == len(input)-1 : 
                    return False 
                if not is_alphanumeric( input[i-1]) or not is_alphanumeric( input[i+1]) : 
                    return False   
                if input[i-1] > input[i+1] : 
                    return False
            elif char not in {'+','*','|','(',')',']','[','?','.'}:
                return False  
    stack = []
    for char in input : 
        if char in {'(','['} : 
            stack.append(char)
        elif char in {')',']'} : 
            if not stack : 
                return False 
            if char == ')' and stack[-1] != '(' : 
                return False 
            if char == ']' and stack[-1] != '[' : 
                return False 
            stack.pop() 
   
    return not stack  
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
        # if the node is start and accepting state then double circle and green color border  with blue border 
        if state_name == start_state and is_accepting: 
            dot.node(state_name, shape='doublecircle', color='green', label=state_name)  # Start and accepting state
        
        elif state_name == start_state:
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
    output_folder = 'output_files/graphs'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dot.render(filename= filename, directory= output_folder, view = True ,cleanup = True, format='png')   
   
