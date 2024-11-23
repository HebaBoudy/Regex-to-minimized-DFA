'''
Postfix notation removes the need for parentheses and allows computer programs to read in 
mathematical expressions one symbol after the other, instead of worrying about operator precedence 
and parentheses during computation. 

'''
def shuntingYard(input) :
    precedence_dict = {'*': 3, '?': 2, '|': 1}
    out =[]
    operator_stack = []
    for char in input :
        # If the input is alphanumeric then append to the output regex 
        if char.isalnum() or char == '.' or len(char) > 1 :
            out.append(char)
        # If the input is an operator
        elif  char in precedence_dict.keys() :
            # The first operator in the stack 
            if len(operator_stack) == 0:
                operator_stack.append(char) 
            #  Any operator shouldn't be compared to an opening parenthes , if an opening parenthes is on the top of the stack Just add the char to the stack directly 
            elif operator_stack[-1] =='('or precedence_dict[ operator_stack[-1] ] < precedence_dict[char] :
                operator_stack.append(char)
            # If the operator on the top of the stack is the same as the current char then pop one to the output regex and leave the other in tha stack 
            # If two consecutive opening parenthes comes we need them both to be in the stack and not popped to the output because they will be deleted later 
            elif operator_stack[-1] != '(' and precedence_dict[ operator_stack[-1] ] == precedence_dict[char] : 
                out.append(char) 
            #If the operator at the top of the stack has higher precedence that the current operator then pop to the output until we can push the current operator to the stack 
            else : 
                while (len(operator_stack)>0 and operator_stack[-1] != '('and precedence_dict[ operator_stack[-1] ]  >= precedence_dict[char]) :
                    popped_operator = operator_stack.pop()
                    out.append(popped_operator)
                operator_stack.append(char) 
        elif char == '(' :
            operator_stack.append(char)
        # The current char is closing parenthes -> pop from the operator stack to the output until you reach an opening parenthes
        elif char == ')' :
            while operator_stack:
                operator = operator_stack.pop()
                if operator == '(':
                    break
                out.append(operator)
        # print ("parsing char :",char,"output:",out,"stack",operator_stack)
        # print("************************")
    out.extend(operator_stack[::-1]) 
    # print ("Final out :",out)
    return out 