# Proof Strategy

Using De Moivre's theorem: $(\cos x + i\sin x)^n = \cos(nx) + i\sin(nx)$

We expand the left side using the binomial theorem:
$$(\cos x + i\sin x)^n = \sum_{k=0}^{n} \binom{n}{k} \cos^{n-k}(x) (i\sin x)^k$$

Since $i^k$ cycles through $1, i, -1, -i$ for $k = 0, 1, 2, 3, ...$, we have:
- $i^{2k} = (-1)^k$ (real part)
- $i^{2k+1} = i(-1)^k$ (imaginary part)

Separating real and imaginary parts:
- Real part: $\sum_{k=0}^{\lfloor n/2 \rfloor} \binom{n}{2k} \cos^{n-2k}(x) \sin^{2k}(x) (-1)^k = \cos(nx)$
- Imaginary part: $\sum_{k=0}^{\lfloor (n-1)/2 \rfloor} \binom{n}{2k+1} \cos^{n-2k-1}(x) \sin^{2k+1}(x) (-1)^k = \sin(nx)$

Note: For the sin formula, when n is even, the upper limit is $\lfloor (n-1)/2 \rfloor = n/2 - 1$, and when n is odd, it's $(n-1)/2$. Both equal $\lfloor n/2 \rfloor$ when considering odd indices.