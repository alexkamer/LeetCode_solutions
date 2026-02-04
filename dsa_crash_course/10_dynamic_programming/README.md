# Dynamic Programming

Dynamic Programming (DP) is a powerful algorithmic technique for solving optimization problems by breaking them down into simpler subproblems. It's one of the most important topics in coding interviews and appears frequently in technical assessments.

## What is Dynamic Programming?

**Dynamic Programming** is an optimization technique that solves complex problems by:
1. Breaking them down into simpler overlapping subproblems
2. Solving each subproblem once and storing the result
3. Reusing stored results to avoid redundant calculations

The name "dynamic programming" was coined by Richard Bellman in the 1950s. Despite the name, it has nothing to do with "programming" in the coding sense - it refers to mathematical optimization.

### Key Insight

DP transforms exponential time complexity problems into polynomial time by trading space for time - storing results to avoid recomputation.

## Two Essential Properties

For a problem to be suitable for DP, it must have both:

### 1. Overlapping Subproblems

The problem can be broken down into subproblems that are reused multiple times.

**Example: Fibonacci Numbers**
```
fib(5) = fib(4) + fib(3)
fib(4) = fib(3) + fib(2)
fib(3) = fib(2) + fib(1)
```

Notice `fib(3)` is calculated twice, `fib(2)` three times! This redundancy grows exponentially.

**Without DP (naive recursion)**: O(2^n) time
**With DP (memoization)**: O(n) time

### 2. Optimal Substructure

The optimal solution to the problem can be constructed from optimal solutions to its subproblems.

**Example: Shortest Path**
If the shortest path from A to C goes through B, then:
- Path A → C = Path A → B + Path B → C
- Both A → B and B → C must also be shortest paths

**Counter-example**: Longest simple path (no cycles) does NOT have optimal substructure because subpaths of the longest path aren't necessarily the longest paths themselves.

## Two Main Approaches

### Top-Down (Memoization)

Start with the original problem and recursively break it down, storing results.

**Characteristics:**
- Natural recursive implementation
- Only computes needed subproblems
- Uses call stack (can cause stack overflow)
- Easier to implement initially

```python
def fibonacci_memo(n, memo=None):
    if memo is None:
        memo = {}

    # Base cases
    if n <= 1:
        return n

    # Check if already computed
    if n in memo:
        return memo[n]

    # Compute and store
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]
```

### Bottom-Up (Tabulation)

Start with the smallest subproblems and build up to the original problem.

**Characteristics:**
- Iterative implementation
- Computes all subproblems (even if not needed)
- No recursion overhead
- Often more space-efficient
- Preferred in interviews

```python
def fibonacci_tabulation(n):
    if n <= 1:
        return n

    # Build table from bottom up
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]
```

### Comparison

| Aspect | Top-Down | Bottom-Up |
|--------|----------|-----------|
| Implementation | Recursive | Iterative |
| Subproblems | Only needed ones | All subproblems |
| Stack Usage | Uses call stack | No recursion |
| Space Optimization | Harder | Easier |
| Intuition | More natural | Requires more thought |
| Performance | Slight overhead | Generally faster |

## The DP Problem-Solving Framework

### Step 1: Identify if it's a DP Problem

**Red flags indicating DP:**
- "Find the minimum/maximum way to..."
- "Count the number of ways to..."
- "What's the longest/shortest..."
- Optimization with multiple choices at each step
- Brute force solution is exponential

**Keywords:** minimum, maximum, longest, shortest, count ways, optimize

### Step 2: Define the State

**The state is what information you need to store.**

Questions to ask:
- What changes as we progress through the problem?
- What parameters uniquely identify a subproblem?
- What's the minimum information needed?

**Examples:**
- **Fibonacci**: `dp[i]` = i-th Fibonacci number
- **Coin Change**: `dp[i]` = minimum coins to make amount i
- **Longest Common Subsequence**: `dp[i][j]` = LCS of first i chars of s1 and first j chars of s2

### Step 3: Define the Recurrence Relation

**Express the answer in terms of smaller subproblems.**

Pattern: `dp[current_state] = function(dp[previous_states])`

**Examples:**
```python
# Fibonacci
dp[i] = dp[i-1] + dp[i-2]

# Coin Change
dp[i] = min(dp[i - coin] + 1 for all coins)

# House Robber
dp[i] = max(dp[i-1], dp[i-2] + nums[i])
```

### Step 4: Identify Base Cases

**What are the simplest subproblems with known answers?**

**Examples:**
- `fib(0) = 0, fib(1) = 1`
- `dp[0] = 0` (0 coins needed for amount 0)
- Empty string has 0 length

### Step 5: Determine Order of Computation

**For bottom-up: In what order should we fill the DP table?**

Usually:
- 1D array: left to right
- 2D array: row by row, left to right

Make sure previous states are computed before current state.

### Step 6: Optimize Space (if possible)

**Can we reduce space complexity?**

Common optimizations:
- 1D DP using only last 2 values: O(n) → O(1)
- 2D DP using only last row: O(n*m) → O(n)

## Common DP Patterns

### 1. Linear Sequence (1D DP)

