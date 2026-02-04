# Binary Search

Binary search is one of the most fundamental and powerful algorithms in computer science. It's the foundation for efficient searching and appears frequently in coding interviews. Mastering binary search requires understanding not just the basic algorithm, but also how to apply it to various problem types.

## 📖 What is Binary Search?

**Binary search** is an efficient algorithm for finding a target value within a sorted array. It works by repeatedly dividing the search interval in half, eliminating half of the remaining elements at each step.

### The Core Idea

Think of binary search like finding a word in a dictionary:
1. Open to the middle page
2. If your word comes before that page, search the first half
3. If your word comes after that page, search the second half
4. Repeat until you find the word

This "divide and conquer" approach is what makes binary search so efficient.

### Key Requirements

Binary search requires:
- **Sorted data** - The array must be sorted (or have some monotonic property)
- **Random access** - Ability to access any element in O(1) time
- **Comparable elements** - Elements must have a defined ordering

## 🎯 Classical Binary Search

The classical binary search finds an exact value in a sorted array.

### Basic Template

```python
def binary_search(arr, target):
    """
    Classic binary search - find exact target in sorted array.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow

        if arr[mid] == target:
            return mid  # Found it!
        elif arr[mid] < target:
            left = mid + 1  # Search right half
        else:
            right = mid - 1  # Search left half

    return -1  # Not found
```

### Why `left + (right - left) // 2`?

Instead of `(left + right) // 2`, we use `left + (right - left) // 2` to avoid integer overflow in languages with fixed integer sizes (though not an issue in Python).

## 🔄 Binary Search Variants

Binary search can be adapted to find different things:

### 1. Find First Occurrence (Left Boundary)

Find the leftmost position where target appears:

```python
def find_first(arr, target):
    """
    Find the first (leftmost) occurrence of target.
    Returns the index, or -1 if not found.

    Example: [1, 2, 2, 2, 3], target=2 -> returns 1
    """
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid      # Found it, but keep searching left
            right = mid - 1   # Continue searching left side
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

### 2. Find Last Occurrence (Right Boundary)

Find the rightmost position where target appears:

```python
def find_last(arr, target):
    """
    Find the last (rightmost) occurrence of target.
    Returns the index, or -1 if not found.

    Example: [1, 2, 2, 2, 3], target=2 -> returns 3
    """
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid      # Found it, but keep searching right
            left = mid + 1    # Continue searching right side
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

### 3. Find Insert Position

Find where to insert target to maintain sorted order:

```python
def find_insert_position(arr, target):
    """
    Find the position where target should be inserted to keep array sorted.
    This is the leftmost position where arr[i] >= target.

    Example: [1, 3, 5, 7], target=4 -> returns 2
    """
    left, right = 0, len(arr)  # Note: right = len(arr), not len(arr)-1

    while left < right:  # Note: left < right, not left <= right
        mid = left + (right - left) // 2

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid  # Don't exclude mid

    return left
```

## 🌀 Rotated Array Problems

A rotated sorted array is created by rotating a sorted array at some pivot point.

Example: `[1, 2, 3, 4, 5]` rotated at index 2 becomes `[3, 4, 5, 1, 2]`

### Search in Rotated Array

```python
def search_rotated(arr, target):
    """
    Search in rotated sorted array.

    Key insight: At least one half is always sorted.
    - If left half is sorted, check if target is in left half
    - Otherwise, check if target is in right half
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid

        # Determine which half is sorted
        if arr[left] <= arr[mid]:
            # Left half is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1  # Target in left half
            else:
                left = mid + 1   # Target in right half
        else:
            # Right half is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1   # Target in right half
            else:
                right = mid - 1  # Target in left half

    return -1
```

### Find Minimum in Rotated Array

```python
def find_min_rotated(arr):
    """
    Find minimum element in rotated sorted array.

    Key insight: The minimum is where the rotation happened.
    If arr[mid] > arr[right], minimum is in right half.
    Otherwise, minimum is in left half (including mid).
    """
    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] > arr[right]:
            # Minimum is in right half
            left = mid + 1
        else:
            # Minimum is in left half (including mid)
            right = mid

    return arr[left]
```

## 🎯 Binary Search on Answer Space

One of the most powerful applications of binary search is searching not in an array, but in the **space of possible answers**.

### When to Use

Use this technique when:
- You need to find the minimum/maximum value that satisfies a condition
- You can check if a value satisfies the condition in reasonable time
- The answer space has a monotonic property (if x works, then all smaller/larger values work)

### Template

```python
def binary_search_answer(condition_func, min_val, max_val):
    """
    Binary search on answer space.

    Find the minimum/maximum value in [min_val, max_val] that satisfies
    a condition.

    Args:
        condition_func: Function that returns True if value satisfies condition
        min_val: Minimum possible answer
        max_val: Maximum possible answer
    """
    left, right = min_val, max_val
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if condition_func(mid):
            result = mid      # Found a valid answer
            right = mid - 1   # Try to find smaller (for minimum)
            # For maximum, use: left = mid + 1
        else:
            left = mid + 1    # Need larger value
            # For maximum, use: right = mid - 1

    return result
```

