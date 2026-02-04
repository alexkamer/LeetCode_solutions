# Backtracking

Backtracking is a powerful algorithmic technique for solving problems that require exploring all possible solutions. It's essentially a smart brute-force approach that abandons partial solutions as soon as it determines they cannot lead to a valid solution.

## What is Backtracking?

**Backtracking** is an algorithmic paradigm that incrementally builds candidates to solutions and abandons a candidate ("backtracks") as soon as it determines that this candidate cannot lead to a valid solution.

Think of it as exploring a maze:
- You try a path
- If you hit a dead end, you go back to the last decision point
- You try a different path
- Repeat until you find the exit or exhaust all possibilities

### Key Characteristics

- **Recursive** - Naturally expressed using recursion
- **Depth-First** - Explores one branch completely before trying others
- **Incremental** - Builds solution one piece at a time
- **Reversible** - Can undo choices (backtrack) when they don't work

## The Decision Tree Concept

Every backtracking problem can be visualized as a **decision tree**:

```
                         Start
                          []
                    /      |      \
                  [1]     [2]     [3]
                 / | \    / | \   / | \
               ... ... ... ... ... ... ...
```

- **Root**: Initial state (empty solution)
- **Nodes**: Partial solutions (decisions made so far)
- **Edges**: Choices/decisions
- **Leaves**: Complete solutions (or dead ends)

### Example: Generating Subsets of [1,2,3]

```
                         []
                    /          \
                  [1]           []
                 /   \         /   \
              [1,2]  [1]    [2]    []
              /  \   / \    / \    / \
          [1,2,3][1,2][1,3][1][2,3][2][3][]
```

At each node, we make a decision: **include** or **exclude** the current element.

## The Backtracking Template

All backtracking solutions follow this template:

```python
def backtrack(path, choices, result):
    """
    path: current partial solution being built
    choices: remaining options to explore
    result: collection of all valid solutions
    """
    # Base case: is this a complete solution?
    if is_valid_solution(path):
        result.append(path.copy())  # Must copy!
        return

    # Recursive case: try each possible choice
    for choice in choices:
        # 1. CHOOSE: Make a choice and add to path
        path.append(choice)

        # 2. EXPLORE: Recursively explore this path
        backtrack(path, new_choices, result)

        # 3. UNCHOOSE: Undo the choice (backtrack)
        path.pop()
```

### Three Steps of Backtracking

1. **CHOOSE**: Make a decision/choice
   - Add element to current path
   - Mark as visited/used
   - Update state

2. **EXPLORE**: Recursively explore consequences
   - Call backtrack with updated state
   - This explores the subtree for this choice

3. **UNCHOOSE**: Undo the choice
   - Remove element from path
   - Unmark as visited/used
   - Restore previous state

This "choose-explore-unchoose" pattern is the heart of backtracking.

## When to Use Backtracking

Use backtracking when:

1. **Generate all possibilities**: Need to explore all combinations/permutations
   - Subsets, permutations, combinations
   - "Find all possible..."
   - "Generate all valid..."

2. **Constraint satisfaction**: Find solutions satisfying constraints
   - N-Queens
   - Sudoku solver
   - Graph coloring

3. **Optimization**: Find best solution among all possibilities
   - Combination sum
   - Word break
   - Often combined with pruning

4. **Decision problems**: Can we achieve goal?
   - Path exists?
   - Word search in grid
   - Can partition?

### Keywords that Hint Backtracking

- "Find all combinations/permutations"
- "Generate all possible solutions"
- "Place N items with constraints"
- "Partition into groups"
- "Word search/pattern matching"
- "Can we achieve X by trying all possibilities?"

## Pruning Techniques

**Pruning** is the optimization that makes backtracking practical. It means stopping exploration of a branch early when we know it can't lead to a valid solution.

### Why Prune?

Without pruning, backtracking explores the entire decision tree, which can be exponential. Pruning can reduce:
- Time complexity significantly
- Number of branches explored
- Unnecessary recursive calls

### Common Pruning Strategies

1. **Constraint Checking**
   ```python
   # Don't explore if constraint violated
   if not satisfies_constraint(path, choice):
       continue  # Skip this choice
   ```

2. **Early Termination**
   ```python
   # Stop if already exceeds target
   if current_sum > target:
       return  # No point continuing
   ```

3. **Duplicate Avoidance**
   ```python
   # Skip duplicates in sorted input
   if i > start and nums[i] == nums[i-1]:
       continue
   ```

4. **Feasibility Check**
   ```python
   # Can't possibly reach target anymore
   if remaining < needed:
       return
   ```

5. **Optimization Bounds**
   ```python
   # Current solution can't beat best found
   if current_cost > best_cost:
       return
   ```

### Example: Combination Sum with Pruning

