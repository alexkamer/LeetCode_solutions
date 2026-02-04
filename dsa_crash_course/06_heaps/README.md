# Heaps

A heap is a specialized tree-based data structure that satisfies the heap property. Heaps are the foundation of priority queues and are essential for solving many optimization problems efficiently.

## 📖 What is a Heap?

A **heap** is a complete binary tree where each node satisfies the heap property:
- **Min-Heap**: Every parent node is smaller than or equal to its children
- **Max-Heap**: Every parent node is greater than or equal to its children

### Visual Representation

**Min-Heap Example:**
```
       1
      / \
     3   2
    / \ / \
   5  4 7  6

Array representation: [1, 3, 2, 5, 4, 7, 6]
```

**Max-Heap Example:**
```
       9
      / \
     7   8
    / \ / \
   4  6 5  3

Array representation: [9, 7, 8, 4, 6, 5, 3]
```

### Key Properties

1. **Complete Binary Tree**: All levels are filled except possibly the last, which is filled left to right
2. **Heap Property**: Parent-child relationship follows min or max constraint
3. **Array Representation**: Can be efficiently stored in an array
4. **No Ordering Between Siblings**: Only parent-child relationships matter

### Array Representation

Heaps are typically implemented using arrays with index relationships:

```python
# For node at index i (0-indexed):
left_child = 2 * i + 1
right_child = 2 * i + 2
parent = (i - 1) // 2

# For node at index i (1-indexed):
left_child = 2 * i
right_child = 2 * i + 1
parent = i // 2
```

**Example:** Array `[1, 3, 2, 5, 4, 7, 6]`
```
Index:  0  1  2  3  4  5  6
Value:  1  3  2  5  4  7  6

Index 1 (value 3):
  - Left child: 2*1+1 = 3 (value 5)
  - Right child: 2*1+2 = 4 (value 4)
  - Parent: (1-1)//2 = 0 (value 1)
```

## 📖 Heap Operations

### Heapify (Bubble Down / Sift Down)

Restore heap property by moving a node down the tree.

**Process:**
1. Compare node with its children
2. Swap with smaller child (min-heap) or larger child (max-heap)
3. Continue until heap property is satisfied

```python
def heapify_down(arr, n, i):
    """
    Maintain min-heap property by bubbling down.

    Time: O(log n)
    """
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Find smallest among node and children
    if left < n and arr[left] < arr[smallest]:
        smallest = left
    if right < n and arr[right] < arr[smallest]:
        smallest = right

    # If smallest is not current node, swap and continue
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        heapify_down(arr, n, smallest)
```

### Bubble Up (Sift Up)

Restore heap property by moving a node up the tree.

**Process:**
1. Compare node with its parent
2. Swap if heap property is violated
3. Continue until root or property is satisfied

```python
def heapify_up(arr, i):
    """
    Maintain min-heap property by bubbling up.

    Time: O(log n)
    """
    parent = (i - 1) // 2

    # If current node is smaller than parent, swap
    if parent >= 0 and arr[i] < arr[parent]:
        arr[i], arr[parent] = arr[parent], arr[i]
        heapify_up(arr, parent)
```

### Insert

Add new element to heap.

```python
def heap_insert(heap, value):
    """
    Insert value into min-heap.

    Time: O(log n)
    """
    # Add to end of array
    heap.append(value)

    # Bubble up to maintain heap property
    heapify_up(heap, len(heap) - 1)
```

### Extract Min/Max

Remove and return root element.

```python
def heap_extract_min(heap):
    """
    Remove and return minimum element.

    Time: O(log n)
    """
    if not heap:
        return None

    # Store minimum
    min_val = heap[0]

    # Move last element to root
    heap[0] = heap[-1]
    heap.pop()

    # Bubble down to maintain heap property
    if heap:
        heapify_down(heap, len(heap), 0)

    return min_val
```

### Build Heap

Convert arbitrary array to heap.

```python
def build_heap(arr):
    """
    Build min-heap from array in-place.

    Time: O(n) - not O(n log n)!
    """
    n = len(arr)

    # Start from last non-leaf node and heapify down
    for i in range(n // 2 - 1, -1, -1):
        heapify_down(arr, n, i)
```

**Why O(n)?** Most nodes are near bottom and only bubble down a few levels.

## ⏱️ Time Complexity

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Insert | O(log n) | Bubble up from bottom |
| Extract Min/Max | O(log n) | Bubble down from root |
| Peek Min/Max | O(1) | Access root element |
| Build Heap | O(n) | Heapify from bottom up |
| Heapify | O(log n) | Move node to correct position |
| Search | O(n) | Must check all nodes |
| Delete | O(log n) | Extract + heapify |

