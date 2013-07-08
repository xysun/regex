A regex engine in Python following Thompson's Algorithm. This will perform significantly better than the backtracking approach implemented in Python's `re` module over some pathological patterns. 

It has the same interface as Python's `re` module:

```python
import regex
n = 20
p = 'a?' * n + 'a' * n
nfa = regex.compile(p)
input_string = 'a' * n
matched = nfa.match(input_string)
print(matched) # True
```
