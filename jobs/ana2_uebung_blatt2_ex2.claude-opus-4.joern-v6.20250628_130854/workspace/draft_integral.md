# Solution for Part b)

We need to compute: ∫₀^π sin²(x)/(sin(x)+cos(x)) dx

Using the substitution t = tan(x/2):
- When x = 0: t = tan(0) = 0
- When x = π: t = tan(π/2) → ∞

Substituting:
- sin(x) = 2t/(1+t²)
- cos(x) = (1-t²)/(1+t²)
- dx = 2/(1+t²)dt

The integral becomes:
∫₀^∞ [4t²/(1+t²)²] / [2t/(1+t²) + (1-t²)/(1+t²)] · 2/(1+t²) dt

Simplifying the denominator:
sin(x) + cos(x) = 2t/(1+t²) + (1-t²)/(1+t²) = (2t + 1 - t²)/(1+t²)

So the integral is:
∫₀^∞ [4t²/(1+t²)²] · [(1+t²)/(2t + 1 - t²)] · 2/(1+t²) dt
= ∫₀^∞ 8t²/[(1+t²)²(2t + 1 - t²)] dt
= ∫₀^∞ 8t²/[(1+t²)(1+t²)(2t + 1 - t²)] dt
= ∫₀^∞ 8t²/[(1+t²)(1 - t² + 2t)] dt

Let me factor 1 - t² + 2t = -(t² - 2t - 1) = -(t - 1)² + 2

Actually, let me be more careful:
1 - t² + 2t = -t² + 2t + 1 = -(t² - 2t - 1) = -(t² - 2t + 1 - 2) = -(t-1)² + 2

Hmm, this is getting complex. Let me try a different approach using partial fractions.