### Example: Minimum Speed Problem

```python
def min_eating_speed(piles, hours):
    """
    Koko Eating Bananas problem:
    Find minimum eating speed to finish all piles within hours.

    Answer space: [1, max(piles)]
    Condition: Can finish all piles at this speed within hours?
    """
    def can_finish(speed):
        """Check if can eat all bananas at given speed within hours."""
        time_needed = 0
        for pile in piles:
            time_needed += (pile + speed - 1) // speed  # Ceiling division
        return time_needed <= hours

    left, right = 1, max(piles)

    while left < right:
        mid = left + (right - left) // 2

        if can_finish(mid):
            right = mid  # This speed works, try slower
        else:
            left = mid + 1  # Too slow, need faster

    return left
```

## ⏱️ Time and Space Complexity

### Classical Binary Search

| Operation | Time | Space |
|-----------|------|-------|
| Search exact value | O(log n) | O(1) |
| Find first/last occurrence | O(log n) | O(1) |
| Find insert position | O(log n) | O(1) |

### Why O(log n)?

At each step, we eliminate half the search space:
- n elements → n/2 → n/4 → n/8 → ... → 1
- Number of steps: log₂(n)

Examples:
- n = 1,000: ~10 comparisons
- n = 1,000,000: ~20 comparisons
- n = 1,000,000,000: ~30 comparisons

### Binary Search on Answer Space

| Operation | Time | Space |
|-----------|------|-------|
| Search answer space | O(log(range) × C) | O(1) |

Where:
- range = max_answer - min_answer
- C = cost of checking if a value works

## 🚨 Common Pitfalls

### 1. Infinite Loops

**Problem:** Wrong boundary updates can cause infinite loops.

```python
# WRONG: Can cause infinite loop
while left < right:
    mid = left + (right - left) // 2
    if arr[mid] < target:
        left = mid  # BUG: left might never change
    else:
        right = mid - 1

# CORRECT:
while left < right:
    mid = left + (right - left) // 2
    if arr[mid] < target:
        left = mid + 1  # Always make progress
    else:
        right = mid
```

**Rule:** Always ensure the search space shrinks.

### 2. Off-by-One Errors

**Problem:** Wrong loop condition or boundary initialization.

```python
# Finding exact value:
left, right = 0, len(arr) - 1
while left <= right:  # Note: <=
    # ...

# Finding insert position:
left, right = 0, len(arr)  # Note: len(arr), not len(arr)-1
while left < right:  # Note: <
    # ...
```

### 3. Integer Overflow

**Problem:** `(left + right) // 2` can overflow in some languages.

```python
# Risky (not in Python, but in Java/C++):
mid = (left + right) // 2

# Safe:
mid = left + (right - left) // 2
```

### 4. Wrong Comparison

**Problem:** Using wrong comparison operator.

```python
# When finding leftmost:
if arr[mid] >= target:  # Include equal
    right = mid - 1

# When finding rightmost:
if arr[mid] <= target:  # Include equal
    left = mid + 1
```

## 📋 Binary Search Templates

### Template 1: Exact Search

Use when: Finding exact target value.

```python
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

### Template 2: Leftmost Boundary

Use when: Finding first occurrence or leftmost position satisfying condition.

```python
left, right = 0, len(arr)
while left < right:
    mid = left + (right - left) // 2
    if arr[mid] < target:
        left = mid + 1
    else:
        right = mid
return left
```

### Template 3: Rightmost Boundary

Use when: Finding last occurrence or rightmost position satisfying condition.

```python
left, right = -1, len(arr) - 1
while left < right:
    mid = left + (right - left + 1) // 2  # Note: +1 to avoid infinite loop
    if arr[mid] <= target:
        left = mid
    else:
        right = mid - 1
return left
```

### Template 4: Minimize/Maximize

Use when: Finding minimum/maximum value satisfying condition.

```python
# Minimize
left, right = min_val, max_val
while left < right:
    mid = left + (right - left) // 2
    if feasible(mid):
        right = mid  # Try smaller
    else:
        left = mid + 1
return left

# Maximize
left, right = min_val, max_val
while left < right:
    mid = left + (right - left + 1) // 2
    if feasible(mid):
        left = mid  # Try larger
    else:
        right = mid - 1
