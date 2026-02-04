# Binary Search - Quick Reference

## Complexity Cheat Sheet

### Time Complexity
- **Classic binary search**: O(log n)
- **Find first/last occurrence**: O(log n)
- **Search rotated array**: O(log n)
- **Binary search on answer space**: O(log(range) × C) where C is condition check cost

### Space Complexity
- **Iterative**: O(1)
- **Recursive**: O(log n) due to call stack

### Why O(log n)?
- Each iteration halves the search space
- n → n/2 → n/4 → ... → 1
- Number of steps = log₂(n)
- Examples: n=1000 → 10 steps, n=1,000,000 → 20 steps

## Binary Search Templates

### Template 1: Exact Search
Find exact target value.

```python
left, right = 0, len(arr) - 1
while left <= right:  # Note: <=
    mid = left + (right - left) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
return -1
```

**When to use:** Finding exact value in sorted array.

**Key points:**
- Initialize: `right = len(arr) - 1`
- Loop: `left <= right`
- Update: `left = mid + 1` or `right = mid - 1`

### Template 2: Leftmost Boundary
Find first occurrence or leftmost valid position.

```python
left, right = 0, len(arr)  # Note: len(arr), not len(arr)-1
while left < right:  # Note: <
    mid = left + (right - left) // 2
    if arr[mid] < target:
        left = mid + 1
    else:
        right = mid  # Don't exclude mid
return left
```

**When to use:**
- First occurrence of target
- Insert position
- Leftmost position where condition is true

**Key points:**
- Initialize: `right = len(arr)`
- Loop: `left < right`
- Update: Keep `mid` in valid range, `right = mid`

### Template 3: Rightmost Boundary
Find last occurrence or rightmost valid position.

```python
left, right = -1, len(arr) - 1
while left < right:
    mid = left + (right - left + 1) // 2  # Note: +1
    if arr[mid] <= target:
        left = mid
    else:
        right = mid - 1
return left
```

**When to use:**
- Last occurrence of target
- Rightmost position where condition is true

**Key points:**
- Initialize: `left = -1` or `left = 0`
- Loop: `left < right`
- Mid calculation: Add 1 to avoid infinite loop
- Update: `left = mid`

### Template 4: Minimize Answer
Find minimum value satisfying condition.

```python
left, right = min_val, max_val
while left < right:
    mid = left + (right - left) // 2
    if feasible(mid):
        right = mid  # Try smaller
    else:
        left = mid + 1  # Need larger
return left
```

**When to use:** Find minimum value where condition holds.

### Template 5: Maximize Answer
Find maximum value satisfying condition.

```python
left, right = min_val, max_val
while left < right:
    mid = left + (right - left + 1) // 2  # Note: +1
    if feasible(mid):
        left = mid  # Try larger
    else:
        right = mid - 1  # Need smaller
return left
```

**When to use:** Find maximum value where condition holds.

## Common Patterns

