# Peano Curve Construction Draft

## Understanding the Problem
We need to construct a continuous surjective map f: [0,1] → [0,1]² from the unit interval to the unit square.

## Construction Approach

The classic approach uses a recursive construction based on subdividing both the interval and the square into smaller parts.

### Key Ideas:
1. Divide [0,1] into 9 equal parts
2. Divide [0,1]² into 9 equal subsquares (3×3 grid)
3. Map each subinterval to a subsquare in a specific order
4. Recursively apply this process

### Construction Steps:

1. **Base Step**: Define a map φ₁: [0,1] → [0,1]² that visits 9 points in order:
   - [0, 1/9] → bottom-left corner region
   - [1/9, 2/9] → bottom-middle region
   - etc., following a specific path

2. **Recursive Step**: For each subsquare, apply a scaled and possibly reflected/rotated version of the base map

3. **Limit Process**: The Peano curve is the uniform limit of these approximations

### Mathematical Details:

The construction uses:
- Cantor's ternary representation of numbers in [0,1]
- A specific traversal pattern through the subsquares
- Careful handling of orientation to ensure continuity

The key is that at each stage, adjacent intervals map to adjacent squares, ensuring continuity in the limit.