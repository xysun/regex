# regex engine in Python
# xiayun.sun@gmail.com
# 06-JUL-2013
# currently supporting: alteration(|), concatenation, star(*) operator
# TODO: 
#more rigorous bnf grammar for regex

import pdb

class Token:
    precedence_table = {'ALT':0, 'CONCAT':1, 'PLUS': 2, 'STAR': 2, 'QMARK':2, 'LEFT_PAREN':-1, 'RIGHT_PAREN':-1, 'CHAR': -1} # -1 should never be used
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.precedence = Token.precedence_table[name]

    def __str__(self):
        return self.name + ":" + self.value

def re2postfix(pattern): # transform to postfix
    symbols = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'ALT', '\x08':'CONCAT', '+':'PLUS', '?':'QMARK'}
    operators = []
    tokens = [] 
    
    l = len(pattern)
    i = 0
    
    def handle_char(c, i):
        if c in symbols.keys(): # operator
            t = Token(symbols[c], c)
            if c == '(':
                operators.append(t)
            elif c == ')':
                t2 = operators.pop()
                while t2.name != 'LEFT_PAREN':
                    tokens.append(t2)
                    t2 = operators.pop()
            elif c == '*' or c == '+' or c == '?':
                tokens.append(t)
            else:
                while len(operators) > 0 and operators[-1].precedence >= t.precedence:
                    tokens.append(operators.pop())
                operators.append(t)

        else: # char
            t = Token('CHAR', c)
            tokens.append(t)
            if i + 1 < l:
                c1 = pattern[i+1]
                if not c1 in symbols.keys(): # two chars together
                    handle_char('\x08', -1)

            else: # last char
                handle_char('\x08', -1)
                
    while i < l:
        c = pattern[i]
        handle_char(c, i)
        i += 1
    
    while len(operators) > 0:
        tokens.append(operators.pop())

    return tokens



class Lexer:
    def __init__(self, pattern):
        self.source = pattern
        self.symbols = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'ALT', '\x08':'CONCAT', '+':'PLUS', '?':'QMARK'}
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
                elif not self.lexer.eof and self.lookahead.name == 'PLUS':
                    self.step_back()
                    self.star()
                elif not self.lexer.eof and self.lookahead.name == 'QMARK':
                    self.step_back()
                    self.star()
                else:
                    self.tokens.append(t)
                self.tokens.append(Token('CONCAT', '\x08'))
            else:
                break

    def star(self): # STAR | PLUS
        self.char()
        while True:
            if not self.lexer.eof and self.lookahead.name == 'STAR':
                t = self.lookahead 
                self.match('STAR')
                self.tokens.append(t)
            elif not self.lexer.eof and self.lookahead.name == 'PLUS':
                t = self.lookahead
                self.match('PLUS')
                self.tokens.append(t)
            elif not self.lexer.eof and self.lookahead.name == 'QMARK':
                t = self.lookahead
                self.match('QMARK')
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
