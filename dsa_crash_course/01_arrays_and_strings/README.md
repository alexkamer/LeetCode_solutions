# Arrays and Strings

Arrays and strings are the most fundamental data structures in programming. They appear in almost every coding interview and form the foundation for understanding more complex data structures.

## 📖 What Are Arrays?

An **array** is a contiguous block of memory that stores elements of the same type. Each element can be accessed directly using its index.

### Key Properties

- **Fixed size** (in most languages) - Size determined at creation
- **Contiguous memory** - Elements stored sequentially
- **Random access** - O(1) access time to any element via index
- **Index-based** - Zero-indexed in most languages

### Arrays in Python

Python uses **lists**, which are dynamic arrays that can grow/shrink:

```python
# Creating arrays
arr = [1, 2, 3, 4, 5]
empty = []
sized = [0] * 5  # [0, 0, 0, 0, 0]

# Accessing elements
first = arr[0]      # 1
last = arr[-1]      # 5 (negative indexing)

# Modifying
arr[0] = 10         # [10, 2, 3, 4, 5]
arr.append(6)       # [10, 2, 3, 4, 5, 6]
arr.pop()           # [10, 2, 3, 4, 5]
```

## 📖 What Are Strings?

A **string** is a sequence of characters. In most languages, strings are immutable (cannot be changed after creation).

### Key Properties

- **Immutable** (in Python, Java, etc.) - Any "modification" creates a new string
- **Indexed like arrays** - Can access characters by position
- **Sequence operations** - Slicing, concatenation, searching

### Strings in Python

```python
# Creating strings
s = "hello"
s = 'hello'
s = """multi
line"""

# Accessing
first = s[0]        # 'h'
last = s[-1]        # 'o'

# Slicing
sub = s[1:4]        # 'ell' (start:end, end exclusive)
rev = s[::-1]       # 'olleh' (reverse)

# Common operations
s.upper()           # 'HELLO'
s.lower()           # 'hello'
s.split(',')        # Split into list
''.join(['a','b'])  # 'ab' (join list into string)
```

## ⏱️ Time Complexity

### Array Operations

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Access by index | O(1) | Direct memory address calculation |
| Search (unsorted) | O(n) | Must check each element |
| Search (sorted) | O(log n) | Binary search |
| Insert at end | O(1)* | Amortized for dynamic arrays |
| Insert at position | O(n) | Must shift elements |
| Delete at end | O(1) | Simple pop |
| Delete at position | O(n) | Must shift elements |
| Slice/Subarray | O(k) | Where k is slice length |

### String Operations (Python)

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Access by index | O(1) | Like arrays |
| Concatenation | O(n+m) | Creates new string |
| Slice | O(k) | Creates new string of length k |
| String formatting | O(n) | Creates new string |
| `s.split()` | O(n) | Creates list of strings |
| `''.join(list)` | O(n) | More efficient than repeated concat |
| `s.replace()` | O(n) | Creates new string |
| `s in text` | O(n*m)* | Naive; can be O(n+m) with KMP |

## 💾 Space Complexity

- **Fixed array**: O(n) where n is the size
- **Dynamic array**: O(n) with potential extra capacity
- **String operations**: Often O(n) due to immutability creating new strings

## 🎯 Common Patterns and Techniques

### 1. Two Pointers

Use two pointers moving through the array/string:

**Types:**
- **Opposite directions** - Start/end moving toward each other
- **Same direction** - Fast/slow pointers
- **Sliding window** - Left/right bounds of a window

**When to use:**
- Sorted array problems
- Palindrome checking
- Finding pairs that sum to target
- Removing duplicates in-place

```python
# Example: Two Sum (sorted array)
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        curr_sum = arr[left] + arr[right]
        
        if curr_sum == target:
            return [left, right]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    
    return []
```

### 2. Sliding Window

Maintain a window of elements and expand/contract it:

**When to use:**
- Subarray/substring problems
- "Maximum/minimum subarray of size k"
- "Longest substring with at most k distinct characters"

**Types:**
- **Fixed size** - Window size doesn't change
- **Variable size** - Window grows/shrinks based on condition

```python
# Example: Maximum sum subarray of size k
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        # Slide window: add new element, remove old
        window_sum = window_sum + arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

### 3. Prefix Sum

Precompute cumulative sums for fast range queries:

```python
# Build prefix sum array
def build_prefix_sum(arr):
    prefix = [0]
    for num in arr:
        prefix.append(prefix[-1] + num)
    return prefix

