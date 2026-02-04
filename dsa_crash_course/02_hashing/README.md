# Hashing

Hashing is one of the most powerful techniques in algorithm design. It enables constant-time lookups, making many problems that would otherwise require O(n²) or O(n log n) solvable in O(n) time.

## 📖 What is a Hash Table?

A **hash table** (also called hash map or dictionary) is a data structure that maps keys to values using a hash function. It provides extremely fast lookups, insertions, and deletions.

### Key Concepts

- **Hash Function**: Converts a key into an array index
- **Buckets**: Array positions where values are stored
- **Collision**: When two keys hash to the same index
- **Load Factor**: Ratio of stored elements to bucket count

### How Hash Tables Work

```
Key → Hash Function → Index → Value

Example:
"apple" → hash("apple") → 7 → 5
"banana" → hash("banana") → 2 → 3
"cherry" → hash("cherry") → 7 → (collision!)
```

The hash function takes a key and computes an integer index where the value should be stored. When two keys hash to the same index (collision), the hash table uses a collision resolution strategy.

### Collision Handling

**1. Chaining (Separate Chaining)**
- Each bucket stores a linked list of entries
- Multiple keys at same index form a chain
- Python's dict uses a variant of this

**2. Open Addressing**
- Find another empty bucket using probing
- Linear probing: Try next bucket
- Quadratic probing: Try quadratically increasing offsets
- Double hashing: Use second hash function

### Python's Implementation

Python's `dict` uses an optimized hash table with:
- Open addressing with random probing
- Dynamic resizing when load factor exceeds 2/3
- Optimized for integer and string keys
- Maintains insertion order (since Python 3.7+)

## 📖 Hash Table vs Hash Set

### Hash Map (Dictionary)
Stores key-value pairs:
```python
# Python: dict
ages = {"Alice": 25, "Bob": 30}
ages["Alice"]  # 25
```

### Hash Set
Stores only keys (no values):
```python
# Python: set
visited = {"Alice", "Bob"}
"Alice" in visited  # True
```

## ⏱️ Time Complexity

### Average Case (Well-distributed hash function)

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Insert | O(1) | Add key-value pair |
| Delete | O(1) | Remove key-value pair |
| Lookup | O(1) | Check if key exists or get value |
| Update | O(1) | Modify value for existing key |

### Worst Case (Many collisions)

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Insert | O(n) | All keys hash to same bucket |
| Delete | O(n) | Must search through chain |
| Lookup | O(n) | Linear search in chain |

**In practice**: With a good hash function and proper load factor, operations are O(1) almost always.

### Space Complexity

- **Hash Map**: O(n) where n is number of entries
- **Hash Set**: O(n) where n is number of elements
- Additional overhead for buckets (typically 1.5-2x the element count)

## 🎯 When to Use Hashing

Hashing is ideal when you need:

1. **Fast lookups** - Check if element exists
2. **Counting frequency** - Track occurrences of elements
3. **Caching/Memoization** - Store computed results
4. **Removing duplicates** - Set guarantees uniqueness
5. **Grouping data** - Collect items by some key
6. **Two-way mapping** - Bidirectional key-value lookup

### Problem Indicators

Use hashing when you see:
- "Find pair that sums to X"
- "Count occurrences/frequency"
- "First/last unique element"
- "Check for duplicates"
- "Group anagrams/similar items"
- "Subarray with sum/condition"
- "Complement/difference problems"

## 🎯 Common Hashing Patterns

### 1. Frequency Counting

Count occurrences of each element:

```python
from collections import Counter

# Manual approach
def count_frequencies(arr):
    freq = {}
    for num in arr:
        freq[num] = freq.get(num, 0) + 1
    return freq

# Using Counter (recommended)
def count_frequencies(arr):
    return Counter(arr)

# Example
arr = [1, 2, 2, 3, 3, 3]
freq = count_frequencies(arr)
# freq = {1: 1, 2: 2, 3: 3}
```

**When to use:**
- Finding most/least frequent element
- Detecting duplicates
- Checking if arrays have same elements
- Character frequency in strings

### 2. Two Sum Pattern

Use hash map to find complement in O(n):

```python
def two_sum(arr, target):
    """
    Find indices of two numbers that sum to target.

    Time: O(n), Space: O(n)
    """
    seen = {}  # value -> index

    for i, num in enumerate(arr):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []

# Example: arr = [2, 7, 11, 15], target = 9
# Returns [0, 1] because arr[0] + arr[1] = 2 + 7 = 9
```

**Variations:**
- Three sum (use hash set with two pointers)
- Four sum
- Pair with given difference
- Count pairs with sum

### 3. Seen/Visited Tracking

Track elements you've encountered:

```python
def contains_duplicate(arr):
    """
    Check if array has any duplicate values.

    Time: O(n), Space: O(n)
    """
    seen = set()

    for num in arr:
        if num in seen:
            return True
        seen.add(num)

    return False
```