```python
def combination_sum(candidates, target):
    result = []
    candidates.sort()  # Enable pruning

    def backtrack(start, path, total):
        if total == target:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            # PRUNING: Stop if exceeded target
            if total + candidates[i] > target:
                break  # No point checking larger numbers

            path.append(candidates[i])
            backtrack(i, path, total + candidates[i])
            path.pop()

    backtrack(0, [], 0)
    return result
```

The `break` statement prunes entire subtrees, dramatically reducing the search space.

## Time Complexity Analysis

Backtracking time complexity depends on:
1. **Size of decision tree**: How many nodes to explore?
2. **Work per node**: How much work at each node?
3. **Pruning effectiveness**: How many branches can we skip?

### Common Complexities

| Problem | Time Complexity | Space | Notes |
|---------|----------------|-------|-------|
| Subsets | O(n * 2^n) | O(n) | 2^n subsets, O(n) to copy each |
| Permutations | O(n * n!) | O(n) | n! permutations, O(n) to copy |
| Combinations | O(k * C(n,k)) | O(k) | C(n,k) combinations of size k |
| N-Queens | O(n!) | O(n^2) | With pruning; O(n^n) without |
| Sudoku | O(9^m) | O(1) | m = empty cells, heavy pruning |
| Word Search | O(m*n * 4^L) | O(L) | L = word length, 4 directions |

### Why So Expensive?

- **Exponential search spaces**: Decision trees grow exponentially
- **No better alternative**: For problems requiring all solutions, must explore all
- **Pruning helps**: Can reduce constant factors significantly
- **Often necessary**: Some problems have no polynomial solution

## Common Backtracking Patterns

### 1. Subsets (Powerset)

Generate all subsets of a set.

```python
def subsets(nums):
    result = []

    def backtrack(start, path):
        # Every node is a valid subset
        result.append(path[:])

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # i+1: can't reuse elements
            path.pop()

    backtrack(0, [])
    return result
```

**Pattern**: Include/exclude decisions for each element.
**Time**: O(n * 2^n)

### 2. Permutations

Generate all orderings of elements.

```python
def permute(nums):
    result = []

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return

        for num in nums:
            if num in path:  # Skip used elements
                continue
            path.append(num)
            backtrack(path)
            path.pop()

    backtrack([])
    return result
```

**Pattern**: Try each unused element at each position.
**Time**: O(n * n!)

### 3. Combinations

Choose k elements from n elements.

```python
def combine(n, k):
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return

        # Pruning: need k-len(path) more elements
        # Must have at least that many remaining
        for i in range(start, n + 1):
            if n - i + 1 < k - len(path):
                break  # Not enough elements left

            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result
```

**Pattern**: Choose elements in sorted order to avoid duplicates.
**Time**: O(k * C(n,k))

### 4. Combination Sum

Find combinations that sum to target (elements can be reused).

```python
def combination_sum(candidates, target):
    result = []

    def backtrack(start, path, total):
        if total == target:
            result.append(path[:])
            return
        if total > target:
            return  # Exceeded target

        for i in range(start, len(candidates)):
            path.append(candidates[i])
            # i (not i+1): can reuse same element
            backtrack(i, path, total + candidates[i])
            path.pop()

    backtrack(0, [], 0)
    return result
```

**Pattern**: Track running sum, allow reuse.
**Time**: O(n^(target/min)) approximately

### 5. N-Queens

Place N queens on N×N board so none attack each other.

```python
def solve_n_queens(n):
    result = []
    board = [['.'] * n for _ in range(n)]
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row):
        if row == n:
            result.append([''.join(row) for row in board])
            return

        for col in range(n):
            # Check if position is under attack
            if col in cols or (row-col) in diag1 or (row+col) in diag2:
                continue

            # Place queen
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            # Remove queen
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result
```

**Pattern**: Place items row by row, check constraints.
**Time**: O(n!) with pruning

### 6. Grid/Matrix Search

Search for word in 2D grid.

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def backtrack(r, c, index):
        # Found complete word
        if index == len(word):
            return True

        # Out of bounds or wrong character
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != word[index]):
            return False

        # Mark as visited
        temp = board[r][c]
        board[r][c] = '#'

        # Explore 4 directions
        found = (backtrack(r+1, c, index+1) or
                 backtrack(r-1, c, index+1) or
                 backtrack(r, c+1, index+1) or
                 backtrack(r, c-1, index+1))

        # Restore cell
        board[r][c] = temp
        return found

    # Try starting from each cell
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

**Pattern**: Explore grid with direction choices, mark visited.
**Time**: O(m*n * 4^L)

## Backtracking vs Other Approaches

### Backtracking vs Dynamic Programming

