# Arrays and Strings - Quick Reference

## Complexity Cheat Sheet

### Array Operations
- **Access**: O(1)
- **Search**: O(n) unsorted, O(log n) sorted
- **Insert/Delete at end**: O(1) amortized
- **Insert/Delete at middle**: O(n)
- **Space**: O(n)

### String Operations
- **Access**: O(1)
- **Concatenation**: O(n+m) - creates new string
- **Slice**: O(k) where k is slice length
- **Split**: O(n)
- **Join**: O(n) - much better than repeated concat

## Common Patterns

### 1. Two Pointers
```python
# Opposite direction (palindrome, sorted array pairs)
left, right = 0, len(arr) - 1
while left < right:
    # process arr[left] and arr[right]
    left += 1
    right -= 1

# Same direction (remove duplicates, partition)
slow = 0
for fast in range(len(arr)):
    if condition:
        arr[slow] = arr[fast]
        slow += 1
```

### 2. Sliding Window
```python
# Fixed size window
window_sum = sum(arr[:k])
for i in range(k, len(arr)):
    window_sum += arr[i] - arr[i-k]

# Variable size window
left = 0
for right in range(len(arr)):
    # Add arr[right] to window
    while window_invalid:
        # Remove arr[left] from window
        left += 1
    # Update result with current window
```

### 3. Prefix Sum
```python
# Build: O(n), Query: O(1)
prefix = [0]
for num in arr:
    prefix.append(prefix[-1] + num)

# Sum of arr[i:j+1]
range_sum = prefix[j+1] - prefix[i]
```

### 4. String Builder
```python
# Build string efficiently
result = []
for item in items:
    result.append(str(item))
return ''.join(result)
```

### 5. Character Frequency
```python
# Using array (for lowercase letters)
freq = [0] * 26
for char in s:
    freq[ord(char) - ord('a')] += 1

# Using dict (for any characters)
from collections import Counter
freq = Counter(s)
```

## Python-Specific Tricks

### List Operations
```python
# Reverse
arr[::-1]

# Copy
arr[:]  or  arr.copy()

# Sort
sorted(arr)  # new list
arr.sort()   # in-place

# Comprehensions
[x*2 for x in arr if x > 0]

# Enumerate
for i, val in enumerate(arr):
    pass

# Zip (pair elements)
for a, b in zip(arr1, arr2):
    pass
```

### String Operations
```python
# Check
s.isalnum()  # alphanumeric
s.isalpha()  # letters only
s.isdigit()  # digits only
s.islower()  # lowercase
s.isupper()  # uppercase

# Transform
s.lower()
s.upper()
s.strip()    # remove whitespace
s.split()    # split by whitespace
s.replace(old, new)

# ASCII values
ord('a')     # 97
chr(97)      # 'a'
```

## Common Edge Cases

- Empty input: `[]` or `""`
- Single element: `[x]` or `"x"`
- Two elements
- All same elements
- Already sorted/reversed
- Negative numbers
- Integer overflow/underflow
- Special characters in strings
- Case sensitivity

## Problem Recognition

| Keywords | Pattern |
|----------|---------|
| "subarray", "substring", "contiguous" | Sliding Window |
| "sorted array", "find pair" | Two Pointers |
| "range sum", "multiple queries" | Prefix Sum |
| "palindrome" | Two Pointers |
| "anagram" | Character Frequency |
| "in-place", "constant space" | Two Pointers / Swap |
| "rotate", "reverse" | Reversal Technique |

## Time Complexity Goals

- **O(n)**: Single pass, two pointers, sliding window
- **O(n log n)**: Sorting first, then process
- **O(n²)**: Nested loops (often brute force)
- **O(log n)**: Binary search on sorted array

## Interview Template

```python
def solve_problem(arr):
    # 1. Handle edge cases
    if not arr:
        return default_value
    
    # 2. Initialize variables
    result = initial_value
    
    # 3. Main logic (choose pattern)
    # - Two pointers
    # - Sliding window
    # - Prefix sum
    # etc.
    
    # 4. Return result
    return result
```

## Quick Wins

1. **Sort first** if order doesn't matter and it simplifies logic
2. **Use hash map** for O(1) lookups (see Hashing section)
3. **Two pointers** for O(n) instead of O(n²) nested loops
4. **Sliding window** for contiguous subarray problems
5. **String builder** (list + join) instead of string concatenation
