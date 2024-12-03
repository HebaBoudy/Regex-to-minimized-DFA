from CustomDataTypes import * 
def get_group_index(state: DFAState, groups: List[Set[DFAState]]) -> int:
        for i, group in enumerate(groups):
            if state in group:
                return i
            
def create_transition_dict(subgroup: Set[DFAState],  groups: List[Set[DFAState]]) -> Dict[Tuple[int, ...], Set[DFAState]]:

    transition_dict: Dict[Tuple[int, ...], Set[DFAState]] = {}
    input_symbols = list(subgroup)[0].get_transitions_inputs() 
    ''' 
    s1,s2,s3 
    (1,2,3) -> {s1,s2}
    '''
    
    for state in subgroup :
        transition_key_elements = []
        for input_symbol in input_symbols:
            destination_state = state.transitions[input_symbol]
            # Get the index of the group to which the destination state belongs
            group_index = get_group_index(destination_state, groups)
            transition_key_elements.append(group_index)
            transition_key = tuple(transition_key_elements)
        # Group states by their transition pattern
        if transition_key in transition_dict:
            transition_dict[transition_key].add(state)
        else:
            transition_dict[transition_key] = {state}
    return transition_dict

def partition_groups_based_on_transitions(groups : List[Set[DFAState]]) -> List[Set[DFAState]]:
    new_groups : List[Set[DFAState]] =  [] 
    print("total groups before partinioning :" ,len(groups))
    for i, group in enumerate(groups) : 
        transitions_dict: Dict[Tuple[str, ...], Set[str]] = {}
        for state in group:
            ''' 
            s1 (a,b)
            s2 (a,b,c)
            s3 (c)

            (a,b) -> [s1,s4]
            
            '''
            transitions = state.get_transitions_inputs()
            if transitions in transitions_dict:
                transitions_dict[transitions].add(state)
            else:
                transitions_dict[transitions] = {state}
       
        for value in transitions_dict.values() :
            new_groups.append(value) 
    return new_groups
def convertGroupsToDFA(groups : List[Set[DFAState]], start_state_group_index) -> DFA :
    dfa=DFA() 
    #dfa.start_state = 
    for i, group in enumerate(groups) :
        state = list(group)[0] 
        if i == start_state_group_index:
            dfa.start_state = state
        if state not in dfa.states:
            dfa.add_state(state)

        for input, dest in state.transitions.items():
            dest_group = get_group_index(dest,groups)
            dest_state = list(groups[dest_group])[0] 
            state.transitions[input] = dest_state
            if dest_state not in dfa.states:
                dfa.add_state(dest_state)
    return dfa

def minimizeDFA(dfa : DFA) -> DFA: 
    # PASS 1 
    accepting_states : Set[DFAState] = set()
    none_accepting_states : Set[DFAState] = set()
    for state in dfa.states : 
        if state.isTerminatingState : 
            accepting_states.add(state)
        else :
            none_accepting_states.add(state)
    
    groups : List[Set[DFAState]] = [accepting_states ,  none_accepting_states] 
    groups = partition_groups_based_on_transitions(groups)
    # PASS TWO : 
    while True:           
        new_groups: List[Set[DFAState]] = []
        for i, group in enumerate(groups): 
            if(len(group) == 1):
                new_groups.append(group)
                continue 
            if(list(group)[0].get_transitions_inputs() == ()): # no transitions
                new_groups.append(group)
                continue
            transition_dict = create_transition_dict(group, groups)
            for  states in transition_dict.values():
                new_groups.append(states)
        if new_groups == groups:
            print("Groups have stabilized, exiting.")
            break
        groups = new_groups
    print("dfa start state",dfa.start_state)
    start_state = dfa.start_state
    start_state_group_index = get_group_index(start_state, groups)
    new_dfa=convertGroupsToDFA(groups,start_state_group_index) 
    return new_dfa
#print (minimizeDFA(dfa))
# print(len(minimizeDFA(dfa)))
# visualize_nfa(renameDFA(minimizeDFA(dfa)).to_dict())
# visualize_nfa(dfa.to_dict())
