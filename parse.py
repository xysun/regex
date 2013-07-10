# regex engine in Python
# parse and classes
# xiayun.sun@gmail.com
# 06-JUL-2013
# currently supporting: alternation (|), concatenation, star (*), question mark (?), plus (+), and parenthesis

import pdb

class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value

class Lexer:
    def __init__(self, pattern):
        self.source = pattern
        self.symbols = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'ALT', '\x08':'CONCAT', '+':'PLUS', '?':'QMARK'}
        self.current = 0
        self.length = len(self.source)
        self.eof = False
       
    def get_token(self): # TODO: always return one None in the end
        if self.current < self.length:
            c = self.source[self.current]
            self.current += 1
            if c not in self.symbols.keys(): # CHAR
                token = Token('CHAR', c)
            else:
                token = Token(self.symbols[c], c)
            return token
        else:
            self.eof = True
            return Token('NONE', '')

class ParseError(Exception):pass

'''
Grammar for regex:

regex = exp $

exp      = term [|] exp      {push '|'}
         | term
         |                   empty?

term     = factor term       chain {add \x08}
         | factor

factor   = primary [*]       star {push '*'}
         | primary [+]       plus {push '+'}
         | primary [?]       optional {push '?'}
         | primary

primary  = \( exp \)
         | char              literal {push char}
'''

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.lookahead = self.lexer.get_token()
    
    def consume(self, name):
        if self.lookahead.name == name:
            self.lookahead = self.lexer.get_token()
        elif self.lookahead.name != name:
            raise ParseError

    def parse(self):
        self.exp()
        return self.tokens
    
    def exp(self):
        self.term()
        if self.lookahead.name == 'ALT':
            t = self.lookahead
            self.consume('ALT')
            self.exp()
            self.tokens.append(t)

    def term(self):
        self.factor()
        if self.lookahead.value not in ')|':
            self.term()
            self.tokens.append(Token('CONCAT', '\x08'))
    
    def factor(self):
        self.primary()
        if self.lookahead.name in ['STAR', 'PLUS', 'QMARK']:
            self.tokens.append(self.lookahead)
            self.consume(self.lookahead.name)

    def primary(self):
        if self.lookahead.name == 'LEFT_PAREN':
            self.consume('LEFT_PAREN')
            self.exp()
            self.consume('RIGHT_PAREN')
        elif self.lookahead.name == 'CHAR':
            self.tokens.append(self.lookahead)
            self.consume('CHAR')

class State:
    def __init__(self, name):
        self.epsilon = [] # eps-closure
        self.transitions = {} # char : list of states
        self.name = name
        self.in_current_states = False
        self.is_end = False
    
class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end # start and end states
        end.is_end = True
    
    def addstate(self, state, state_list): # add state + epsilon transitions
        if state.in_current_states:
            return
        state_list.append(state)
        state.in_current_states = True
        for eps in state.epsilon:
            self.addstate(eps, state_list)
    
    def pretty_print(self):
        '''
        print using Graphviz
        '''
        pass
    
    def match(self,s):
        current_states = []
        self.addstate(self.start, current_states)
        
        # clean is_current_states flag 
        for state in current_states:
            state.in_current_states = False
        
        for c in s:
            next_states = []
            for state in current_states:
                if c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    self.addstate(trans_state, next_states)
            # clean up
            for state in current_states:
                state.in_current_states = False
            for state in next_states:
                state.in_current_states = False
            
            current_states = next_states

        for s in current_states:
            if s.is_end:
                return True
        return False