### Space Complexity

- **Heap storage**: O(n) for n elements
- **Operations**: O(1) extra space (or O(log n) with recursion)

## 📖 Priority Queue

A **priority queue** is an abstract data type where elements have priorities. Heaps are the most efficient implementation.

### Priority Queue Interface

```python
pq.push(item)          # Add item
pq.pop()               # Remove highest priority
pq.top()               # View highest priority
len(pq)                # Number of items
```

### Min-Heap vs Max-Heap Priority Queue

- **Min-Heap PQ**: Smallest element has highest priority
- **Max-Heap PQ**: Largest element has highest priority

## 💻 Python heapq Module

Python's `heapq` module provides a min-heap implementation.

### Basic Operations

```python
import heapq

# Create heap
heap = []                    # Empty heap
heap = [3, 1, 4, 1, 5]
heapq.heapify(heap)          # Convert to heap: O(n)

# Insert
heapq.heappush(heap, 2)      # O(log n)

# Extract minimum
min_val = heapq.heappop(heap)  # O(log n)

# Peek minimum
min_val = heap[0]            # O(1)

# Push and pop atomically
heapq.heappushpop(heap, 6)   # More efficient than separate ops

# Replace minimum
heapq.heapreplace(heap, 7)   # Pop then push
```

### Finding N Largest/Smallest

```python
import heapq

nums = [3, 1, 4, 1, 5, 9, 2, 6]

# N largest elements
largest = heapq.nlargest(3, nums)     # [9, 6, 5]

# N smallest elements
smallest = heapq.nsmallest(3, nums)   # [1, 1, 2]

# With custom key
items = [('A', 3), ('B', 1), ('C', 4)]
largest = heapq.nlargest(2, items, key=lambda x: x[1])
# [('C', 4), ('A', 3)]
```

### Max-Heap in Python

Python's heapq is min-heap only. For max-heap, negate values:

```python
import heapq

# Max-heap by negating values
max_heap = []
heapq.heappush(max_heap, -5)   # Insert 5
heapq.heappush(max_heap, -3)   # Insert 3
heapq.heappush(max_heap, -8)   # Insert 8

max_val = -heapq.heappop(max_heap)  # Get 8

# Or use wrapper class
class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        heapq.heappush(self.heap, -val)

    def pop(self):
        return -heapq.heappop(self.heap)

    def peek(self):
        return -self.heap[0]

    def __len__(self):
        return len(self.heap)
```

### Heap with Custom Objects

```python
import heapq

# Using tuples (priority, data)
heap = []
heapq.heappush(heap, (2, 'task2'))
heapq.heappush(heap, (1, 'task1'))
heapq.heappush(heap, (3, 'task3'))

priority, task = heapq.heappop(heap)  # (1, 'task1')

# Using custom class with __lt__
class Task:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name

    def __lt__(self, other):
        return self.priority < other.priority

heap = []
heapq.heappush(heap, Task(2, 'task2'))
heapq.heappush(heap, Task(1, 'task1'))

task = heapq.heappop(heap)  # Task(1, 'task1')
```

## 🎯 Common Heap Patterns

### 1. Top K Elements

Find K largest or smallest elements.

```python
def find_k_largest(nums, k):
    """
    Find K largest elements using min-heap.

    Approach:
    - Maintain min-heap of size K
    - Heap top is Kth largest
    - Larger elements replace minimum

    Time: O(n log k)
    Space: O(k)
    """
    import heapq

    # Method 1: Using nlargest (simplest)
    return heapq.nlargest(k, nums)

    # Method 2: Manual min-heap of size K
    heap = []

    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)

    return heap
```

**Pattern Recognition:**
- "Find K largest/smallest"
- "Top K frequent"
- "Kth largest element"

**Key Insight:** Use min-heap of size K for K largest (max-heap for K smallest).

### 2. Merge K Sorted Lists

Merge multiple sorted sequences efficiently.

```python
def merge_k_sorted(lists):
    """
    Merge K sorted arrays.

    Approach:
    - Min-heap with one element from each list
    - Pop minimum, push next from same list
    - Heap maintains K elements

    Time: O(N log K) where N is total elements
    Space: O(K) for heap
    """
    import heapq

    result = []
    heap = []

    # Initialize heap with first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Add next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result
```

**Pattern Recognition:**
- "Merge K sorted"
- "Find median from streams"
- "Smallest range in K lists"

**Key Insight:** Heap efficiently finds minimum among K candidates.

### 3. Running Median

Maintain median of a stream of numbers.

