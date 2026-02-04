# Hashing - Quick Reference

## Complexity Cheat Sheet

### Hash Map (dict)
- **Insert**: O(1) average, O(n) worst
- **Delete**: O(1) average, O(n) worst
- **Lookup**: O(1) average, O(n) worst
- **Space**: O(n)

### Hash Set (set)
- **Add**: O(1) average, O(n) worst
- **Remove**: O(1) average, O(n) worst
- **Contains**: O(1) average, O(n) worst
- **Space**: O(n)

**In practice**: Almost always O(1) with good hash function.

## Common Patterns

### 1. Frequency Counting
```python
# Manual
freq = {}
for num in arr:
    freq[num] = freq.get(num, 0) + 1

# Using Counter
from collections import Counter
freq = Counter(arr)
most_common = freq.most_common(1)[0]
```

### 2. Two Sum Pattern
```python
# Find pair that sums to target
seen = {}
for i, num in enumerate(arr):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
```

### 3. Seen/Visited Tracking
```python
# Check for duplicates
seen = set()
for num in arr:
    if num in seen:
        return True
    seen.add(num)
return False
```

### 4. Grouping by Key
```python
# Group items by property
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    key = compute_key(item)
    groups[key].append(item)
```

### 5. Prefix Sum + Hash Map
```python
# Count subarrays with sum k
count = 0
prefix_sum = 0
sum_freq = {0: 1}

for num in arr:
    prefix_sum += num
    count += sum_freq.get(prefix_sum - k, 0)
    sum_freq[prefix_sum] = sum_freq.get(prefix_sum, 0) + 1
```

### 6. Index Mapping
```python
# Store first/last occurrence
first_index = {}
for i, val in enumerate(arr):
    if val not in first_index:
        first_index[val] = i

last_index = {}
for i, val in enumerate(arr):
    last_index[val] = i
```

### 7. Set Operations
```python
# Intersection, union, difference
intersection = set(arr1) & set(arr2)
union = set(arr1) | set(arr2)
difference = set(arr1) - set(arr2)
symmetric_diff = set(arr1) ^ set(arr2)
```

## Python-Specific Tricks

### Dictionary Operations
```python
# Creation
d = {}
d = dict()
d = {"key": "value"}

# Safe access
value = d.get("key", default)
value = d.setdefault("key", default)

# Iteration
for key in d:                    # keys
for value in d.values():         # values
for key, value in d.items():     # pairs

# Comprehension
{k: v*2 for k, v in d.items()}

# Merge (Python 3.9+)
merged = d1 | d2
```

### Set Operations
```python
# Creation
s = set()
s = {1, 2, 3}
s = set(arr)

# Methods
s.add(x)
s.remove(x)      # KeyError if missing
s.discard(x)     # No error if missing
s.pop()          # Remove arbitrary

# Comprehension
{x*2 for x in s if x > 0}
```

### Collections Module
```python
from collections import Counter, defaultdict

# Counter
counter = Counter(arr)
counter.most_common(k)
counter['x'] += 1

# defaultdict
dd = defaultdict(int)       # Default: 0
dd = defaultdict(list)      # Default: []
dd = defaultdict(set)       # Default: set()
dd['key'].append(value)     # No KeyError
```

## Common Edge Cases

- Empty input: `[]` or `""`
- Single element: `[x]`
- All duplicates: `[5, 5, 5, 5]`
- No duplicates: `[1, 2, 3, 4]`
- All same key: Hash collisions
- Negative numbers: Works fine
- Zero: Valid key/value
- None: Valid key (hashable)

## Problem Recognition

| Keywords | Pattern | Data Structure |
|----------|---------|----------------|
| "find pair", "two sum" | Two Sum | dict |
| "count frequency", "occurrences" | Frequency Count | Counter |
| "duplicate", "unique" | Seen/Visited | set |
| "first/last unique" | Index Mapping | dict |
| "group by", "anagrams" | Grouping | defaultdict(list) |
| "subarray sum", "prefix" | Prefix Sum | dict |
| "intersection", "union" | Set Ops | set |
| "complement", "difference" | Lookup | dict/set |

## Time Complexity Goals

- **O(n)**: Single pass with hash map
- **O(n log n)**: Sort + hash map
- **O(n * k)**: n items, k operations each
- **O(1) lookup**: Hash map advantage over array

## Hash Map vs Alternatives

| Need | Use | Don't Use |
|------|-----|-----------|
| Fast lookup | Hash map | Sorted array → Binary search O(log n) |
| Count frequency | Counter | Array of counts for limited range |
| Check existence | set | List with `in` → O(n) |
| Group items | defaultdict | Multiple passes |
| Track visited | set | Boolean array if indices known |

## Common Mistakes

### 1. Unhashable Types
```python
# BAD
d = {[1, 2]: "value"}    # Lists not hashable

# GOOD
d = {(1, 2): "value"}    # Tuples hashable
```

### 2. Default Values
```python
# BAD
count = {}
count[x] += 1            # KeyError on first

# GOOD
count[x] = count.get(x, 0) + 1

# BETTER
from collections import defaultdict
count = defaultdict(int)
count[x] += 1
```

### 3. Modifying During Iteration
```python
# BAD
for key in d:
    del d[key]           # RuntimeError

# GOOD
for key in list(d.keys()):
    del d[key]
```

### 4. Set vs List for Lookup
```python
# BAD - O(n)
if x in list:            # Linear search

# GOOD - O(1)
if x in set:             # Hash lookup
```

## Interview Template

```python
def solve_with_hash(arr, target):
    # 1. Choose data structure
    seen = {}        # dict for key-value
    # seen = set()   # set for membership only
    # seen = Counter(arr)  # Counter for frequency

    # 2. Handle edge cases
    if not arr:
        return default

    # 3. Single pass with hash map
    for i, val in enumerate(arr):
        # Check if complement/target exists
        if complement in seen:
            return found

        # Store current element
        seen[val] = i

    # 4. Return result
    return not_found
```

## Quick Wins

1. **O(n²) → O(n)**: Replace nested loop with hash map lookup
2. **Check duplicates**: Use set instead of nested loops
3. **Count frequency**: Use Counter instead of manual dict
4. **Group items**: Use defaultdict(list) instead of checking keys
5. **Prefix sums**: Combine with hash map for subarray problems
6. **Two sum pattern**: Works for many "find pair" problems

## Common LeetCode Patterns

### Easy Level
- Two Sum → Hash map for complement
- Contains Duplicate → Set for seen values
- Valid Anagram → Counter comparison
- First Unique Character → Frequency count + scan

### Medium Level
- Group Anagrams → defaultdict with sorted key
- Subarray Sum K → Prefix sum + hash map
- Top K Frequent → Counter + heap
- Longest Consecutive → Set for O(1) lookup

### Hard Level
- Substring with Concatenation → Sliding window + hash map
- LRU Cache → Hash map + doubly linked list
- All O'one Structure → Multiple hash maps

## Space-Time Tradeoffs

| Approach | Time | Space | When to Use |
|----------|------|-------|-------------|
| Brute force | O(n²) | O(1) | Space constrained |
| Hash map | O(n) | O(n) | Time critical |
| Sort + binary search | O(n log n) | O(1) | Balance both |
| Two pointers | O(n) | O(1) | Sorted input |
