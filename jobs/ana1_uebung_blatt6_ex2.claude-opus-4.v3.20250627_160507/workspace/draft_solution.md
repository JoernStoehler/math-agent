# Draft Solution

## Series (a): $\sum_{n=1}^\infty \frac{2^n n!}{n^n}$

Let $a_n = \frac{2^n n!}{n^n}$. Using the ratio test:

$\frac{a_{n+1}}{a_n} = \frac{2^{n+1} (n+1)!}{(n+1)^{n+1}} \cdot \frac{n^n}{2^n n!}$

$= \frac{2 \cdot (n+1) \cdot n^n}{(n+1)^{n+1}}$

$= \frac{2 \cdot (n+1) \cdot n^n}{(n+1) \cdot (n+1)^n}$

$= \frac{2 \cdot n^n}{(n+1)^n}$

$= 2 \cdot \left(\frac{n}{n+1}\right)^n$

$= 2 \cdot \left(1 - \frac{1}{n+1}\right)^n$

As $n \to \infty$: $\left(1 - \frac{1}{n+1}\right)^n \to e^{-1}$

Therefore: $\lim_{n \to \infty} \frac{a_{n+1}}{a_n} = \frac{2}{e} < 1$

Since $\frac{2}{e} \approx 0.736 < 1$, the series converges.

## Series (b): $\sum_{n=1}^\infty \frac{3^n n!}{n^n}$

Similarly, let $b_n = \frac{3^n n!}{n^n}$:

$\frac{b_{n+1}}{b_n} = 3 \cdot \left(\frac{n}{n+1}\right)^n \to \frac{3}{e} > 1$

Since $\frac{3}{e} \approx 1.104 > 1$, the series diverges.

## Series (c): $\sum_{n=1}^\infty \frac{1 + (-1)^n n}{n^2}$

Split into two series:
$\sum_{n=1}^\infty \frac{1 + (-1)^n n}{n^2} = \sum_{n=1}^\infty \frac{1}{n^2} + \sum_{n=1}^\infty \frac{(-1)^n n}{n^2}$

$= \sum_{n=1}^\infty \frac{1}{n^2} + \sum_{n=1}^\infty \frac{(-1)^n}{n}$

The first series is the p-series with p=2, which converges.
The second series is the alternating harmonic series, which converges.
Therefore, the sum converges.

## Series (d): $\sum_{n=0}^\infty \frac{x^n}{1+x^{2n}}$ for $x \in \mathbb{R}$

Need to consider different cases:
- If $|x| < 1$: $\frac{x^n}{1+x^{2n}} \approx x^n$ for large n, geometric series converges
- If $|x| = 1$: Need more careful analysis
- If $|x| > 1$: $\frac{x^n}{1+x^{2n}} \approx \frac{x^n}{x^{2n}} = x^{-n} \to 0$, but need to check convergence

Let me work through this more carefully...