# Style Guide

## Some basic principles for the style guide:

1. Use tabs, not spaces. Any PR with spaces will be asked to reformat.
2. For long parameter lists, put the commas on the line with the *next* parameter, like so:
```python
foo(
	some_parameter
	, some_other_parameter
	, a_third_parameter
	, blorp
)
```
3. Use `underscores_for_naming` your functions and variables
```python
my_foo = 5 # Good
myFoo = 5 # Bad
```
