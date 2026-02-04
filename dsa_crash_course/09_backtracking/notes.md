# Backtracking - Quick Reference

## Core Template

```python
def backtrack(path, choices, result):
    # BASE CASE: Complete solution?
    if is_valid_solution(path):
        result.append(path[:])  # Must copy!
        return

    # RECURSIVE CASE: Try each choice
    for choice in choices:
        # 1. CHOOSE
        path.append(choice)

        # 2. EXPLORE
        backtrack(path, new_choices, result)

        # 3. UNCHOOSE (backtrack)
        path.pop()

# Usage
result = []
backtrack([], initial_choices, result)
return result
```

## Three Steps: Remember "CEU"

1. **CHOOSE**: Add choice to path, mark as used
2. **EXPLORE**: Recurse with new state
3. **UNCHOOSE**: Remove choice, unmark

## Complexity Cheat Sheet

| Problem | Time | Space | Notes |
|---------|------|-------|-------|
| Subsets | O(n * 2^n) | O(n) | 2^n subsets |
| Permutations | O(n * n!) | O(n) | n! orderings |
| Combinations C(n,k) | O(k * C(n,k)) | O(k) | Choose k from n |
| Combination Sum | O(n^(T/M)) | O(T/M) | T=target, M=min |
| N-Queens | O(n!) | O(n^2) | With pruning |
| Word Search | O(m*n * 4^L) | O(L) | L=word length |

## Pattern Recognition

| Keywords | Pattern | Reuse? | Order? |
|----------|---------|--------|--------|
| "all subsets" | Subsets | No | No |
| "all permutations" | Permutations | No | Yes |
| "choose k from n" | Combinations | No | No |
| "sum to target" | Combination Sum | Maybe | No |
| "place with constraints" | N-Queens | No | Yes |
| "find in grid" | Grid Search | No | Yes |

## Common Patterns

### 1. Subsets (Include/Exclude)

```python
def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])  # Every node is valid

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # i+1: no reuse
            path.pop()

    backtrack(0, [])
    return result
```

**Key**: Every node is a subset. Start index prevents duplicates.

### 2. Permutations (Try Each Unused)

```python
def permute(nums):
    result = []

    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i, num in enumerate(nums):
            if used[i]:
                continue

            used[i] = True
            path.append(num)
            backtrack(path, used)
            path.pop()
            used[i] = False

    backtrack([], [False] * len(nums))
    return result
```

**Key**: Track which elements used. Try all positions.

### 3. Combinations (Start Index)

```python
def combine(n, k):
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return

        # Pruning: need k-len(path) more elements
        for i in range(start, n + 1):
            if n - i + 1 < k - len(path):
                break  # Not enough left

            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result
```

**Key**: Start index for ordering. Prune if insufficient elements remain.

### 4. Combination Sum (With Reuse)

```python
def combination_sum(candidates, target):
    result = []
    candidates.sort()  # Enable pruning

    def backtrack(start, path, total):
        if total == target:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            if total + candidates[i] > target:
                break  # Pruning: exceeds target

            path.append(candidates[i])
            backtrack(i, path, total + candidates[i])  # i: allow reuse
            path.pop()

    backtrack(0, [], 0)
    return result
```

**Key**: Pass `i` (not `i+1`) to allow reuse. Break when sum exceeds target.

### 5. N-Queens (Constraint Checking)

```python
def solve_n_queens(n):
    result = []
    board = [['.'] * n for _ in range(n)]
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return

        for col in range(n):
            # Check constraints
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

**Key**: Sets for O(1) constraint checking. Diagonals: `row±col`.

### 6. Grid Search (4 Directions)

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def backtrack(r, c, index):
        if index == len(word):
            return True

        if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != word[index]):
            return False

        # Mark visited
        temp = board[r][c]
        board[r][c] = '#'

        # Try 4 directions
        found = (backtrack(r+1, c, index+1) or
                 backtrack(r-1, c, index+1) or
                 backtrack(r, c+1, index+1) or
                 backtrack(r, c-1, index+1))

        # Restore
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

**Key**: Modify grid to mark visited. Restore after recursion.

## Pruning Strategies

### 1. Constraint Violation
```python
if not satisfies_constraint(path, choice):
    continue  # Skip this branch
