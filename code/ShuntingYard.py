
def split_input(input: str):
    split_list = []
    opening_match_found = False 
    match = ""
    for char in input: 
        if char == '[' :
            opening_match_found = True 
        elif char == ']': 
            opening_match_found = False 
            split_list.append('['+ match +']')
            match = "" 
        elif  opening_match_found == 0 :
            split_list.append (char) 
        else : 
            match =  match + char 
    return split_list 


def preprocessing(input : str) :
    # Step 1 : Replace zero or one symbol '?'
    step_1 = ""
    for i,char in enumerate(input) :
        if i != 0 and char == '?' :
            # pop the last caracter and add ( last_char | ~) 
            step_1 = step_1[:-1] + '(' + step_1[-1] + '|~)'
        else : 
            step_1 += char
    # Step 2 : Replace one or more symbol '+'
    step_2 = ""
    for i,char in enumerate(step_1) : 
        if i != 0 and char == '+' :
            step_2 += step_1[i-1] + '*' 
        else : 
            step_2 += char 
    # Step 3 : Add concat symbol before every [ or (  if they are not at the start of the regex and they are not preceded by ?  and they are not followed by nested brackets (( )) there should not be concat inside 
    
    step_3 = ""
    for i,char in enumerate(step_2) : 
        if i != 0 and step_2[i-1] != '?' and  step_2[i-1] != '|' and ((char == '[' and step_2[i-1] != '[')or (char == '(' and step_2[i-1] != '(')) : 
            step_3 += '?'+char
        else : 
            step_3 += char 
    # Step 4 : Add concat symbol after every ] or ) if they are not the end of regex OR they are not followed by * and not followed by ?and they are not followed by nested brackets (( )) there should not be concat inside 
    step_4 = ""
    for i,char in enumerate(step_3) : 
        if i != len(step_3)-1 and step_3[i+1] != '*' and step_3[i+1] != '|' and step_3[i+1] != '?' and ((char == ']' and step_3[i+1]!= ']') or (char == ')' and step_3[i+1]!= ')')) : 
            step_4 += char + '?'
        else : 
            step_4 += char 
    # Step 5 : Add concat after every * if its not the end of regex and its not follwed by star
    step_5 = ""
    for i,char in enumerate(step_4) : 
        if i != len(step_4)-1 and step_4[i+1] != '?' and char == '*' : 
            step_5 += char + '?'
        else : 
            step_5 += char 
        # Step 6: Add concat after every alphanum or dot if it's followed by alphanumeric or dot,
    # but skip concatenation for characters inside square brackets
    step_6 = ""
    inside_square_brackets = False

    for i, char in enumerate(step_5):
        if char == '[':
            inside_square_brackets = True  # Start of square brackets
            step_6 += char
        elif char == ']':
            inside_square_brackets = False  # End of square brackets
            step_6 += char
        elif (
            not inside_square_brackets  # Ensure we are not inside square brackets
            and i != len(step_5) - 1
            and (char.isalnum() or char == '.')
            and (step_5[i + 1].isalnum() or step_5[i + 1] == '.')
        ):
            step_6 += char + '?'  # Add concat symbol
        else:
            step_6 += char
    return (split_input(step_6))
'''
Postfix notation removes the need for parentheses and allows computer programs to read in 
mathematical expressions one symbol after the other, instead of worrying about operator precedence 
and parentheses during computation. 

'''
def shuntingYard(input) :
    input = preprocessing(input)
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