```python
class MedianFinder:
    """
    Find median from data stream.

    Approach:
    - Max-heap for smaller half
    - Min-heap for larger half
    - Balance heaps to keep sizes equal

    Time: O(log n) per insert, O(1) for median
    Space: O(n)
    """
    def __init__(self):
        import heapq
        self.small = []  # Max-heap (negated)
        self.large = []  # Min-heap

    def add_num(self, num):
        # Add to max-heap (smaller half)
        heapq.heappush(self.small, -num)

        # Balance: move largest from small to large
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # If large has more, move one back
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

**Pattern Recognition:**
- "Find median"
- "Running average"
- "Split data into halves"

**Key Insight:** Two heaps maintain split point in sorted order.

### 4. Task Scheduling

Schedule tasks with cooldown periods.

```python
def task_scheduler(tasks, n):
    """
    Schedule tasks with cooldown period n.

    Approach:
    - Max-heap for most frequent tasks
    - Schedule tasks, track cooldown
    - Idle time when no available tasks

    Time: O(m log m) where m is unique tasks
    Space: O(m)
    """
    from collections import Counter
    import heapq

    # Count frequencies
    freq = Counter(tasks)

    # Max-heap of frequencies
    heap = [-count for count in freq.values()]
    heapq.heapify(heap)

    time = 0

    while heap:
        temp = []

        # Execute n+1 tasks (one cycle)
        for _ in range(n + 1):
            if heap:
                count = heapq.heappop(heap)
                if count < -1:
                    temp.append(count + 1)

        # Put tasks back
        for count in temp:
            heapq.heappush(heap, count)

        # Add time for this cycle
        time += (n + 1) if heap else len(temp)

    return time
```

**Pattern Recognition:**
- "Schedule with constraints"
- "Cooldown period"
- "Maximize utilization"

**Key Insight:** Prioritize most frequent items to avoid idle time.

### 5. K-Way Merge

Generalization of merge K sorted lists.

```python
def k_way_merge(iterators):
    """
    Merge K sorted iterators.

    Approach:
    - Heap maintains one element per iterator
    - Always process smallest available
    - Replace with next from same iterator

    Time: O(N log K)
    Space: O(K)
    """
    import heapq

    heap = []

    # Initialize heap
    for i, it in enumerate(iterators):
        try:
            val = next(it)
            heapq.heappush(heap, (val, i, it))
        except StopIteration:
            pass

    while heap:
        val, idx, it = heapq.heappop(heap)
        yield val

        try:
            next_val = next(it)
            heapq.heappush(heap, (next_val, idx, it))
        except StopIteration:
            pass
```

### 6. Sliding Window Maximum

Find maximum in each sliding window (can use heap or deque).

```python
def sliding_window_max(nums, k):
    """
    Find maximum in each window of size k.

    Heap approach (not optimal, but demonstrates pattern).

    Time: O(n log k)
    Space: O(k)
    """
    import heapq

    # Max-heap with (value, index)
    heap = []
    result = []

    for i, num in enumerate(nums):
        # Add current
        heapq.heappush(heap, (-num, i))

        # Remove elements outside window
        while heap and heap[0][1] <= i - k:
            heapq.heappop(heap)

        # Add to result when window is full
        if i >= k - 1:
            result.append(-heap[0][0])

    return result
```

### 7. Interval Problems

Merge intervals, find meeting rooms, etc.

```python
def min_meeting_rooms(intervals):
    """
    Find minimum meeting rooms needed.

    Approach:
    - Sort by start time
    - Min-heap tracks end times
    - Add new meeting if rooms available

    Time: O(n log n)
    Space: O(n)
    """
    import heapq

    if not intervals:
        return 0

    # Sort by start time
    intervals.sort()

    # Min-heap of end times
    heap = []

    for start, end in intervals:
        # If room available (earliest meeting ended), reuse it
        if heap and heap[0] <= start:
            heapq.heappop(heap)

        # Add current meeting's end time
        heapq.heappush(heap, end)

    return len(heap)
