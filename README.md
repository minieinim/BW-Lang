# BW Lang
## Syntax
### Hello World
```
print "Hello World\n"
# prints "Hello World"
```
### Functions and Variables
```
let foo 1 # defines a variable
print foo "\n"
let bar (print $1 "\n") #defines a function
bar "Hello World:
```
### If Statements
```
print (if True "Hello World" "Goodbye World") "\n"
# prints "Hello World"
print (if False "Hello World" "Goodbye World") "\n"
# prints "Goodbye World"
```
### Comparision
```
print (= 1 2) "\n" # False
print (< 1 2) "\n" # True
print (> 1 2) "\n" # False
```
## Types
### String
```
"Hello World" # this is a string
```
### Number
```
1 # this is a number
3.14 # this is also a number
```
### Boolean
```
True
False
# these are boolean
```
