# Dynamic Programming - Quick Reference

## When to Use DP

**Keywords that indicate DP:**
- "Minimum/Maximum ways to..."
- "Count number of ways..."
- "Longest/Shortest..."
- "Is it possible to..."
- Optimization problems with choices

**Must have both:**
1. Overlapping subproblems (same calculation multiple times)
2. Optimal substructure (optimal solution contains optimal subsolutions)

## Top-Down vs Bottom-Up

### Top-Down (Memoization)
```python
def dp_topdown(n, memo=None):
    if memo is None:
        memo = {}

    # Base case
    if base_condition:
        return base_value

    # Check memo
    if n in memo:
        return memo[n]

    # Compute and store
    memo[n] = recurrence_relation
    return memo[n]
```

**Pros:** Natural, only computes needed states
**Cons:** Recursion overhead, possible stack overflow

### Bottom-Up (Tabulation)
```python
def dp_bottomup(n):
    # Base case
    dp = [base_value] * (n + 1)

    # Fill table
    for i in range(start, n + 1):
        dp[i] = recurrence_relation

    return dp[n]
```

**Pros:** No recursion, easier to optimize space
**Cons:** Computes all states, less intuitive

## Common DP Patterns

### 1. Linear Sequence (1D DP)
```python
# State: dp[i] = answer for first i elements
dp = [0] * (n + 1)
dp[0] = base

for i in range(1, n + 1):
    dp[i] = function_of(dp[i-1], dp[i-2], ...)
```
**Examples:** Climbing Stairs, House Robber, Decode Ways

### 2. Unbounded Knapsack
```python
# State: dp[i] = answer for capacity i
# Can use items unlimited times
dp = [base] * (capacity + 1)

for i in range(1, capacity + 1):
    for item in items:
        if i >= item.weight:
            dp[i] = optimize(dp[i], dp[i - item.weight] + item.value)
```
**Examples:** Coin Change, Coin Change II

### 3. 0/1 Knapsack
```python
# State: dp[i][w] = answer using first i items, capacity w
# Each item used at most once
dp = [[0] * (W + 1) for _ in range(n + 1)]

for i in range(1, n + 1):
    for w in range(W + 1):
        # Don't take
        dp[i][w] = dp[i-1][w]
        # Take if possible
        if w >= weight[i-1]:
            dp[i][w] = max(dp[i][w],
                          dp[i-1][w - weight[i-1]] + value[i-1])
```
**Examples:** Partition Equal Subset Sum, Target Sum

### 4. Longest Increasing Subsequence (LIS)
```python
# State: dp[i] = length of LIS ending at i
dp = [1] * n

for i in range(1, n):
    for j in range(i):
        if nums[j] < nums[i]:
            dp[i] = max(dp[i], dp[j] + 1)

return max(dp)  # Time: O(n²)
```
**Optimized:** Use binary search for O(n log n)

### 5. String Matching (2D DP)
```python
# State: dp[i][j] = answer for s1[0:i] and s2[0:j]
m, n = len(s1), len(s2)
dp = [[0] * (n + 1) for _ in range(m + 1)]

# Base cases
for i in range(m + 1):
    dp[i][0] = base_i
for j in range(n + 1):
    dp[0][j] = base_j

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```
**Examples:** LCS, Edit Distance, Distinct Subsequences

### 6. Grid Path (2D DP)
```python
# State: dp[i][j] = answer at cell (i, j)
m, n = len(grid), len(grid[0])
dp = [[0] * n for _ in range(m)]

# Base case
dp[0][0] = grid[0][0]

# First row and column
for i in range(1, m):
    dp[i][0] = dp[i-1][0] + grid[i][0]
for j in range(1, n):
    dp[0][j] = dp[0][j-1] + grid[0][j]

# Fill rest
for i in range(1, m):
    for j in range(1, n):
        dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
```
**Examples:** Unique Paths, Minimum Path Sum

### 7. Interval DP
```python
# State: dp[i][j] = answer for interval [i, j]
n = len(arr)
dp = [[0] * n for _ in range(n)]

# Base: single elements
for i in range(n):
    dp[i][i] = base

# Fill by increasing length
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        # Try all possible splits
        for k in range(i, j):
            dp[i][j] = optimize(dp[i][j],
                               dp[i][k] + dp[k+1][j] + cost)
```
**Examples:** Burst Balloons, Palindrome Partitioning

## Space Optimization Techniques

### 1. Two Variables (1D DP)
```python
# If dp[i] only needs dp[i-1] and dp[i-2]
# O(n) space → O(1) space

# Before
dp = [0] * (n + 1)
dp[i] = dp[i-1] + dp[i-2]

# After
prev2, prev1 = 0, 1
for i in range(2, n + 1):
    curr = prev1 + prev2
    prev2, prev1 = prev1, curr
```

### 2. Rolling Array (2D DP)
```python
# If dp[i] only needs dp[i-1]
# O(m*n) space → O(n) space

# Before
dp = [[0] * n for _ in range(m)]

# After
prev = [0] * n
curr = [0] * n
for i in range(m):
    for j in range(n):
        curr[j] = function_of(prev[j], curr[j-1])
    prev, curr = curr, prev
```

