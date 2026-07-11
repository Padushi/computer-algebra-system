# Computer Algebra System in Python

## Description

This computer algebra system will be a command line REPL that allows for basic symbolic manipulation, including:

- Differentiation
- Integration
- Equation solving
- Expression simplification

## Syntax

Declarations are written using the 'let' keyword and ':=' operator:
```
> let eq1 := x + 3 = 9x - 5             # An equation
> let delta := b^2 - 4ac                # An expression
> let f(x) := sqrt(8x - 3) - sin(x)     # A function
```

Operations are predifined functions called by name; arguments are enclosed in parentheses:
```
> sqrt(x + sin(7))
> diff(f(x), x)
> limit((9x^2 + 3)/x^2, 7)
```