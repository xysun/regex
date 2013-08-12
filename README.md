A regex engine in Python following Thompson's Algorithm. This will perform significantly better than the backtracking approach implemented in Python's `re` module on some pathological patterns. 

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

Currently it supports the following:

* Repitition operators: \* \+ ? 
* Parenthesis
* Characters (no character sets)

`regex.py` is the interface, `parse.py` holds main implementation logic, `sample.py` shows some samples. 

You can run `python3 testing.py -v` to ensure it passes all test cases in `test_suite.dat`

### Performance

This regex engine underperforms Python's `re` module on normal inputs (using Glenn Fowler's test suite -- see below), however it outperforms significantly on pathological inputs. 

![normal](plot_normal.jpg?raw=true)
![pathological](plot_path.jpg?raw=true)

### Credits

* Test suite is based on [Glenn Fowler](http://www2.research.att.com/~gsf/testregex/)'s regex test suites.

* [Russ Cox](http://swtch.com/~rsc/regexp/) has an excellent collection of articles on regex.