```

### 2. Early Termination
```python
if current_sum > target:
    return  # Can't succeed from here
```

### 3. Skip Duplicates
```python
# After sorting
if i > start and nums[i] == nums[i-1]:
    continue  # Skip duplicate elements
```

### 4. Feasibility Check
```python
# Need k more, have n-i remaining
if n - i + 1 < k - len(path):
    break  # Insufficient elements
```

### 5. Optimization Bound
```python
if current_cost > best_cost:
    return  # Can't beat current best
```

## Common Pitfalls

### 1. Forget to Copy
```python
# WRONG
result.append(path)  # Reference!

# RIGHT
result.append(path[:])  # Copy
result.append(path.copy())  # Also works
```

### 2. Forget to Backtrack
```python
# WRONG
path.append(choice)
backtrack(...)
# Missing path.pop()!

# RIGHT
path.append(choice)
backtrack(...)
path.pop()  # Restore state
```

### 3. Wrong Index
```python
# Combinations (no reuse, no order)
backtrack(i + 1, ...)

# Combination sum (reuse allowed)
backtrack(i, ...)

# Permutations (all positions)
backtrack(...)  # No index needed
```

### 4. Inefficient Lookup
```python
# WRONG - O(n) per check
if choice in path:

# RIGHT - O(1) per check
used = set()
if choice in used:
```

## Decision Tree Patterns

### Include/Exclude (Subsets)
```
         []
       /    \
    [1]      []
   /  \     /  \
[1,2] [1] [2]  []
```

### Try Each Position (Permutations)
```
          []
      /   |   \
    [1]  [2]  [3]
    / \  / \  / \
  [1,2][1,3]...
```

### Choose K Elements (Combinations)
```
Level 0:    []
Level 1:    [1] [2] [3]
Level 2:    [1,2] [1,3] [2,3]
```

## Quick Decision Guide

**Q: Return all solutions?**
- Yes → Backtracking likely needed

**Q: Can elements be reused?**
- Yes → Pass same index `i`
- No → Pass next index `i+1`

**Q: Does order matter?**
- Yes → Permutation pattern
- No → Use start index

**Q: Fixed length k?**
- Yes → Check `len(path) == k`
- No → Check other conditions

**Q: Have constraints?**
- Yes → Add pruning checks
- No → Still check for early termination

## When NOT to Use Backtracking

- **Need only one solution** → BFS, DFS, Greedy
- **Optimization problem** → Dynamic Programming
- **Large input** → Backtracking may be too slow
- **Known polynomial algorithm** → Use that instead

## Optimization Checklist

- [ ] Sort input if helpful for pruning
- [ ] Use sets for O(1) lookups
- [ ] Add early termination checks
- [ ] Skip duplicate elements
- [ ] Check feasibility before recursing
- [ ] Pass minimal state in recursion
- [ ] Consider memoization for repeated subproblems

## Testing Strategy

1. **Empty/base cases**: [], n=0
2. **Single element**: [1], n=1
3. **Small example**: [1,2], n=2
4. **Duplicates**: [1,1,2]
5. **All same**: [1,1,1]
6. **Large valid input**: Verify performance

## Interview Template

```python
def solve(input):
    result = []

    def backtrack(state_params):
        # 1. BASE CASE
        if is_complete(state):
            result.append(build_solution(state))
            return

        # 2. PRUNING (optional but important)
        if should_prune(state):
            return

        # 3. ITERATION
        for choice in get_choices(state):
            # CHOOSE
            make_choice(state, choice)

            # EXPLORE
            backtrack(updated_state)

            # UNCHOOSE
            undo_choice(state, choice)

    backtrack(initial_state)
    return result
```

## Key Formulas

**Subsets**: 2^n total subsets
**Permutations**: n! orderings
**Combinations**: C(n,k) = n! / (k!(n-k)!)
**Diagonals**:
- Top-left to bottom-right: `row - col`
- Top-right to bottom-left: `row + col`

## Quick Wins

1. **Sort first** if it enables pruning
2. **Use sets** for constant-time constraint checks
3. **Break early** when sum/cost exceeds target
4. **Skip duplicates** with sorted input
5. **Visualize** with small decision tree first
