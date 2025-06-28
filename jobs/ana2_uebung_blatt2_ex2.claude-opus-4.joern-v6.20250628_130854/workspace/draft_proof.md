# Proof for Part a)

Starting with t = tan(x/2), we need to prove:
- sin(x) = 2t/(1+t²)
- cos(x) = (1-t²)/(1+t²)
- dx = 2/(1+t²)dt

## Step 1: Express sin(x) and cos(x) using half-angle formulas

We know:
- sin(x) = 2sin(x/2)cos(x/2)
- cos(x) = cos²(x/2) - sin²(x/2) = 2cos²(x/2) - 1 = 1 - 2sin²(x/2)

## Step 2: Express sin(x/2) and cos(x/2) in terms of t

Since t = tan(x/2) = sin(x/2)/cos(x/2), we have:
- sin(x/2) = t·cos(x/2)

Using sin²(x/2) + cos²(x/2) = 1:
- t²cos²(x/2) + cos²(x/2) = 1
- cos²(x/2)(1 + t²) = 1
- cos²(x/2) = 1/(1 + t²)
- cos(x/2) = 1/√(1 + t²) (taking positive root since x/2 ∈ (-π/2, π/2) for x ∈ (-π, π))

Therefore:
- sin(x/2) = t/√(1 + t²)

## Step 3: Substitute into sin(x) and cos(x)

sin(x) = 2sin(x/2)cos(x/2) = 2 · (t/√(1 + t²)) · (1/√(1 + t²)) = 2t/(1 + t²)

cos(x) = cos²(x/2) - sin²(x/2) = 1/(1 + t²) - t²/(1 + t²) = (1 - t²)/(1 + t²)

## Step 4: Find dx in terms of dt

Since t = tan(x/2), we have:
dt/dx = (1/2)sec²(x/2) = (1/2)(1 + tan²(x/2)) = (1/2)(1 + t²)

Therefore:
dx = 2dt/(1 + t²)