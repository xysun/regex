# regex engine in Python
# xiayun.sun@gmail.com
# 06-JUL-2013
# currently supporting: alteration(|), concatenation, star(*) operator
# TODO: 
#more rigorous bnf grammar for regex

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
        self.symbols = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'ALT', '\x08':'CONCAT'}
        self.current = 0
        self.length = len(self.source)
        self.eof = False
       
    def get_token(self):
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

class ParseError(Exception):pass

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = self.lexer.get_token()
        self.tokens = []

    def match(self, name):
        if not self.lexer.eof and self.lookahead.name == name:
            self.lookahead = self.lexer.get_token()
        else:
            raise ParseError
    
    def step_back(self):
        self.lexer.current -= 2
        self.lookahead = self.lexer.get_token()

    def prog(self):
        self.alt()
        return self.tokens
    
    def alt(self):
        self.concat()
        while True:
            if not self.lexer.eof and self.lookahead.name == 'ALT':
                t = self.lookahead
                self.match('ALT')
                self.concat()
                self.tokens.append(t)
            else:
                break
        
    def concat(self):
        self.star()
        while True: #TODO: LL(2)?
            if not self.lexer.eof and self.lookahead.name == 'CHAR':
                t = self.lookahead
                self.match('CHAR')
                if not self.lexer.eof and self.lookahead.name == 'STAR':
                    self.step_back()
                    self.star()
                else:
                    self.tokens.append(t)
                self.tokens.append(Token('CONCAT', '\x08'))
            else:
                break

    def star(self):
        self.char()
        while True:
            if not self.lexer.eof and self.lookahead.name == 'STAR':
                t = self.lookahead 
                self.match('STAR')
                self.tokens.append(t)
            else:
                break

    def char(self):
        if not self.lexer.eof and self.lookahead.name == 'CHAR':
            self.tokens.append(self.lookahead)
        self.match('CHAR')

class State:
    def __init__(self, name):
        self.epsilon = [] # eps-closure
        self.transitions = {} # char : list of state
        self.name = name
        self.in_current_states = False
    
    def clean(self): # set in_current_states to False for all related states
        self.in_current_states = False
        for s in self.epsilon:
            s.clean()
        for c in self.transitions.keys():
            self.transitions[c].clean()

class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end # start and end states
    
    def clone(self, state, current_states):
        if len(state.epsilon) == 0:
            return current_states
        else:
            for eps in state.epsilon:
                if not eps.in_current_states:   
                    current_states.append(eps)
                    eps.in_current_states = True
                    self.clone(eps, current_states)
            return current_states

    
    def match(self,s):
        current_states = [self.start] 
        current_states = self.clone(self.start, current_states)
        for c in s:
            next_states = []
            for state in current_states:
                if c in state.transitions.keys():
                    s = state.transitions[c]
                    if not s.in_current_states:
                        next_states.append(s)
                        s.in_current_states = True
                        next_states = self.clone(s, next_states)
            # clean up
            for s in current_states:
                s.in_current_states = False
            for s in next_states:
                s.in_current_states = False

            current_states = next_states

        for s in current_states:
            if s == self.end:
                return True
        return False