**When to use:**
- Detecting duplicates
- Cycle detection
- Visited nodes in graph traversal
- Avoiding recomputation

### 4. Grouping by Key

Collect items that share a property:

```python
def group_anagrams(words):
    """
    Group strings that are anagrams of each other.

    Time: O(n * k log k) where k is max word length
    Space: O(n * k)
    """
    groups = {}

    for word in words:
        # Use sorted word as key
        key = ''.join(sorted(word))

        if key not in groups:
            groups[key] = []

        groups[key].append(word)

    return list(groups.values())

# Example: ["eat", "tea", "tan", "ate", "nat", "bat"]
# Returns: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

**When to use:**
- Group anagrams
- Group by sum/product/property
- Categorize by pattern
- Collect by shared attribute

### 5. Prefix Sum with Hash Map

Find subarrays with given sum/property:

```python
def subarray_sum_equals_k(arr, k):
    """
    Count subarrays that sum to k.

    Time: O(n), Space: O(n)
    """
    count = 0
    prefix_sum = 0
    sum_freq = {0: 1}  # Handle subarrays starting at index 0

    for num in arr:
        prefix_sum += num

        # Check if (prefix_sum - k) exists
        # If yes, we found subarrays ending at current position
        if prefix_sum - k in sum_freq:
            count += sum_freq[prefix_sum - k]

        # Store current prefix sum
        sum_freq[prefix_sum] = sum_freq.get(prefix_sum, 0) + 1

    return count
```

**When to use:**
- Subarray sum equals K
- Longest subarray with sum
- Contiguous array (equal 0s and 1s)
- Running sum problems

### 6. Index Mapping

Store first/last occurrence of elements:

```python
def first_unique_character(s):
    """
    Find index of first non-repeating character.

    Time: O(n), Space: O(1) - limited character set
    """
    # Count frequency
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1

    # Find first unique
    for i, char in enumerate(s):
        if freq[char] == 1:
            return i

    return -1
```

**When to use:**
- First unique element
- Last occurrence tracking
- Index-based problems
- Position mapping

### 7. Set Operations

Use sets for mathematical operations:

```python
def intersection(arr1, arr2):
    """
    Find common elements in two arrays.

    Time: O(n + m), Space: O(n)
    """
    return list(set(arr1) & set(arr2))

def union(arr1, arr2):
    """Find all unique elements."""
    return list(set(arr1) | set(arr2))

def difference(arr1, arr2):
    """Find elements in arr1 but not arr2."""
    return list(set(arr1) - set(arr2))
```

**When to use:**
- Finding common elements
- Removing duplicates
- Checking subset/superset
- Set-based math problems

## 💻 Python Dict and Set Operations

### Dictionary (dict)

```python
# Creating
d = {}
d = dict()
d = {"key": "value"}
d = dict(key="value")

# Accessing
value = d["key"]           # KeyError if missing
value = d.get("key")       # None if missing
value = d.get("key", 0)    # Default value

# Modifying
d["key"] = "new_value"     # Insert or update
d.setdefault("key", 0)     # Set if not exists
d.update({"k": "v"})       # Merge dictionaries

# Removing
del d["key"]               # KeyError if missing
value = d.pop("key")       # Remove and return
value = d.pop("key", None) # With default
d.clear()                  # Remove all

# Checking
"key" in d                 # O(1) membership test
"key" not in d

# Iterating
for key in d:              # Iterate keys
for key, val in d.items(): # Iterate pairs
for val in d.values():     # Iterate values

# Useful methods
len(d)                     # Number of entries
list(d.keys())            # All keys
list(d.values())          # All values
```

### Set (set)

```python
# Creating
s = set()
s = {1, 2, 3}
s = set([1, 2, 3])

# Adding
s.add(4)                   # Add single element
s.update([5, 6, 7])        # Add multiple

# Removing
s.remove(4)                # KeyError if missing
s.discard(4)               # No error if missing
s.pop()                    # Remove arbitrary element
s.clear()                  # Remove all

# Checking
4 in s                     # O(1) membership
len(s)                     # Number of elements

# Set operations
s1 & s2                    # Intersection
s1 | s2                    # Union
s1 - s2                    # Difference
s1 ^ s2                    # Symmetric difference
s1.intersection(s2)        # Same as &
s1.union(s2)              # Same as |

# Comparison
s1 <= s2                   # Is subset
s1 < s2                    # Is proper subset
s1 >= s2                   # Is superset
```

### Collections Module

```python
from collections import Counter, defaultdict, OrderedDict

# Counter: Count hashable objects
counter = Counter([1, 2, 2, 3, 3, 3])
# Counter({3: 3, 2: 2, 1: 1})

counter.most_common(2)     # [(3, 3), (2, 2)]
counter['new'] = 5         # Add/update count
counter.update([1, 1, 1])  # Add counts