**Problem structure:** Make decisions at each position in a sequence.

**State:** `dp[i]` = answer for first i elements

**Examples:**
- Climbing Stairs
- House Robber
- Decode Ways
- Jump Game

**Template:**
```python
def linear_dp(arr):
    n = len(arr)
    dp = [0] * (n + 1)

    # Base case
    dp[0] = base_value

    # Fill table
    for i in range(1, n + 1):
        dp[i] = function_of(dp[i-1], dp[i-2], ...)

    return dp[n]
```

### 2. Unbounded Knapsack

**Problem structure:** Unlimited supply of items, maximize value within capacity.

**State:** `dp[i]` = best solution for capacity i

**Examples:**
- Coin Change
- Coin Change II (count ways)
- Perfect Squares

**Template:**
```python
def unbounded_knapsack(capacity, items):
    dp = [0] * (capacity + 1)

    for i in range(1, capacity + 1):
        for item in items:
            if i >= item.weight:
                dp[i] = max(dp[i], dp[i - item.weight] + item.value)

    return dp[capacity]
```

### 3. 0/1 Knapsack

**Problem structure:** Each item can be used once, maximize value.

**State:** `dp[i][w]` = max value using first i items with weight limit w

**Examples:**
- Partition Equal Subset Sum
- Target Sum
- Last Stone Weight II

**Template:**
```python
def zero_one_knapsack(items, capacity):
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i-1
            dp[i][w] = dp[i-1][w]

            # Take item i-1 if possible
            if w >= items[i-1].weight:
                dp[i][w] = max(dp[i][w],
                              dp[i-1][w - items[i-1].weight] + items[i-1].value)

    return dp[n][capacity]
```

### 4. Longest Increasing Subsequence (LIS)

**Problem structure:** Find longest subsequence with increasing elements.

**State:** `dp[i]` = length of LIS ending at index i

**Examples:**
- Longest Increasing Subsequence
- Russian Doll Envelopes
- Maximum Length of Pair Chain

**Template:**
```python
def lis(nums):
    n = len(nums)
    dp = [1] * n  # Each element is a subsequence of length 1

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)
```

### 5. String/Subsequence (2D DP)

**Problem structure:** Compare two strings/sequences.

**State:** `dp[i][j]` = answer for s1[0:i] and s2[0:j]

**Examples:**
- Longest Common Subsequence
- Edit Distance
- Distinct Subsequences
- Interleaving String

**Template:**
```python
def string_dp(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = base_value_for_i
    for j in range(n + 1):
        dp[0][j] = base_value_for_j

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + something
            else:
                dp[i][j] = function_of(dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

### 6. Grid Path (2D DP)

**Problem structure:** Navigate a 2D grid with certain rules.

**State:** `dp[i][j]` = answer at cell (i, j)

**Examples:**
- Unique Paths
- Minimum Path Sum
- Dungeon Game
- Cherry Pickup

**Template:**
```python
def grid_path(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]

    # Base case: starting position
    dp[0][0] = grid[0][0]

    # Fill first row and column
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + grid[0][j]

    # Fill rest
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = function_of(dp[i-1][j], dp[i][j-1]) + grid[i][j]

    return dp[m-1][n-1]
```

### 7. Interval DP

**Problem structure:** Process intervals or subsequences.

**State:** `dp[i][j]` = answer for subarray from i to j

**Examples:**
- Longest Palindromic Subsequence
- Palindrome Partitioning II
- Burst Balloons
- Minimum Cost Tree From Leaf Values

**Template:**
```python
def interval_dp(arr):
    n = len(arr)
    dp = [[0] * n for _ in range(n)]

    # Base case: single elements
    for i in range(n):
        dp[i][i] = base_value

    # Fill by increasing interval length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = optimal_over_all_splits(i, j)

    return dp[0][n-1]
```

## Space Optimization Techniques

### 1. Reducing Dimensions

If `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`:

**Before (O(n) space):**
```python
dp = [0] * (n + 1)
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
```

**After (O(1) space):**
```python
prev2, prev1 = 0, 1
for i in range(2, n + 1):
    current = prev1 + prev2
    prev2, prev1 = prev1, current
```

### 2. Rolling Array

For 2D DP where row i only depends on row i-1:

**Before (O(m*n) space):**
```python
dp = [[0] * n for _ in range(m)]
```

**After (O(n) space):**
```python
prev_row = [0] * n
curr_row = [0] * n

for i in range(m):
    for j in range(n):
        curr_row[j] = function_of(prev_row[j], curr_row[j-1])
    prev_row, curr_row = curr_row, prev_row
```

### 3. In-Place Modification

Sometimes you can update the grid itself:

```python
# Instead of creating dp array
for i in range(1, m):
    for j in range(1, n):
        grid[i][j] += min(grid[i-1][j], grid[i][j-1])

