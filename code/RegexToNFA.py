from CustomDataTypes import *
from ShuntingYard import *
from Utils import is_alphanumeric
'''
Finally : Thomsons construction Algorithm 
'''

def create_nfa_initial_states() : 
    start_state = State()
    end_state = State()
    end_state.isTerminatingState = True 
    return start_state , end_state
    
def alphanumeric_nfa(char) : 
    start_state , end_state = create_nfa_initial_states()
    start_state.add_transition(end_state , char)
    nfa = NFA() 
    nfa.add_states([start_state , end_state])
    return nfa 

def zero_or_more_nfa(operand: NFA) : 
    new_start_state , new_end_state = create_nfa_initial_states()
    new_start_state.add_transition(operand.start_state , '~')
    new_start_state.add_transition(new_end_state ,'~')
    operand.accept_states[0].add_transition(operand.start_state ,'~')
    operand.accept_states[0].add_transition(new_end_state,'~')
    nfa = NFA ()
    nfa.add_states([new_start_state , operand.states , new_end_state])
    return nfa

def union_nfa(operand1: NFA , operand2: NFA) :
    new_start_state , new_end_state = create_nfa_initial_states()
    new_start_state.add_transition(operand1.start_state , '~')
    new_start_state.add_transition(operand2.start_state , '~')
    operand1.accept_states[0].add_transition(new_end_state , '~')
    operand2.accept_states[0].add_transition(new_end_state , '~')
    nfa = NFA()
    nfa.add_states([new_start_state , operand1.states , operand2.states , new_end_state])
    return nfa

def concatinate_nfa(operand1: NFA , operand2: NFA) :
    operand1.accept_states[0].add_transition(operand2.start_state , '~')
    nfa = NFA()
    nfa.add_states([operand1.states , operand2.states])
    return nfa

def constructNFA(input ) : 
    stack_NFA = []
    for char in input : 
        if is_alphanumeric(char) or char == '~' : 
            stack_NFA.append(alphanumeric_nfa(char))  
        elif char == '*':
            stack_NFA.append(zero_or_more_nfa(stack_NFA.pop()))
        elif char == '|': 
            operand2 = stack_NFA.pop() 
            operand1 = stack_NFA.pop()
            stack_NFA.append(union_nfa(operand1, operand2))
        elif char == '?' :
            operand2 = stack_NFA.pop() 
            operand1 = stack_NFA.pop()
            stack_NFA.append(concatinate_nfa(operand1, operand2))

    return stack_NFA[0] 

def ThomsonsConstruction (input : str) -> NFA : 
    shunting_yard = shuntingYard(input) 
    print("Shunting Yard : ",shunting_yard)
    nfa = constructNFA(shunting_yard) 
    return nfa

   