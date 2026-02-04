# Heaps - Quick Reference

## Complexity Cheat Sheet

### Heap Operations
- **Insert**: O(log n)
- **Extract Min/Max**: O(log n)
- **Peek Min/Max**: O(1)
- **Build Heap**: O(n) - not O(n log n)!
- **Heapify**: O(log n)
- **Search**: O(n)
- **Space**: O(n)

### Common Patterns
- **Top K elements**: O(n log k) time, O(k) space
- **Merge K sorted**: O(N log K) time where N is total elements
- **Running median**: O(log n) insert, O(1) find median
- **Task scheduling**: O(m log m) where m is unique tasks

## Python heapq Operations

### Basic Operations
```python
import heapq

# Create heap
heap = []
heap = [3, 1, 4, 1, 5]
heapq.heapify(heap)          # O(n) - convert to heap

# Insert
heapq.heappush(heap, 2)      # O(log n)

# Extract minimum
min_val = heapq.heappop(heap)  # O(log n)

# Peek minimum
min_val = heap[0]            # O(1)

# Combined operations
heapq.heappushpop(heap, 6)   # Push then pop (efficient)
heapq.heapreplace(heap, 7)   # Pop then push

# Find N largest/smallest
largest = heapq.nlargest(k, nums)    # O(n log k)
smallest = heapq.nsmallest(k, nums)  # O(n log k)
```

### Max-Heap in Python
```python
# Python heapq is min-heap only
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
    def peek(self):
        return -self.heap[0] if self.heap else None
```

### With Tuples (Priority, Data)
```python
# Tuples compare element-wise
heap = []
heapq.heappush(heap, (priority, data))

# If data not comparable, add tiebreaker
counter = 0
for item in items:
    heapq.heappush(heap, (priority, counter, item))
    counter += 1
```

## Common Patterns

### 1. Top K Elements
```python
# K largest: use min-heap of size K
def k_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap

# Or use built-in
def k_largest(nums, k):
    return heapq.nlargest(k, nums)
```

### 2. Merge K Sorted Lists
```python
def merge_k_sorted(lists):
    heap = []
    # Initialize with first from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Add next from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result
```

### 3. Running Median (Two Heaps)
```python
class MedianFinder:
    def __init__(self):
        self.small = []  # Max-heap (negated)
        self.large = []  # Min-heap

    def add_num(self, num):
        # Add to max-heap
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

### 4. Task Scheduling
```python
def task_scheduler(tasks, n):
    from collections import Counter

    freq = Counter(tasks)
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

        for count in temp:
            heapq.heappush(heap, count)

        time += (n + 1) if heap else len(temp)

    return time
```

### 5. K Closest Points
```python
def k_closest(points, k):
    # Use max-heap of size K
    # Store (-distance, point)
    heap = []

    for x, y in points:
        dist = x*x + y*y
        heapq.heappush(heap, (-dist, [x, y]))
        if len(heap) > k:
            heapq.heappop(heap)

    return [point for _, point in heap]
```

### 6. Meeting Rooms
```python
def min_meeting_rooms(intervals):
    if not intervals:
        return 0

    intervals.sort()  # Sort by start time
    heap = []  # Track end times

    for start, end in intervals:
        # If room available, reuse it
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)

    return len(heap)
```

### 7. Kth Largest in Stream
```python
class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)

        # Keep only K largest
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

## Problem Recognition

| Keywords | Pattern | Heap Type |
|----------|---------|-----------|
| "K largest" | Top K | Min-heap size K |
| "K smallest" | Top K | Max-heap size K |
| "Kth largest element" | Top K | Min-heap size K |
| "Top K frequent" | Top K + Counter | Min-heap size K |
| "Merge K sorted" | K-way merge | Min-heap |
| "Find median" | Two heaps | Max + Min heap |
| "Meeting rooms" | Interval scheduling | Min-heap (end times) |
| "Task scheduler" | Greedy scheduling | Max-heap (frequencies) |
| "K closest points" | Top K with distance | Max-heap size K |
| "Smallest range" | K pointers | Min-heap |

## Array Index Formulas

```python
# For 0-indexed array:
parent(i) = (i - 1) // 2
left_child(i) = 2 * i + 1
right_child(i) = 2 * i + 2

# For 1-indexed array:
parent(i) = i // 2
left_child(i) = 2 * i
right_child(i) = 2 * i + 1
```

## Common Edge Cases

- Empty input: `[]`
- Single element: `[x]`
- K equals array length: Return entire array
- K larger than array: Return all elements
- All same values: Heap still works
- Negative numbers: Works fine
- Duplicate values: Works fine
- K = 1: Find minimum/maximum
- Real-time stream: Use heap for dynamic data

## Time Complexity Goals

| Problem | Naive | With Heap |
|---------|-------|-----------|
| K largest | O(n log n) sort | O(n log k) |
| Merge K sorted | O(NK log NK) | O(NK log K) |
| Kth largest | O(n log n) sort | O(n log k) or O(n) quickselect |
| Running median | O(n²) | O(n log n) |
| Meeting rooms | O(n²) | O(n log n) |

## Heap vs Alternatives

