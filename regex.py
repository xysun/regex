# regex engine in Python
# xiayun.sun@gmail.com
# 06-JUL-2013
# currently supporting: alteration(|), concatenation, star(*) operator
# TODO: 
#more rigorous bnf grammar for regex

from classes import Lexer, Parser, Token, State, NFA
import pdb


def test(p):
    lexer = Lexer(p)
    parser = Parser(lexer)
    tokens = parser.prog()
    for t in tokens:
        print(t)

s0 = State('s0')
s1 = State('s1')
s2 = State('s2')
s3 = State('s3')

s0.epsilon = [s1, s3]
s1.transitions = {'a':s2}
s2.epsilon = [s1, s3]

nfa = NFA(s0, s3) # sample NFA: a*

state_i = 0

def create_state():
    global state_i # TODO: better than global variable?
    state_i += 1
    return State('s' + str(state_i))

def compile(p):
    lexer = Lexer(p)
    parser = Parser(lexer)
    tokens = parser.prog()

    nfa_stack = []
    for t in tokens:
        
        if t.name == 'CHAR': # push onto stack 
            s0 = create_state()
            s1 = create_state()
            s0.transitions[t.value] = [s1]
            nfa = NFA(s0, s1)
            nfa_stack.append(nfa)
        
        elif t.name == 'CONCAT':
            n2 = nfa_stack.pop()
            n1 = nfa_stack.pop()
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
            nfa = NFA(s0, s3)
            nfa_stack.append(nfa)
        
        elif t.name == 'STAR':
            n1 = nfa_stack.pop()
            s0 = create_state()
            s1 = create_state()
            s0.epsilon = [n1.start, s1]
            n1.end.epsilon.append(n1.start)
            n1.end.epsilon.append(s1)
            nfa = NFA(s0, s1)
            nfa_stack.append(nfa)

    return nfa_stack.pop() # TODO: check len(nfa_stack) == 1?


def main():
    global status_i
    status_i = 0

    nfa = compile('bc|ac*')
    print(nfa.match('ac'))
    print(nfa.match('accc'))
    print(nfa.match('bc'))
    print(nfa.match('bac'))

if __name__ == '__main__':
    main()
