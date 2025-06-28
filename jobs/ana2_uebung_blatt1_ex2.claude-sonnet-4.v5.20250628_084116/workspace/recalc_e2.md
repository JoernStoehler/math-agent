# More careful calculation of (e)

Let I = ∫e^x sin(x) dx and J = ∫e^x cos(x) dx

For I: u = sin(x), v' = e^x
u' = cos(x), v = e^x
I = e^x sin(x) - ∫e^x cos(x) dx = e^x sin(x) - J

For J: u = cos(x), v' = e^x
u' = -sin(x), v = e^x
J = e^x cos(x) - ∫e^x (-sin(x)) dx = e^x cos(x) + ∫e^x sin(x) dx = e^x cos(x) + I

From the two equations:
I = e^x sin(x) - J
J = e^x cos(x) + I

Substituting the second into the first:
I = e^x sin(x) - (e^x cos(x) + I)
I = e^x sin(x) - e^x cos(x) - I
2I = e^x(sin(x) - cos(x))
I = (1/2)e^x(sin(x) - cos(x))

Actually, let me double-check by differentiating:
d/dx[(1/2)e^x(sin(x) - cos(x))] = (1/2)[e^x(sin(x) - cos(x)) + e^x(cos(x) + sin(x))]
                                  = (1/2)[e^x sin(x) - e^x cos(x) + e^x cos(x) + e^x sin(x)]
                                  = (1/2)[2e^x sin(x)]
                                  = e^x sin(x) ✓

So the answer is correct! But wait, I made a sign error. Let me recalculate more carefully.

Actually, the issue is that I have:
I = (1/2)e^x(sin(x) - cos(x))

But some sources give:
I = (1/2)e^x(sin(x) + cos(x))

Let me verify once more by substitution back into the original equations...