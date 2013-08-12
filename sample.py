# regex engine in Python
# sample program: timing scripts
# xiayun.sun@gmail.com
# 06-JUL-2013

import regex
import re, time

def test(debug = False):
    nfa = regex.compile('ab?', debug)
    if debug:
        nfa.pretty_print()
    print(nfa.match('ab'))

def timing_normal(): 
    '''
    comparing re and regex on normal inputs
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
    nfa_me = regex.compile(p)
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