```

## 🎯 When to Use Heaps

Use heaps when you need:

1. **Top K elements** - K largest/smallest from collection
2. **Priority ordering** - Process items by priority
3. **Streaming data** - Running minimum/maximum/median
4. **K-way merge** - Combine multiple sorted sequences
5. **Scheduling** - Task scheduling with priorities
6. **Optimization** - Greedy algorithms (Dijkstra, Huffman)

### Problem Indicators

Use heaps when you see:
- "Find K largest/smallest"
- "Top K frequent"
- "Kth largest element"
- "Merge K sorted"
- "Meeting rooms"
- "Task scheduler"
- "Find median"
- "Shortest path" (Dijkstra)
- "Minimum cost"

## 🎓 Heap vs Other Data Structures

| Need | Heap | Alternative |
|------|------|-------------|
| Find min/max | O(1) peek | Sorted array: O(1) |
| Insert | O(log n) | Sorted array: O(n) |
| Delete min/max | O(log n) | Sorted array: O(n) |
| Build from array | O(n) | Sort: O(n log n) |
| Find K largest | O(n log k) | Sort: O(n log n) |
| Search arbitrary | O(n) | Hash map: O(1) |
| Range query | Not supported | Segment tree |

**Use Heap when:**
- Need efficient min/max access
- Dynamic insertions/deletions
- Don't need full sorting
- K << N for top-K problems

**Consider alternatives when:**
- Need full sorting → Sort array
- Need arbitrary lookups → Hash map
- Need range queries → Segment tree
- Static data → Pre-sort once

## 🚨 Common Pitfalls and Tips

### 1. Python heapq is Min-Heap Only

```python
import heapq

# For max-heap, negate values
max_heap = []
heapq.heappush(max_heap, -5)
max_val = -heapq.heappop(max_heap)

# Or use wrapper class
class MaxHeap:
    def __init__(self):
        self.heap = []
    def push(self, val):
        heapq.heappush(self.heap, -val)
    def pop(self):
        return -heapq.heappop(self.heap)
```

### 2. Tuple Comparison for Priority

```python
# Tuples compare element-wise
heap = []
heapq.heappush(heap, (priority, data))

# If data is not comparable, add tiebreaker
counter = 0
for item in items:
    heapq.heappush(heap, (priority, counter, item))
    counter += 1
```

### 3. Tracking Indices with Values

```python
# Store (value, index) to track positions
heap = []
for i, val in enumerate(nums):
    heapq.heappush(heap, (val, i))

val, idx = heapq.heappop(heap)
```

### 4. Removing Stale Entries

```python
# Lazy deletion: mark as deleted, skip when popped
deleted = set()

while heap and heap[0] in deleted:
    heapq.heappop(heap)
```

### 5. Building Heap vs Repeated Insert

```python
# BAD: O(n log n)
heap = []
for num in nums:
    heapq.heappush(heap, num)

# GOOD: O(n)
heap = nums[:]
heapq.heapify(heap)
```

### 6. Top K with Opposite Heap

```python
# K largest: use min-heap of size K
# K smallest: use max-heap of size K

def k_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)  # Min-heap
        if len(heap) > k:
            heapq.heappop(heap)  # Remove smallest
    return heap

def k_smallest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, -num)  # Max-heap (negated)
        if len(heap) > k:
            heapq.heappop(heap)  # Remove largest
    return [-x for x in heap]
```

## 💡 Interview Tips

1. **Identify heap problems**
   - "Top K" → Heap of size K
   - "Merge K sorted" → K-way merge with heap
   - "Median" → Two heaps
   - "Scheduling" → Priority queue

2. **Choose min-heap or max-heap**
   - K largest → min-heap (top is Kth largest)
   - K smallest → max-heap (top is Kth smallest)
   - Median → both (split data)

3. **Optimize with heap**
   - Reduce O(n²) to O(n log n) for comparisons
   - Avoid full sort when only partial order needed
   - Use heap for dynamic data

4. **Complexity analysis**
   - Build heap: O(n), not O(n log n)
   - K operations: O(k log n)
   - N elements, K candidates: O(N log K)

5. **Common mistakes to avoid**
   - Forgetting Python heapq is min-heap
   - Using heap when array would suffice
   - Not considering space for heap
   - Comparing incompatible types

## 📚 LeetCode Problem Categories

### Easy
- Kth Largest Element in Array (215)
- Last Stone Weight (1046)
- Relative Ranks (506)
- Third Maximum Number (414)

### Medium
- Top K Frequent Elements (347)
- Kth Largest Element in Stream (703)
- K Closest Points to Origin (973)
- Reorganize String (767)
- Task Scheduler (621)
- Find K Pairs with Smallest Sums (373)
- Sort Characters by Frequency (451)

### Hard
- Merge K Sorted Lists (23)
- Find Median from Data Stream (295)
- Sliding Window Maximum (239)
- Smallest Range Covering Elements from K Lists (632)
- IPO (502)
- The Skyline Problem (218)

## 🔗 Related Topics

- **Priority Queues** - Heaps are the standard implementation
- **Sorting** - Heap sort uses heap structure
- **Graph Algorithms** - Dijkstra's algorithm uses min-heap
- **Greedy Algorithms** - Often use heaps for optimization
- **Trees** - Heaps are complete binary trees
- **Divide and Conquer** - Merge K sorted uses heap

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems!
