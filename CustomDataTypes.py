from typing import List , Union , Dict , Set ,Tuple, Optional
import json 
'''
Datastructures defined
 
'''
class Transition:
    def __init__(self, destination , input):
        self.destination = destination
        self.input = input
    def __repr__(self) -> str:
        return f"Transition(destination={self.destination.state_name}, input='{self.input}')"


class State: 
    state_counter = 0  

    def __init__(self):
        self.state_name = 'S'+ str(State.state_counter) 
        State.state_counter += 1
        self.transitions = [] 
        self.isTerminatingState = False 

    def add_transition(self, destination, input):
        self.transitions.append(Transition(destination, input))

    def findTransitionByInput(self , input : str) :
        transition : Transition 
        for transition in self.transitions : 
            if transition.input == input :
                return True , transition.destination 
        return None ,None 

    def to_dict(self):
        state_dict = {
            "isTerminatingState": self.isTerminatingState
        }
        for transition in self.transitions:
            if transition.input in state_dict:
                # If key already exists, append to the list of destinations
                if isinstance(state_dict[transition.input], list):
                    state_dict[transition.input].append(transition.destination.state_name)
                else:
                    # If it's not already a list, make it a list
                    state_dict[transition.input] = [state_dict[transition.input], transition.destination.state_name]
            else:
                # If key doesn't exist, add it
                state_dict[transition.input] = transition.destination.state_name
        return state_dict

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)
    
class NFA:
    def __init__(self):
        self.states = []
        self.start_state:State = None 
        #TODO : is this list or one element 
        self.accept_states : List [State] = []

    def add_states(self, states: Union[List[State], List[List[State]]]):
        # Flatten the list of lists if necessary
        def flatten(states_list: List[Union[State, List[State]]]) -> List[State]:
            flat_list = []
            for state in states_list:
                if isinstance(state, list):
                    flat_list.extend(flatten(state))
                else:
                    flat_list.append(state)
            return flat_list

        states = flatten(states)
        # Ensure every state.isTerminatingState = False
        for state in states:
            state.isTerminatingState = False
        
        self.states.extend(states)
        if not self.start_state and states:
            self.start_state = states[0]
        if states:
            self.accept_states.append(states[-1])
            states[-1].isTerminatingState = True

        
    def add_state(self, state , is_start = False , is_accept = False  ):
        self.states.append(state)
        if is_start:
            self.start_state = state
        if is_accept:
            self.accept_states.append(state)
        return state
    
    def to_dict(self):
        nfa_dict = {
            "startingState": self.start_state.state_name if self.start_state else None
        }
        for state in self.states:
            nfa_dict[state.state_name] = state.to_dict()
        return nfa_dict

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2) 


'''
NFA to DFA 

'''
class DFAState:
    def __init__(self, nfa_states: Set[State]):
        self.nfa_states = nfa_states
        self.transitions: Dict[str, 'DFAState'] = {}
        self.isTerminatingState = any(state.isTerminatingState for state in nfa_states)
        self.state_name = ','.join(sorted(state.state_name for state in nfa_states))

    def add_transition(self, input: str, destination: 'DFAState'):
        self.transitions[input] = destination
    
    def get_transitions_inputs(self) :
        return tuple(sorted(self.transitions.keys()))
    
    def to_dict(self):
        state_dict = {
            "isTerminatingState": self.isTerminatingState
        }
        for input, destination in self.transitions.items():
            state_dict[input] = destination.state_name
        return state_dict

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)
    
class DFA:
    def __init__(self):
        self.states: List[DFAState] = []
        self.start_state: DFAState = None

    def add_state(self, state: DFAState, is_start=False):
        self.states.append(state)
        if is_start:
            self.start_state = state
    def find_DFA_state_by_NFA_states(self, nfa_states: Set[State]) -> Optional[DFAState]:
        for dfa_state in self.states:
            if dfa_state.nfa_states == nfa_states:
                return dfa_state
        return None
    def to_dict(self):
        dfa_dict = {
            "startingState": self.start_state.state_name if self.start_state else None
        }
        for state in self.states:
            dfa_dict[state.state_name] = state.to_dict()
        return dfa_dict

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)