### 3. In-Place Modification
```python
# Modify input array if allowed
for i in range(1, m):
    for j in range(1, n):
        grid[i][j] += min(grid[i-1][j], grid[i][j-1])
```

## Complexity Analysis

**Time Complexity:**
- Number of states × Time per state
- Example: 2D DP with m×n states, O(1) per state → O(m×n)

**Space Complexity:**
- Size of DP table
- Often can optimize (see above)

| Problem | Time | Space | Space Optimized |
|---------|------|-------|-----------------|
| Fibonacci | O(n) | O(n) | O(1) |
| Coin Change | O(amount × coins) | O(amount) | - |
| LCS | O(m × n) | O(m × n) | O(min(m,n)) |
| 0/1 Knapsack | O(n × W) | O(n × W) | O(W) |
| LIS | O(n²) | O(n) | - |

## Problem Recognition Guide

| Problem Type | Clues | Pattern |
|--------------|-------|---------|
| Count ways to reach goal | "How many ways", "Number of paths" | Linear/Grid DP |
| Minimize/Maximize cost | "Minimum cost", "Maximum profit" | Knapsack/Linear |
| Longest/Shortest subsequence | "Longest increasing", "Shortest common" | LIS/LCS |
| Multiple items, limited capacity | "Knapsack", "Subset sum" | 0/1 Knapsack |
| Unlimited supply | "Coin change", "Unbounded" | Unbounded Knapsack |
| Two strings comparison | "Edit distance", "Common subsequence" | 2D String DP |
| Grid navigation | "Unique paths", "Path sum" | Grid DP |
| Range/Interval problems | "Burst balloons", "Palindrome partitioning" | Interval DP |

## Common Recurrence Relations

```python
# Fibonacci-style
dp[i] = dp[i-1] + dp[i-2]

# Climbing stairs (1 or 2 steps)
dp[i] = dp[i-1] + dp[i-2]

# House Robber
dp[i] = max(dp[i-1], dp[i-2] + nums[i])

# Coin Change (minimum coins)
dp[i] = min(dp[i - coin] + 1 for coin in coins if i >= coin)

# Coin Change II (count ways)
for coin in coins:
    for i in range(coin, amount + 1):
        dp[i] += dp[i - coin]

# Longest Common Subsequence
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

# Edit Distance
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1]
else:
    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

# Unique Paths (grid)
dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

## Step-by-Step Process

1. **Identify DP** - Check for overlapping subproblems and optimal substructure
2. **Define State** - What info do we need to track? (dp[i] means what?)
3. **Find Recurrence** - How to compute dp[i] from previous states?
4. **Base Cases** - What are the simplest cases we know?
5. **Order** - What order to compute states (bottom-up)?
6. **Implement** - Code it up
7. **Optimize** - Can we reduce space?

## Common Pitfalls

1. **Wrong base cases** - Most common error
2. **Off-by-one errors** - Array indexing mistakes
3. **Wrong initialization** - Use `float('inf')` for min, `-float('inf')` for max
4. **Missing state transitions** - Not considering all possibilities
5. **Wrong iteration order** - Computing state before dependencies ready
6. **Not checking bounds** - Index out of range

## Interview Template

```python
def dp_problem(input):
    # 1. Handle edge cases
    if not input:
        return default

    # 2. Initialize DP table
    n = len(input)
    dp = [base_value] * (n + 1)

    # 3. Set base cases
    dp[0] = base_case

    # 4. Fill DP table
    for i in range(1, n + 1):
        # Consider all transitions
        dp[i] = recurrence_relation

    # 5. Return answer
    return dp[n]
```

## DP vs Other Approaches

### DP vs Greedy
- **Greedy**: Local optimal → Global optimal (faster but doesn't always work)
- **DP**: Try all, pick best (slower but guaranteed optimal)
- **Test**: Can you find counterexample where greedy fails?

### DP vs Backtracking
- **Backtracking**: Find all solutions, actual paths
- **DP**: Count/min/max, optimal value only
- **Combine**: DP for value, backtracking to reconstruct path

### DP vs Divide & Conquer
- **D&C**: Independent subproblems (merge sort, binary search)
- **DP**: Overlapping subproblems (fibonacci, LCS)

## Quick Wins

1. **Start with recursion** - Easier to think about
2. **Add memoization** - Quick win, prevents recomputation
3. **Convert to tabulation** - If needed for space optimization
4. **Draw small example** - Visualize the DP table
5. **Verify base cases** - Test with n=0, n=1
6. **Check dependencies** - Make sure order is correct

## Must-Know Problems

**Foundations:**
- Fibonacci (introduce memoization)
- Climbing Stairs (1D DP basics)
- House Robber (decision at each step)

**Knapsack:**
- Coin Change (unbounded knapsack)
- Partition Equal Subset Sum (0/1 knapsack)

**Strings:**
- Longest Common Subsequence (2D DP)
- Edit Distance (2D with 3 operations)

**Sequences:**
- Longest Increasing Subsequence (O(n²) and O(n log n))

**Grids:**
- Unique Paths (2D grid navigation)

**Master these and you'll handle 80% of DP problems!**