# Query sum of arr[i:j+1] in O(1)
def range_sum(prefix, i, j):
    return prefix[j+1] - prefix[i]
```

**When to use:**
- Multiple range sum queries
- Subarray sum problems

### 4. In-Place Modification

Modify array without extra space:

```python
# Example: Remove duplicates in sorted array
def remove_duplicates(arr):
    if not arr:
        return 0
    
    write_pos = 1
    for i in range(1, len(arr)):
        if arr[i] != arr[i-1]:
            arr[write_pos] = arr[i]
            write_pos += 1
    
    return write_pos
```

### 5. String Builder Pattern

Efficiently build strings by using a list:

```python
# BAD: O(n²) due to string immutability
result = ""
for char in chars:
    result += char  # Creates new string each time

# GOOD: O(n) using list
result = []
for char in chars:
    result.append(char)
return ''.join(result)  # Single join operation
```

### 6. Character Mapping

Use arrays as hash maps for character counting:

```python
# Count character frequencies
def count_chars(s):
    # For lowercase letters only
    counts = [0] * 26
    for char in s:
        counts[ord(char) - ord('a')] += 1
    return counts

# Check if two strings are anagrams
def are_anagrams(s1, s2):
    return count_chars(s1) == count_chars(s2)
```

### 7. Reversal Techniques

```python
# Reverse entire array in-place
def reverse(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

# Rotate array right by k positions
def rotate(arr, k):
    k = k % len(arr)
    reverse(arr)              # Reverse all
    reverse(arr[:k])          # Reverse first k
    reverse(arr[k:])          # Reverse rest
```

## 🚨 Edge Cases to Consider

1. **Empty input** - `[]` or `""`
2. **Single element** - `[1]` or `"a"`
3. **All same elements** - `[5,5,5,5]`
4. **Already sorted** - In wrong direction
5. **Negative numbers** - If applicable
6. **Very large/small values** - Integer overflow
7. **Special characters/spaces** - In strings
8. **Unicode characters** - In strings
9. **Case sensitivity** - In string comparisons

## 🎓 When to Use Arrays vs Other Structures

**Use Arrays when:**
- You need random access by index
- Size is known or doesn't change often
- Elements are homogeneous
- Memory locality is important (cache-friendly)

**Consider alternatives when:**
- Frequent insertions/deletions at arbitrary positions → Linked List
- Need fast lookups by key → Hash Table
- Need to maintain sorted order with insertions → Binary Search Tree
- Need to track min/max efficiently → Heap

## 📚 LeetCode Problem Categories

### Easy
- Two Sum
- Best Time to Buy and Sell Stock
- Merge Sorted Array
- Valid Palindrome
- Remove Duplicates from Sorted Array

### Medium
- 3Sum
- Container With Most Water
- Longest Substring Without Repeating Characters
- Group Anagrams
- Product of Array Except Self

### Hard
- Trapping Rain Water
- Minimum Window Substring
- Median of Two Sorted Arrays
- Longest Valid Parentheses

## 🔧 Python-Specific Tips

```python
# List comprehensions (fast and Pythonic)
squares = [x**2 for x in range(10)]
evens = [x for x in arr if x % 2 == 0]

# Unpacking
a, b = b, a  # Swap
first, *rest = arr  # first = arr[0], rest = arr[1:]

# Useful built-ins
max(arr)
min(arr)
sum(arr)
sorted(arr)  # Returns new sorted list
arr.sort()   # In-place sort

# Slicing tricks
reversed_arr = arr[::-1]
copy = arr[:]
every_other = arr[::2]

# Enumerate for index + value
for i, val in enumerate(arr):
    print(f"Index {i}: {val}")
```

## 💡 Interview Tips

1. **Clarify the problem**
   - Can the array be empty?
   - Can it contain duplicates?
   - Is the array sorted?
   - Are there constraints on values?

2. **Consider space-time tradeoffs**
   - Can you solve it in-place? (O(1) space)
   - Would a hash table speed it up?

3. **Start simple**
   - Brute force first (often O(n²))
   - Then optimize (often to O(n) or O(n log n))

4. **Think about patterns**
   - Sorted array → Binary search or two pointers
   - Subarray/substring → Sliding window
   - Multiple queries → Prefix sum

5. **Write clean code**
   - Use meaningful variable names
   - Handle edge cases
   - Add comments for complex logic

## 🔗 Related Topics

- **Hashing** - Often used together with arrays
- **Sorting** - Many array algorithms
- **Binary Search** - On sorted arrays
- **Dynamic Programming** - Often uses arrays for memoization

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems!
