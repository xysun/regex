# regex engine in Python
# xiayun.sun@gmail.com
# 06-JUL-2013
# currently supporting: alteration(|), concatenation, repetitions (* ? +), parentheses
#
# TODO: 
#     more rigorous bnf grammar for regex                 DONE
#     add . 
#     better unit tests                                   DONE
#     backreferences? NO
#     convert to DFA
#     draw NFA in debug mode using Graphviz


from parse import Lexer, Parser, Token, State, NFA
import pdb, re, time

state_i = 0

def create_state():
    global state_i # TODO: better than global variable?
    state_i += 1
    return State('s' + str(state_i))

def print_tokens(tokens):
    for t in tokens:
        print(t)

def compile(p, debug = False):
    global state_i
    state_i = 0

    lexer = Lexer(p)
    parser = Parser(lexer)
    tokens = parser.parse()
    
    if debug:
        print_tokens(tokens) 

    nfa_stack = []
    
    for t in tokens:
        if t.name == 'CHAR':  
            s0 = create_state()
            s1 = create_state()
            s0.transitions[t.value] = s1
            nfa = NFA(s0, s1)
            nfa_stack.append(nfa)
        
        elif t.name == 'CONCAT':
            n2 = nfa_stack.pop()
            n1 = nfa_stack.pop()
            n1.end.is_end = False
            n1.end.epsilon.append(n2.start)
            nfa = NFA(n1.start, n2.end)
            nfa_stack.append(nfa)
        
        elif t.name == 'ALT':
            n2 = nfa_stack.pop()
            n1 = nfa_stack.pop()
            s0 = create_state()
            s0.epsilon = [n1.start, n2.start]
            s3 = create_state()
            n1.end.epsilon.append(s3)
            n2.end.epsilon.append(s3)
            n1.end.is_end = False
            n2.end.is_end = False
            nfa = NFA(s0, s3)
            nfa_stack.append(nfa)
        
        elif t.name == 'STAR':
            n1 = nfa_stack.pop()
            s0 = create_state()
            s1 = create_state()
            s0.epsilon = [n1.start, s1]
            n1.end.epsilon.extend([s1, n1.start])
            n1.end.is_end = False
            nfa = NFA(s0, s1)
            nfa_stack.append(nfa)

        elif t.name == 'PLUS':
            n1 = nfa_stack.pop()
            s0 = create_state()
            s1 = create_state()
            n1.end.is_end = False
            s0.epsilon = [n1.start]
            n1.end.epsilon.extend([s1, n1.start])
            nfa = NFA(s0, s1)
            nfa_stack.append(nfa)
        
        elif t.name == 'QMARK':
            n1 = nfa_stack.pop()
            n1.start.epsilon.append(n1.end)
            nfa_stack.append(n1)
    
    assert len(nfa_stack) == 1
    return nfa_stack.pop() 

def main(debug = False):
    nfa = compile('(Ab|cD)*', debug)
    if debug:
        nfa.pretty_print()
    print(nfa.match('Abc'))

def timing(): 
    '''
    comparing re and regex
    '''
    with open('test_suite.dat', 'r') as f:
        text = f.readlines()
    f = open('time.dat', 'w')
    f.write('Python(ms)\tRegex(ms)\n')
    for line in text:
        (pattern, string) = line.split()
        #testing python
        t1 = time.time()
        c = re.compile(pattern)
        c.match(string)
        t_py = 1000 * (time.time() - t1)
        #testing regex
        t2 = time.time()
        nfa = compile(pattern)
        nfa.match(string)
        t_regex = 1000 * (time.time() - t2)

        f.write(str(t_py) + '\t' + str(t_regex) + '\n')
    f.close()

def test_pathological(n):
    p = 'a?' * n + 'a' * n
    nfa_python = re.compile(p)
    nfa_me = compile(p)
    string = 'a' * n
    print("Pattern:", p, "\nInput:", string)
    # test python
    t0 = time.time()
    m = nfa_python.match(string)
    print("Python:", time.time() - t0)
    print("result:", m)
    # test mine
    t0 = time.time()
    m = nfa_me.match(string)
    print("Thompson's Algo:", time.time() - t0)
    print("result:", m)

if __name__ == '__main__':
    main(debug = True)
