# Draft Solution for Fibonacci Exercise

## Part (a): Sum formula
We need to prove: $\sum_{i=0}^{n} f_i = f_{n+2} - 1$

Base case: 
- For n=0: $f_0 = 1 = f_2 - 1 = 2 - 1 = 1$ ✓
- For n=1: $f_0 + f_1 = 1 + 1 = 2 = f_3 - 1 = 3 - 1 = 2$ ✓

Inductive step: Assume $\sum_{i=0}^{n} f_i = f_{n+2} - 1$ holds.
Need to show: $\sum_{i=0}^{n+1} f_i = f_{n+3} - 1$

$\sum_{i=0}^{n+1} f_i = \sum_{i=0}^{n} f_i + f_{n+1} = (f_{n+2} - 1) + f_{n+1} = f_{n+2} + f_{n+1} - 1 = f_{n+3} - 1$ ✓

## Part (b): Divisibility
We need to prove: $f_n | f_{2n}$ for all $n \in \mathbb{N}$

Let me verify with small values first:
- n=1: $f_1 = 1$ divides $f_2 = 2$? Wait, that's wrong...
- Let me recalculate the Fibonacci sequence: $f_0 = 1, f_1 = 1, f_2 = 2, f_3 = 3, f_4 = 5, f_5 = 8, f_6 = 13$...

For n=1: $f_1 = 1$ divides $f_2 = 2$? No!
For n=2: $f_2 = 2$ divides $f_4 = 5$? No!

This seems wrong. Let me think about a different approach...

Actually, I need to prove this by induction. Let me think about a formula or pattern.

## Part (c): Relative primality
We need to prove: $\gcd(f_n, f_{n+1}) = 1$ for all $n \in \mathbb{N}$

This can be proven using the Euclidean algorithm and the recursive definition.