return grid[m-1][n-1]
```

## DP vs Other Paradigms

### DP vs Greedy

**Greedy:** Makes locally optimal choice at each step.
**DP:** Considers all possibilities and finds global optimum.

**When to use Greedy:**
- Locally optimal choices lead to globally optimal solution
- Problem has greedy choice property
- Usually O(n) or O(n log n)

**When to use DP:**
- Need to explore all possibilities
- Greedy approach doesn't work (counterexample exists)
- Usually O(n^2) or higher

**Example where Greedy fails:**
- Coin change with coins [1, 3, 4] and amount 6
- Greedy: 4 + 1 + 1 = 3 coins
- Optimal: 3 + 3 = 2 coins

### DP vs Backtracking

**Backtracking:** Explores all possibilities, prunes invalid paths.
**DP:** Stores results to avoid recomputing.

**When to use Backtracking:**
- Need to find all solutions (not just count)
- Need the actual paths/combinations
- Problem has constraints that allow pruning

**When to use DP:**
- Overlapping subproblems exist
- Only need count/minimum/maximum
- No need for actual solution path

**Can combine both:**
- Use DP to find optimal value
- Use backtracking to reconstruct solution

### DP vs Divide and Conquer

**Divide and Conquer:** Splits into independent subproblems.
**DP:** Splits into overlapping subproblems.

**Divide and Conquer examples:** Merge sort, quick sort, binary search
**DP examples:** When subproblems overlap and are reused

## Time and Space Complexity

### Analyzing DP Complexity

**Time Complexity:**
- Number of states × Time per state
- Count unique subproblems × Work for each

**Space Complexity:**
- Size of DP table/memo
- Can often be optimized

**Examples:**

| Problem | States | Time per State | Time | Space | Can Optimize |
|---------|--------|----------------|------|-------|--------------|
| Fibonacci | n | O(1) | O(n) | O(n) | Yes → O(1) |
| Coin Change | amount | O(coins) | O(amount × coins) | O(amount) | No |
| LCS | m × n | O(1) | O(m × n) | O(m × n) | Yes → O(n) |
| LIS | n | O(n) | O(n²) | O(n) | No* |
| Grid Paths | m × n | O(1) | O(m × n) | O(m × n) | Yes → O(n) |

*LIS can be optimized to O(n log n) using binary search + different approach

## Common Pitfalls and Tips

### Pitfalls to Avoid

1. **Wrong base cases** - Most common error, test small examples
2. **Off-by-one errors** - Carefully handle indices and array sizes
3. **Not considering all transitions** - Miss some possibilities in recurrence
4. **Initializing with wrong values** - Use `float('inf')` for min, `-float('inf')` for max
5. **Forgetting to check bounds** - Array index out of bounds
6. **Computing states in wrong order** - In bottom-up, ensure dependencies are met

### Interview Tips

1. **Start with recursion** - Write brute force recursive solution first
2. **Add memoization** - Convert to top-down DP by adding memo
3. **Convert to tabulation** - Translate to bottom-up if needed
4. **Optimize space** - Look for space optimization opportunities
5. **Verify with examples** - Walk through small examples
6. **Explain state meaning** - Clearly define what `dp[i]` represents
7. **Draw diagrams** - Visualize the state transitions

### Problem-Solving Checklist

- [ ] Identify overlapping subproblems
- [ ] Identify optimal substructure
- [ ] Define the state clearly
- [ ] Write recurrence relation
- [ ] Identify base cases
- [ ] Choose top-down or bottom-up
- [ ] Implement solution
- [ ] Test with examples
- [ ] Optimize space if possible
- [ ] Analyze time and space complexity

## LeetCode Problem Categories

### Easy
- Climbing Stairs (70)
- Min Cost Climbing Stairs (746)
- Pascal's Triangle (118)
- Fibonacci Number (509)
- Divisor Game (1025)

### Medium
- House Robber (198)
- Coin Change (322)
- Longest Increasing Subsequence (300)
- Longest Common Subsequence (1143)
- Unique Paths (62)
- Word Break (139)
- Decode Ways (91)
- Maximum Product Subarray (152)
- Partition Equal Subset Sum (416)
- Target Sum (494)

### Hard
- Edit Distance (72)
- Longest Valid Parentheses (32)
- Best Time to Buy and Sell Stock III (123)
- Word Break II (140)
- Regular Expression Matching (10)
- Wildcard Matching (44)
- Burst Balloons (312)
- Dungeon Game (174)

## Related Topics

- **Greedy Algorithms** - Sometimes alternative to DP
- **Backtracking** - For exploring solution space
- **Graphs** - Shortest path algorithms use DP
- **Arrays** - DP often uses arrays for storage
- **Recursion** - Foundation for top-down DP

## Additional Resources

### Books
- "Introduction to Algorithms" (CLRS) - Chapter 15
- "Algorithm Design Manual" by Skiena
- "Competitive Programming" by Halim

### Online
- LeetCode DP tag problems
- Codeforces DP tutorials
- YouTube: Tushar Roy, Back To Back SWE

### Practice Strategy
1. Start with 1D DP problems (Fibonacci-style)
2. Move to unbounded knapsack (Coin Change)
3. Learn 0/1 knapsack pattern
4. Practice 2D DP (LCS, Grid paths)
5. Try harder patterns (Intervals, Trees)

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems with multiple approaches!