| Backtracking | Dynamic Programming |
|--------------|---------------------|
| Explores all solutions | Finds optimal solution |
| Exponential time (usually) | Polynomial time (usually) |
| Uses DFS/recursion | Uses memoization/tabulation |
| Good for: all solutions | Good for: one best solution |
| Example: All subsets | Example: Longest subsequence |

**Can sometimes combine**: Use DP to optimize backtracking.

### Backtracking vs Greedy

| Backtracking | Greedy |
|--------------|---------|
| Explores multiple paths | Makes one choice per step |
| Guaranteed correct | May not be optimal |
| Slower but complete | Fast but incomplete |
| Example: N-Queens | Example: Activity selection |

### Backtracking vs Branch and Bound

| Backtracking | Branch and Bound |
|--------------|------------------|
| Decision problems | Optimization problems |
| Find feasible solutions | Find best solution |
| Prunes invalid branches | Prunes suboptimal branches |
| Example: Sudoku | Example: TSP optimization |

## Common Pitfalls and Tips

### Pitfall 1: Forgetting to Copy

```python
# WRONG: Adds reference, all results are same
result.append(path)

# RIGHT: Adds copy of current state
result.append(path[:])  # or path.copy()
```

### Pitfall 2: Not Backtracking

```python
# WRONG: State persists
path.append(choice)
backtrack(path)
# Forgot to remove choice!

# RIGHT: Undo the choice
path.append(choice)
backtrack(path)
path.pop()  # Backtrack!
```

### Pitfall 3: Wrong Loop Range

```python
# For combinations (no reuse, order doesn't matter)
backtrack(i + 1, path)  # Next element

# For combination sum (reuse allowed)
backtrack(i, path)  # Same element can be reused

# For permutations (use all, check if used)
if num not in path:  # Check usage
```

### Pitfall 4: Missing Base Case

```python
# WRONG: Infinite recursion
def backtrack(path):
    for choice in choices:
        backtrack(path + [choice])

# RIGHT: Has termination condition
def backtrack(path):
    if len(path) == target_length:
        result.append(path[:])
        return  # Stop here
    for choice in choices:
        backtrack(path + [choice])
```

### Pitfall 5: Inefficient Pruning Check

```python
# WRONG: O(n) check per recursion
if choice in path:  # List lookup is O(n)
    continue

# RIGHT: Use set for O(1) check
used = set(path)
if choice in used:  # Set lookup is O(1)
    continue
```

## Tips for Success

1. **Draw the decision tree**: Visualize the problem before coding

2. **Identify the choices**: What decisions do we make at each step?

3. **Define the state**: What information do we need to pass down?

4. **Find base cases**: When is a solution complete? When should we stop?

5. **Look for pruning opportunities**: What branches can we skip early?

6. **Use helper data structures**: Sets for O(1) lookups, etc.

7. **Test with small examples**: Try n=2 or n=3 first

8. **Watch for duplicates**: Sort input and skip consecutive duplicates

9. **Consider memoization**: Can we cache repeated subproblems?

10. **Profile your solution**: Is pruning working? Are you exploring too much?

## Interview Strategy

When faced with a backtracking problem:

1. **Recognize the pattern**
   - "All possible solutions"
   - Constraint satisfaction
   - Generate combinations/permutations

2. **Clarify requirements**
   - Return all solutions or just one?
   - Any constraints on the solution?
   - Can elements be reused?
   - Does order matter?

3. **Start with brute force**
   - Explain the exponential approach
   - Draw a small decision tree

4. **Add pruning**
   - Identify impossible branches
   - Add checks to skip them early

5. **Optimize data structures**
   - Use sets instead of lists where appropriate
   - Consider arrays for better cache locality

6. **Analyze complexity**
   - Size of decision tree
   - Work per node
   - Impact of pruning

7. **Code carefully**
   - Follow the template
   - Remember to copy results
   - Don't forget to backtrack

## Practice Problems

### Easy
- Subsets (78)
- Combinations (77)
- Letter Case Permutation (784)

### Medium
- Permutations (46)
- Combination Sum (39)
- Generate Parentheses (22)
- Word Search (79)
- Palindrome Partitioning (131)
- Subsets II (90) - with duplicates

### Hard
- N-Queens (51)
- N-Queens II (52)
- Sudoku Solver (37)
- Word Search II (212)
- Regular Expression Matching (10)

## Key Takeaways

1. **Backtracking explores all possibilities** systematically
2. **Follow the template**: Choose → Explore → Unchoose
3. **Pruning is critical** for practical performance
4. **Time complexity is usually exponential** - that's okay for these problems
5. **Draw the decision tree** to understand the problem
6. **Remember to copy results** when adding to result list
7. **Use appropriate data structures** (sets for lookups, etc.)

Backtracking is powerful but expensive. Use it when you truly need to explore all possibilities or when no better approach exists.

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems with detailed explanations!
