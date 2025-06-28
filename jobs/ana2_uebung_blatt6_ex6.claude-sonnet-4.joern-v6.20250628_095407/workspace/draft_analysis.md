# Analysis of Exercise

## Part (a)
We need to show that the curve f:[0,1]→ℝ² defined by:
- f(t) = (t, t·cos(π/t)) for t > 0
- f(0) = (0, 0) for t = 0

is:
1. Continuous (including at t=0)
2. Not rectifiable

### Continuity:
- For t > 0: f is continuous as composition of continuous functions
- At t = 0: Need to show lim_{t→0⁺} f(t) = f(0) = (0,0)
  - First component: lim_{t→0⁺} t = 0 ✓
  - Second component: lim_{t→0⁺} t·cos(π/t) = 0 (since |cos(π/t)| ≤ 1)

### Non-rectifiability:
The key insight is that cos(π/t) oscillates infinitely often as t → 0⁺.
We'll show the curve has infinite length by considering partitions.

For partition points t_k = 1/k (k = 1, 2, 3, ...), the curve oscillates between
local maxima and minima, creating an infinite sum of lengths.

## Part (b)
We need to show that for any rectifiable curve f:[a,b]→ℝ², there exists a point
in [0,1]² that is not in the image of f.

Key insight: Rectifiable curves have finite length, hence their image has
2-dimensional Lebesgue measure zero. Since [0,1]² has positive measure,
there must be points not in the image.