### 1. Classic Binary Search
```python
# Find target in sorted array
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### 2. Find First Occurrence
```python
# Find leftmost occurrence of target
def find_first(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Keep searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

### 3. Find Last Occurrence
```python
# Find rightmost occurrence of target
def find_last(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            result = mid
            left = mid + 1  # Keep searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

### 4. Search in Rotated Array
```python
# Key: At least one half is always sorted
def search_rotated(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        # Determine which half is sorted
        if arr[left] <= arr[mid]:
            # Left half sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

### 5. Binary Search on Answer Space
```python
# Template for "find minimum X such that condition(X) is true"
def binary_search_answer(min_val, max_val):
    left, right = min_val, max_val
    while left < right:
        mid = left + (right - left) // 2
        if condition(mid):
            right = mid  # Try smaller
        else:
            left = mid + 1  # Need larger
    return left
```

## Problem Recognition

### Array Search Problems
| Clue | Pattern |
|------|---------|
| "Find target in sorted array" | Classic binary search |
| "Find first occurrence" | Leftmost boundary |
| "Find last occurrence" | Rightmost boundary |
| "Find insert position" | Leftmost boundary |
| "Rotated sorted array" | Modified binary search |
| "Find peak element" | Modified binary search |

### Answer Space Problems
| Clue | Pattern |
|------|---------|
| "Minimum speed/capacity to..." | Binary search on answer (minimize) |
| "Maximum value that..." | Binary search on answer (maximize) |
| "Can you do X in Y time?" | Binary search on answer |
| "Split array to minimize maximum" | Binary search + greedy |
| "Kth smallest/largest" | Binary search on value |

### Keywords to Watch For
- "Sorted array"
- "O(log n)" requirement
- "Minimum X such that..."
- "Maximum X such that..."
- "First occurrence"
- "Last occurrence"
- "Rotated"
- "Find peak"

## Common Pitfalls

### 1. Infinite Loops
```python
# WRONG: Can loop forever
while left < right:
    mid = left + (right - left) // 2
    if condition:
        left = mid  # BUG: left never changes when left == mid

# FIX: Add 1 to mid or ensure left/right always change
while left < right:
    mid = left + (right - left + 1) // 2
    if condition:
        left = mid
```

### 2. Off-by-One Errors
```python
# For exact search: use <=
while left <= right:  # CORRECT

# For boundary search: use <
while left < right:  # CORRECT

# Initialize right correctly
right = len(arr) - 1  # For exact search
right = len(arr)      # For boundary search
```

### 3. Integer Overflow
```python
# In Java/C++, avoid:
mid = (left + right) / 2  # Can overflow

# Use instead:
mid = left + (right - left) / 2  # Safe
```

### 4. Wrong Boundary Updates
```python
# When you want to keep mid:
right = mid  # NOT mid - 1

# When you want to exclude mid:
left = mid + 1  # NOT mid
right = mid - 1  # NOT mid
```

## Edge Cases to Test

1. **Empty array**: `[]`
2. **Single element**: `[x]`
3. **Two elements**: `[x, y]`
4. **Target not present**: Returns -1 or insert position
5. **Target at boundaries**: First or last element
6. **All elements equal**: `[5, 5, 5, 5]`
7. **Duplicates**: Multiple occurrences of target
8. **Minimum value**: `[min_int, ...]`
9. **Maximum value**: `[..., max_int]`

## Debugging Checklist

If your binary search isn't working:

1. **Check initialization**
   - Is `right` set correctly? (`len(arr) - 1` vs `len(arr)`)
   - Is `left` starting at right value?

2. **Check loop condition**
   - Use `<=` for exact search
   - Use `<` for boundary search

3. **Check mid calculation**
   - Add `+ 1` when doing `left = mid` to avoid infinite loop

4. **Check boundary updates**
   - Do they always shrink the search space?
   - Are you including/excluding `mid` correctly?

5. **Trace through examples**
   - Target found
   - Target not found
   - Target at edges
   - Single element

## Interview Template

```python
def solve_with_binary_search(arr, target):
    # 1. Handle edge cases
    if not arr:
        return -1  # or appropriate default

    # 2. Initialize boundaries
    left, right = 0, len(arr) - 1

    # 3. Binary search loop
    while left <= right:  # or left < right
        mid = left + (right - left) // 2

        # 4. Check condition
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # 5. Return result
    return -1
```

## Python Tips

### Ceiling Division
```python
# For "how many hours to eat pile of size p at speed s?"
import math
hours = math.ceil(p / s)
# Or without import:
hours = (p + s - 1) // s
```

### Bisect Module
```python
import bisect

# Find leftmost insertion point
bisect.bisect_left(arr, target)

# Find rightmost insertion point
bisect.bisect_right(arr, target)

# Insert and keep sorted
bisect.insort(arr, target)
```

## Quick Decision Tree

```
Is array sorted?
├─ Yes → Use binary search
│  ├─ Find exact value? → Template 1 (exact search)
│  ├─ Find first occurrence? → Template 2 (leftmost)
│  ├─ Find last occurrence? → Template 3 (rightmost)
│  └─ Rotated? → Modified binary search
│
└─ No → Can you binary search on answer space?
   ├─ Find "minimum X that works"? → Template 4 (minimize)
   ├─ Find "maximum X that works"? → Template 5 (maximize)
   └─ Otherwise → Consider other approaches
```

## Time Complexity Goals

- **O(log n)**: Binary search on array
- **O(n log n)**: Sort first, then binary search
- **O(log(range) × n)**: Binary search on answer space, O(n) to check each answer
- **O((log n)²)**: Binary search with binary search in condition check

## Related Patterns

- **Two Pointers**: For sorted arrays, sometimes alternative to binary search
- **Divide and Conquer**: Binary search is a D&C algorithm
- **Greedy**: Often combined with binary search on answer space
- **Sorting**: Prerequisite for many binary search problems

## Common Mistakes

1. Using `left < right` when you need `left <= right`
2. Forgetting to update `left` or `right`
3. Not handling the case when target isn't found
4. Using wrong mid calculation causing infinite loop
5. Not considering duplicates
6. Forgetting edge cases (empty array, single element)
7. Wrong boundary initialization

## Mental Model

Think of binary search as:
1. **Search space**: Range of possible answers
2. **Invariant**: Answer (if exists) is always in [left, right]
3. **Progress**: Each step eliminates half the space
4. **Termination**: When left and right meet

## Practice Tips

1. Master Template 1 (exact search) first
2. Understand why each boundary update works
3. Practice with duplicates
4. Try both iterative and recursive versions
5. Solve rotated array problems
6. Graduate to answer space problems
7. Combine with other techniques (greedy, DP)
