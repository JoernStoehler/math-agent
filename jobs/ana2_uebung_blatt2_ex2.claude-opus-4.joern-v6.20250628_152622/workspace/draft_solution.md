# Draft Solution

## Part (a): Proving the substitution formulas

Let $t = \tan(\frac{x}{2})$

First, I need to derive the formulas for $\sin(x)$, $\cos(x)$, and $dx$ in terms of $t$.

### Finding $\sin(x)$:
Using the double angle formula:
$\sin(x) = 2\sin(\frac{x}{2})\cos(\frac{x}{2})$

From $t = \tan(\frac{x}{2}) = \frac{\sin(\frac{x}{2})}{\cos(\frac{x}{2})}$, we have:
- $\sin(\frac{x}{2}) = t\cos(\frac{x}{2})$

Using the identity $\sin^2(\frac{x}{2}) + \cos^2(\frac{x}{2}) = 1$:
- $t^2\cos^2(\frac{x}{2}) + \cos^2(\frac{x}{2}) = 1$
- $\cos^2(\frac{x}{2})(t^2 + 1) = 1$
- $\cos^2(\frac{x}{2}) = \frac{1}{1+t^2}$
- $\cos(\frac{x}{2}) = \frac{1}{\sqrt{1+t^2}}$ (taking positive root since $x \in [-\pi, \pi]$ means $\frac{x}{2} \in [-\frac{\pi}{2}, \frac{\pi}{2}]$)

Therefore:
- $\sin(\frac{x}{2}) = \frac{t}{\sqrt{1+t^2}}$

So:
$\sin(x) = 2 \cdot \frac{t}{\sqrt{1+t^2}} \cdot \frac{1}{\sqrt{1+t^2}} = \frac{2t}{1+t^2}$

### Finding $\cos(x)$:
Using the double angle formula:
$\cos(x) = \cos^2(\frac{x}{2}) - \sin^2(\frac{x}{2})$

$\cos(x) = \frac{1}{1+t^2} - \frac{t^2}{1+t^2} = \frac{1-t^2}{1+t^2}$

### Finding $dx$:
From $t = \tan(\frac{x}{2})$:
$\frac{dt}{dx} = \frac{1}{2}\sec^2(\frac{x}{2}) = \frac{1}{2}(1 + \tan^2(\frac{x}{2})) = \frac{1}{2}(1 + t^2)$

Therefore:
$dx = \frac{2}{1+t^2}dt$

## Part (b): Calculate the integral

$\int_0^\pi \frac{\sin(x)^2}{\sin(x)+\cos(x)}dx$

Using the substitution $t = \tan(\frac{x}{2})$:
- When $x = 0$: $t = \tan(0) = 0$
- When $x = \pi$: $t = \tan(\frac{\pi}{2}) = \infty$

The integral becomes:
$\int_0^\infty \frac{(\frac{2t}{1+t^2})^2}{\frac{2t}{1+t^2} + \frac{1-t^2}{1+t^2}} \cdot \frac{2}{1+t^2}dt$

Simplifying the integrand:
- Numerator: $\frac{4t^2}{(1+t^2)^2}$
- Denominator: $\frac{2t + 1 - t^2}{1+t^2} = \frac{1 + 2t - t^2}{1+t^2}$

So the integrand is:
$\frac{\frac{4t^2}{(1+t^2)^2}}{\frac{1 + 2t - t^2}{1+t^2}} \cdot \frac{2}{1+t^2} = \frac{4t^2}{(1+t^2)^2} \cdot \frac{1+t^2}{1 + 2t - t^2} \cdot \frac{2}{1+t^2}$

$= \frac{8t^2}{(1+t^2)^2} \cdot \frac{1+t^2}{1 + 2t - t^2} = \frac{8t^2}{(1+t^2)(1 + 2t - t^2)}$

Need to do partial fraction decomposition...