# regex engine in Python
# main program
# xiayun.sun@gmail.com
# 06-JUL-2013
# Supporting: alteration(|), concatenation, repetitions (* ? +), parentheses
#
# TODO: 
#     more rigorous bnf grammar for regex                 DONE
#     add . 
#     better unit tests                                   DONE
#     backreferences?                                     NO
#     convert to DFA
#     draw NFA in debug mode using Graphviz
#     return positions of match


from parse import Lexer, Parser, Token, State, NFA, Handler
import pdb, re, time

def print_tokens(tokens):
    for t in tokens:
        print(t)

def compile(p, debug = False):
    lexer = Lexer(p)
    parser = Parser(lexer)
    tokens = parser.parse()

    handler = Handler()
    
    if debug:
        print_tokens(tokens) 

    nfa_stack = []
    
    for t in tokens:
        handler.handlers[t.name](t, nfa_stack)
    
    assert len(nfa_stack) == 1
    return nfa_stack.pop() 

def test(debug = False):
    nfa = compile('(Ab|cD)*', debug)
    if debug:
        nfa.pretty_print()
    print(nfa.match('Abc'))

def timing_normal(): 
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
    t0 = time.time()
    m = nfa_python.match(string)
    t_py = time.time() - t0
    t0 = time.time()
    m = nfa_me.match(string)
    t_regex = time.time() - t0
    return t_py, t_regex

def timing_pathological():
    MAX = 26
    f = open('time_pathological.dat', 'w')
    f.write('n\tPython\tRegex\n')
    for i in range(1, MAX):
        t_py, t_regex = test_pathological(i)
        f.write(str(i) + '\t' + str(t_py) + '\t' + str(t_regex) + '\n')
    f.close()

if __name__ == '__main__':
    test(debug = True)
