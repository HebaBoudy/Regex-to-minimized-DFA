from Utils import *
from RegexToNFA import ThomsonsConstruction 
from NFAToDFA import subsetConstruction 
from MinimizeDFA import minimizeDFA


regex = read_input_file("../input.txt") 
if not validate_input(regex):
    print("Invalid regex")
else :
    print(regex)
    nfa = ThomsonsConstruction(regex) 
    rename(nfa)
    write_output_to_file('nfa.json', nfa)
    visualize(nfa.to_dict(),'nfa')


    dfa = subsetConstruction(nfa) 
    rename(dfa)
    write_output_to_file('dfa.json', dfa)
    visualize(dfa.to_dict(),'dfa')

    
    minimized_dfa = minimizeDFA(dfa)
    rename(minimized_dfa)
    write_output_to_file('minimized_dfa.json', minimized_dfa)
    visualize(minimized_dfa.to_dict(),'minimized_dfa')

