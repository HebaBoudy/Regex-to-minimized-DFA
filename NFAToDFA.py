from CustomDataTypes import * 
# from Visualize import visualize_nfa
def epsilonClosure(state : State) -> Set[State] :
    states : Set[State] = {state} 
    transition : Transition 

   
    for transition in state.transitions : 
        if transition.input == '~':
            states.add(transition.destination)
            states.update(epsilonClosure(transition.destination))

    return states 
def rename(dfa) :
    counter = 1 #TODO : LET THIS COUNTER =0 ANA 3MLTO KDA BS 3SHAN BA TEST 
    for state in dfa.states : 
        state.state_name = 'S'+ str(counter) 
        counter += 1
    return dfa

def subsetConstruction(nfa : NFA) -> DFA :
    
    dfa = DFA()
    start_dfa_state = DFAState(epsilonClosure(nfa.start_state)  ) 
    dfa.add_state(start_dfa_state , is_start = True)
    work_list = [start_dfa_state] 
    while (work_list):
        transition : Transition
        transitions_dict: Dict[str, List[State]] = {} 
        current_dfa_state = work_list.pop() 
        #  if current_dfa_state in processed_states:
        #     continue
        # processed_states.add(current_dfa_state)


        for state in current_dfa_state.nfa_states :
            for transition in state.transitions : 
                if transition.input != '~':
                    if transition.input not in transitions_dict.keys() :
                        transitions_dict[transition.input] = [transition.destination]
                    else : 
                        transitions_dict[transition.input].append(transition.destination)
       
       # print("dictionary of transitions :",transitions_dict)
        for key , value in transitions_dict.items() : 
            epsilon_closures : Set[State] = set()

            for nfa_state in value : 
                epsilon_closures.update(epsilonClosure(nfa_state))

            existing_dfa_state = dfa.find_DFA_state_by_NFA_states(epsilon_closures)
            if existing_dfa_state is None:
                new_dfa_state = DFAState(epsilon_closures)
                dfa.add_state(new_dfa_state)
                work_list.append(new_dfa_state)
            else:
                new_dfa_state = existing_dfa_state

            current_dfa_state.add_transition(key, new_dfa_state) 
            rename(dfa)
    return dfa 
# dfa = subsetConstruction(nfa) 
#print (dfa)


# print("hello",(dfa.states[0].transitions))
# print("**************")