| Need | Use Heap | Don't Use |
|------|----------|-----------|
| Top K elements | Yes - O(n log k) | Full sort O(n log n) |
| Find min/max once | No - just scan O(n) | Don't need heap |
| Maintain min/max | Yes - O(log n) updates | Sorted array O(n) updates |
| Full sorting | No | Use sort() instead |
| Arbitrary search | No - O(n) | Use hash map O(1) |
| Range queries | No | Use segment tree |

## Common Mistakes

### 1. Forgetting Min-Heap Default
```python
# BAD: Thinking heapq is max-heap
heapq.heappush(heap, num)
max_val = heapq.heappop(heap)  # Actually gives minimum!

# GOOD: Negate for max-heap
heapq.heappush(heap, -num)
max_val = -heapq.heappop(heap)
```

### 2. Building Heap Inefficiently
```python
# BAD: O(n log n)
heap = []
for num in nums:
    heapq.heappush(heap, num)

# GOOD: O(n)
heap = nums[:]
heapq.heapify(heap)
```

### 3. Wrong Heap for Top K
```python
# K largest: use MIN-heap
# K smallest: use MAX-heap (negated)

# BAD: Using max-heap for K largest
for num in nums:
    heapq.heappush(heap, -num)
    if len(heap) > k:
        heapq.heappop(heap)  # Removes largest!

# GOOD: Use min-heap for K largest
for num in nums:
    heapq.heappush(heap, num)
    if len(heap) > k:
        heapq.heappop(heap)  # Removes smallest, keeps K largest
```

### 4. Not Handling Empty Heap
```python
# BAD: Crash on empty
max_val = heap[0]

# GOOD: Check first
max_val = heap[0] if heap else None
```

### 5. Modifying Heap Directly
```python
# BAD: Don't modify heap array directly
heap[0] = new_value  # Breaks heap property!

# GOOD: Use heapq operations
heapq.heapreplace(heap, new_value)
```

## Interview Template

```python
def solve_with_heap(data, k):
    import heapq

    # 1. Decide min-heap or max-heap
    heap = []  # Min-heap
    # For max-heap: negate values

    # 2. Handle edge cases
    if not data or k <= 0:
        return []

    # 3. Build/populate heap
    for item in data:
        heapq.heappush(heap, item)

        # For top-K: maintain size K
        if len(heap) > k:
            heapq.heappop(heap)

    # 4. Extract results
    result = []
    while heap:
        result.append(heapq.heappop(heap))

    return result
```

## Key Insights

### Top K Pattern
- **K largest**: Min-heap of size K (top is Kth largest, rest are larger)
- **K smallest**: Max-heap of size K (top is Kth smallest, rest are smaller)
- **Intuition**: Heap top is the "gatekeeper" for being in top K

### Two Heap Pattern
- **Use case**: Find median, percentiles, split data
- **Structure**: Max-heap for lower half, min-heap for upper half
- **Balance**: Keep sizes equal or differ by 1
- **Median**: Average of tops (even) or top of larger heap (odd)

### K-Way Merge Pattern
- **Use case**: Merge K sorted lists/streams
- **Heap size**: K elements (one from each source)
- **Process**: Pop minimum, push next from same source
- **Complexity**: O(N log K) where N is total elements

### Scheduling Pattern
- **Use case**: Task scheduling, meeting rooms
- **Max-heap**: For frequencies (schedule most frequent first)
- **Min-heap**: For end times (track resource availability)
- **Greedy**: Always pick highest priority available

## Quick Wins

1. **Top K in O(n log k)**: Use heap instead of O(n log n) sort
2. **Running median in O(log n)**: Two heaps instead of O(n) insertion sort
3. **Merge K in O(N log K)**: Heap instead of O(N log N) full sort
4. **nlargest/nsmallest**: Use built-in heapq functions
5. **Build heap in O(n)**: Use heapify() instead of repeated push

## LeetCode Categories

### Must-Know (Easy/Medium)
- Kth Largest Element (215) - Top K pattern
- Top K Frequent Elements (347) - Top K + Counter
- Merge K Sorted Lists (23) - K-way merge
- Find Median from Data Stream (295) - Two heaps
- Task Scheduler (621) - Scheduling pattern

### Good Practice (Medium)
- K Closest Points (973) - Top K with distance
- Kth Largest in Stream (703) - Streaming data
- Meeting Rooms II (253) - Interval scheduling
- Reorganize String (767) - Greedy scheduling
- Sort Characters by Frequency (451) - Top K + sorting

### Advanced (Hard)
- Sliding Window Maximum (239) - Heap vs deque tradeoff
- Smallest Range (632) - K-way merge variant
- IPO (502) - Greedy with heaps
- The Skyline Problem (218) - Complex heap application

## Space-Time Tradeoffs

| Approach | Time | Space | When to Use |
|----------|------|-------|-------------|
| Heap | O(n log k) | O(k) | K << n, streaming |
| Sort | O(n log n) | O(1) or O(n) | Need all sorted |
| Quickselect | O(n) avg | O(1) | Single Kth element |
| Bucket sort | O(n) | O(n) | Limited value range |

## Memory Tips

- **Heap shape**: Complete binary tree, like a pyramid
- **Min-heap root**: Smallest on top (like water flowing down)
- **Max-heap root**: Largest on top (like a mountain peak)
- **Top K largest**: Min-heap guards the gate, kicks out smallest
- **Two heaps median**: Left max-heap, right min-heap, balanced scales
- **Merge K sorted**: Heap is a tournament bracket finding the winner
