import re 


def validate_input(input:str) : 
    # check for the substring () or [] 
    if input.find('()') != -1 or input.find('[]') != -1 : 
        return False
    for i,char in enumerate(input) : 
        if not char.isalnum() : 
            if char =='-' : 
                if i == 0 or i == len(input)-1 : 
                    return False 
                if not input[i-1].isalnum() or not input[i+1].isalnum() : 
                    return False   
                if input[i-1] > input[i+1] : 
                    return False
            if char not in {'+','*','|','(',')',']','[','?','.'}:
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

'''
This preporcessing is applied to the regex before applying shunting yard algorithm in order to : 
1) reduce all the regex to these operations only ( * , | , parenthes , concat wich is represented by ?)
2) add a concatination symbol between characters to be recognized by the algorithm as an operator 
3) replace every [match] with one char to be treated as other alphanumeric 
'''  
def preprocessing(input : str) :
# input= 'a?a((cd)|(a|b))b+bb' 
    #Step1: Replace zero or one symbol '?'
    step_1 = re.sub(r'(\w)\?', r'(\1|~)', input)
    #Step2: Replace one or more symbol '+'
    step_2 = re.sub(r'(\w)\+', r'\1\1*', step_1)
    #Step3: Add concat symbol before every [ or (  if they are not at the start of the regex and they are not preceded by ?
    pattern_before = re.compile(r'''
        (?<!^)      # Negative lookbehind assertion to ensure the position is not at the start of the string
        (?<!\?)     # Negative lookbehind assertion to ensure the position is not preceded by '?'
        (?=[\[\(])  # Positive lookahead assertion to match '[' or '(' without consuming them
    ''', re.VERBOSE)
    step_3 = pattern_before.sub('?', step_2) 
    #Step 4: Add concat symbol after every ] or ) if they are not the end of regex OR they are not followed by * and not followed by ? 
    pattern_after = re.compile(r'''
        (?<=[\]\)])  # Positive lookbehind assertion to match ']' or ')' without consuming them
        (?!$)        # Negative lookahead assertion to ensure the position is not at the end of the string
        (?![\*\?])   # Negative lookahead assertion to ensure the position is not followed by '*' or '?'
    ''', re.VERBOSE)
    step_4 = pattern_after.sub('?', step_3)
    #Step 5 : Add concat after every * if its not the end of regex and its not follwed by star 
    pattern_star = re.compile(r'''
        \*          # Match the '*' character
        (?!$)       # Negative lookahead assertion to ensure the position is not at the end of the string
        (?![\?])    # Negative lookahead assertion to ensure the position is not followed by '?'                      
    ''', re.VERBOSE)
    step_5 = pattern_star.sub('*?', step_4)
    #Step 6 : Add concat after every alphanum or dot if its followed by alphanumeric or dot 
    pattern_alnum_dot = re.compile(r'''
        ([a-zA-Z0-9\.])  # Match any alphanumeric character or dot
        (?=[a-zA-Z0-9\.])  # Positive lookahead assertion to ensure it is followed by another alphanumeric character or dot
    ''', re.VERBOSE)
    step_6 = pattern_alnum_dot.sub(r'\1?', step_5)
    return split_input(step_6) 

''' 
this function does the same as preprocessing but without using re library 
'''
def preprocessing_v2(input : str) :
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