# defaultdict: Dict with default values
dd = defaultdict(int)      # Default: 0
dd = defaultdict(list)     # Default: []
dd = defaultdict(set)      # Default: set()

dd['key'].append(1)        # No KeyError!

# OrderedDict: Remembers insertion order
# Note: Regular dict maintains order since Python 3.7
od = OrderedDict()
od['first'] = 1
od['second'] = 2
od.move_to_end('first')    # Move to end
```

## 🚨 Common Pitfalls and Tips

### 1. Unhashable Types

Only immutable types can be dictionary keys or set elements:

```python
# Valid keys
d = {42: "int"}
d = {"string": "value"}
d = {(1, 2): "tuple"}

# Invalid keys (mutable)
d = {[1, 2]: "list"}       # TypeError
d = {{"k": "v"}: "dict"}   # TypeError
d = {{1, 2}: "set"}        # TypeError

# Workaround: Convert to tuple
d = {tuple([1, 2]): "value"}
```

### 2. Default Values

Use `get()` or `defaultdict` to avoid KeyError:

```python
# BAD: Can raise KeyError
count = {}
for num in arr:
    count[num] += 1  # Error on first occurrence

# GOOD: Use get() with default
count = {}
for num in arr:
    count[num] = count.get(num, 0) + 1

# BETTER: Use defaultdict
from collections import defaultdict
count = defaultdict(int)
for num in arr:
    count[num] += 1
```

### 3. Set vs List for Membership

Use set for fast membership testing:

```python
# BAD: O(n) per lookup
words = ["apple", "banana", "cherry"]
if "apple" in words:  # Linear search

# GOOD: O(1) per lookup
words = {"apple", "banana", "cherry"}
if "apple" in words:  # Hash lookup
```

### 4. Modifying While Iterating

Don't modify dict/set during iteration:

```python
# BAD: RuntimeError
d = {"a": 1, "b": 2}
for key in d:
    if key == "a":
        del d[key]  # Error!

# GOOD: Create list of keys first
for key in list(d.keys()):
    if key == "a":
        del d[key]
```

### 5. Hash Collisions

Be aware of worst-case O(n) performance:

```python
# Adversarial input can cause collisions
# Python mitigates with random hash seed
# Usually not a concern in practice
```

## 🎓 Hash Table vs Other Data Structures

| Need | Hash Table | Alternative |
|------|-----------|-------------|
| Fast lookup | O(1) | Array: O(1) with index, O(n) search |
| Maintain order | No (use OrderedDict) | Array maintains order |
| Range queries | No | Binary Search Tree: O(log n) |
| Find min/max | O(n) | Heap: O(1) |
| Sorted data | No | BST or sorted array |
| Memory efficiency | Moderate | Array more compact |

**Use Hash Table when:**
- Fast lookups are critical
- Frequency counting needed
- Duplicate detection required
- No need for sorted order

**Consider alternatives when:**
- Need sorted iteration → Binary Search Tree
- Need min/max frequently → Heap
- Need range queries → Segment Tree
- Memory is very limited → Array with sorting

## 📚 LeetCode Problem Categories

### Easy
- Two Sum (1)
- Contains Duplicate (217)
- Valid Anagram (242)
- First Unique Character in String (387)
- Intersection of Two Arrays (349)

### Medium
- Group Anagrams (49)
- Top K Frequent Elements (347)
- Subarray Sum Equals K (560)
- Longest Consecutive Sequence (128)
- 4Sum II (454)

### Hard
- Substring with Concatenation of All Words (30)
- LRU Cache (146) - Hash + Doubly Linked List
- All O'one Data Structure (432)
- Longest Substring with At Most K Distinct Characters (340)

## 💡 Interview Tips

1. **Recognize hashing opportunities**
   - Need O(1) lookup? → Hash table
   - Finding complement/pair? → Hash map
   - Counting frequency? → Hash map
   - Check duplicates? → Hash set

2. **Consider space-time tradeoffs**
   - Hash table uses O(n) extra space
   - Often worth it for O(n²) → O(n) improvement
   - Ask if space is constrained

3. **Choose right data structure**
   - Key-value mapping → dict
   - Membership only → set
   - Counting → Counter
   - Grouping → defaultdict(list)

4. **Handle edge cases**
   - Empty input
   - All duplicates
   - No duplicates
   - Single element

5. **Explain your approach**
   - "I'll use a hash map to store..."
   - "This gives us O(1) lookup..."
   - "Trade O(n) space for better time"

## 🔗 Related Topics

- **Arrays** - Often used together
- **Two Pointers** - Alternative for sorted arrays
- **Sliding Window** - With hash map for character counting
- **Graph Algorithms** - Hash sets for visited nodes
- **Dynamic Programming** - Hash maps for memoization

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems!