return left
```

## 🎓 Problem Recognition

### Signs You Should Use Binary Search

1. **Sorted array** - Given explicitly or can be sorted
2. **Find target** - Search for a specific value
3. **"First/last occurrence"** - Boundary problems
4. **Rotated sorted array** - Modified sorted array
5. **"Minimum/maximum value that satisfies"** - Answer space search
6. **Time limit is tight** - Need O(log n) instead of O(n)
7. **Monotonic condition** - If x works, all smaller/larger x work

### Common Problem Types

**Array Search:**
- Find exact value
- Find first/last occurrence
- Find insert position
- Search in rotated array
- Find peak element
- Find missing number

**Answer Space Search:**
- Minimum capacity/speed/time to meet condition
- Maximum value under constraint
- Kth smallest/largest element
- Split array problems
- Minimum maximum subarray sum

## 💡 Advanced Patterns

### Binary Search + Greedy

Many problems combine binary search on answer space with greedy checking:

```python
def split_array_minimize_sum(arr, m):
    """
    Split array into m subarrays to minimize largest sum.

    Binary search on answer: What's the minimum possible largest sum?
    Greedy check: Can we split array such that no subarray exceeds this sum?
    """
    def can_split(max_sum):
        """Greedy: Try to split with max_sum limit."""
        splits, current_sum = 1, 0
        for num in arr:
            if current_sum + num > max_sum:
                splits += 1
                current_sum = num
                if splits > m:
                    return False
            else:
                current_sum += num
        return True

    left, right = max(arr), sum(arr)

    while left < right:
        mid = left + (right - left) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

### Binary Search in 2D

Search in sorted 2D matrix:

```python
def search_matrix(matrix, target):
    """
    Search in row-wise and column-wise sorted matrix.
    Treat 2D matrix as 1D sorted array.
    """
    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1

    while left <= right:
        mid = left + (right - left) // 2
        # Convert 1D index to 2D
        row, col = mid // cols, mid % cols
        mid_val = matrix[row][col]

        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

### Binary Search with Floating Point

Some problems require binary search on continuous values:

```python
def sqrt_binary_search(x, precision=1e-6):
    """
    Find square root using binary search.
    Works with floating point numbers.
    """
    if x < 1:
        left, right = x, 1
    else:
        left, right = 0, x

    while right - left > precision:
        mid = (left + right) / 2
        if mid * mid < x:
            left = mid
        else:
            right = mid

    return (left + right) / 2
```

## 🔧 Implementation Tips

### 1. Choose the Right Template

Different boundary conditions for different problems:
- Exact search: `left <= right`, return when found
- Boundary search: `left < right`, converge to answer

### 2. Test Edge Cases

Always test:
- Empty array
- Single element
- Two elements
- Target not in array
- Target at boundaries
- All elements equal
- Duplicates

### 3. Verify Invariants

After each iteration, verify:
- Search space is shrinking
- Answer (if exists) is in [left, right]
- Loop will terminate

### 4. Debug Systematically

If stuck in infinite loop:
1. Check loop condition
2. Check mid calculation
3. Verify left/right updates always change
4. Trace through small example

## 📊 Comparison with Linear Search

| Aspect | Linear Search | Binary Search |
|--------|--------------|---------------|
| Time | O(n) | O(log n) |
| Space | O(1) | O(1) |
| Requirement | None | Sorted data |
| Best for | Small data, unsorted | Large data, sorted |
| Simplicity | Very simple | More complex |

**When to use each:**
- Linear search: Small arrays (< 100 elements), unsorted data
- Binary search: Large arrays, sorted data, or when you can use answer space

## 🎯 Interview Strategy

### 1. Clarify the Problem
- Is the array sorted?
- Can there be duplicates?
- What should I return if not found?
- Any constraints on array size?

### 2. Identify the Pattern
- Exact search vs boundary search?
- Array search vs answer space search?
- Any special properties (rotated, 2D, etc.)?

### 3. Choose the Template
- Use appropriate template for the problem type
- Don't try to memorize all variants, understand the pattern

### 4. Handle Edge Cases
- Empty array
- Single/two elements
- Target at boundaries
- All elements same

### 5. Test Thoroughly
Walk through examples:
- Target found
- Target not found
- Target at edges
- Small arrays

## 📚 LeetCode Problem Categories

### Easy
- Binary Search (Classic)
- Search Insert Position
- First Bad Version
- Valid Perfect Square
- Sqrt(x)

### Medium
- Find First and Last Position of Element
- Search in Rotated Sorted Array
- Find Minimum in Rotated Sorted Array
- Find Peak Element
- Koko Eating Bananas
- Capacity To Ship Packages
- Minimum Size Subarray Sum

### Hard
- Median of Two Sorted Arrays
- Split Array Largest Sum
- Minimize Max Distance to Gas Station
- Find K-th Smallest Pair Distance

## 🔗 Related Topics

- **Sorting** - Binary search requires sorted data
- **Divide and Conquer** - Binary search is a classic D&C algorithm
- **Two Pointers** - Often used together
- **Trees** - Binary Search Trees use similar logic
- **Dynamic Programming** - Can optimize with binary search

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems!
