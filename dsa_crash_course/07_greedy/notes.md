# Greedy Algorithms - Quick Reference

## When to Use Greedy

### Greedy Works When:
1. **Greedy Choice Property**: Local optimal choices lead to global optimum
2. **Optimal Substructure**: Problem can be broken into smaller subproblems
3. **No future dependencies**: Current choice doesn't depend on future
4. **Monotonic property**: More/less is always better

### Greedy Fails When:
- Future choices affect current decisions
- Need exact count/sum (usually DP)
- Multiple competing objectives
- Must reconsider past decisions

## Pattern Recognition Guide

| Problem Type | Keywords | Greedy Strategy | Sort By |
|-------------|----------|----------------|---------|
| **Interval Scheduling** | "non-overlapping", "maximum activities" | Pick earliest ending | End time |
| **Interval Removal** | "minimum to remove", "overlap" | Pick earliest ending, remove conflicts | End time |
| **Meeting Rooms** | "minimum rooms", "schedule meetings" | Track overlaps with heap | Start time |
| **Merging/Huffman** | "minimum cost to merge/connect" | Always merge smallest two | N/A (use heap) |
| **Fractional Knapsack** | "maximize value", "can take fractions" | Take best ratio first | Value/weight ratio |
| **Two-Pointer Partition** | "pair elements", "maximize/minimize pairs" | Sort, process extremes | Value |
| **State-Based** | "sequence of operations", "running total" | Track state, single pass | N/A (one pass) |
| **Jump/Reach** | "can reach end", "minimum jumps" | Track maximum reachable | N/A (one pass) |

## Common Greedy Patterns

### 1. Interval Scheduling (Sort by End)
```python
# Maximum non-overlapping intervals
intervals.sort(key=lambda x: x[1])  # Sort by end
count, last_end = 1, intervals[0][1]
for start, end in intervals[1:]:
    if start >= last_end:
        count += 1
        last_end = end
```

**Use when**: Select maximum activities, minimum removals
**Examples**: Non-overlapping Intervals, Minimum Arrows

### 2. Meeting Rooms (Heap for Overlaps)
```python
# Minimum meeting rooms needed
import heapq
intervals.sort()  # Sort by start
heap = []  # Track end times of ongoing meetings
for start, end in intervals:
    if heap and heap[0] <= start:
        heapq.heappop(heap)  # Room freed
    heapq.heappush(heap, end)
return len(heap)
```

**Use when**: Count maximum overlaps, resource allocation
**Examples**: Meeting Rooms II, Car Pooling

### 3. Huffman/Merging (Min Heap)
```python
# Minimum cost to merge all elements
import heapq
heapq.heapify(arr)
cost = 0
while len(arr) > 1:
    first = heapq.heappop(arr)
    second = heapq.heappop(arr)
    merged = first + second
    cost += merged
    heapq.heappush(arr, merged)
```

**Use when**: Combine elements, cost depends on size
**Examples**: Connect Ropes, Merge Stones

### 4. Jump Game (Track Maximum Reach)
```python
# Can reach end?
max_reach = 0
for i in range(len(nums)):
    if i > max_reach:
        return False
    max_reach = max(max_reach, i + nums[i])
return True

# Minimum jumps
jumps, current_end, farthest = 0, 0, 0
for i in range(len(nums) - 1):
    farthest = max(farthest, i + nums[i])
    if i == current_end:
        jumps += 1
        current_end = farthest
```

**Use when**: Reach problems, minimum steps
**Examples**: Jump Game I/II, Video Stitching

### 5. Gas Station (Running Balance)
```python
# Can complete circuit?
total, current, start = 0, 0, 0
for i in range(len(gas)):
    diff = gas[i] - cost[i]
    total += diff
    current += diff
    if current < 0:
        start = i + 1
        current = 0
return start if total >= 0 else -1
```

**Use when**: Circular array, running total, find starting point
**Examples**: Gas Station, Jump Game

### 6. Partition Labels (Last Occurrence)
```python
# Partition into maximum parts
last = {c: i for i, c in enumerate(s)}
start, end = 0, 0
result = []
for i, c in enumerate(s):
    end = max(end, last[c])
    if i == end:
        result.append(end - start + 1)
        start = i + 1
```

**Use when**: Split into parts, each part has property
**Examples**: Partition Labels, Merge Intervals

### 7. Two-Pointer Pairing
```python
# Pair elements optimally
nums.sort()
# Consecutive pairs
result = sum(nums[i] for i in range(0, len(nums), 2))

# Or opposite ends
left, right = 0, len(nums) - 1
while left < right:
    process_pair(nums[left], nums[right])
    left += 1
    right -= 1
```

**Use when**: Pair elements, assignment problems
**Examples**: Assign Cookies, Boats to Save People

### 8. State Capture (Every Profit)
```python
# Buy and sell stock (multiple transactions)
profit = 0
for i in range(1, len(prices)):
    if prices[i] > prices[i-1]:
        profit += prices[i] - prices[i-1]
```

**Use when**: Capture every opportunity, accumulate gains
**Examples**: Best Time to Buy Sell Stock II

## Greedy vs DP Decision Tree

```
Is it an optimization problem (max/min)?
├─ Yes
│  ├─ Can you make locally optimal choices?
│  │  ├─ Yes
│  │  │  ├─ Do future choices affect current?
│  │  │  │  ├─ No → Try GREEDY
│  │  │  │  └─ Yes → Use DP
│  │  │  └─ No
│  │  └─ Need exact count/sum? → Use DP
│  └─ Not optimization
└─ No → Not greedy or DP
```

## Correctness Proof Templates

### Exchange Argument
```
1. Assume optimal solution O differs from greedy G
2. Find first difference
3. Exchange O's choice with G's choice
4. Show new solution is at least as good
5. Conclude G is optimal
```

### Induction
```
1. Base: First greedy choice is in some optimal solution
2. Hypothesis: After k choices, have part of optimal
3. Step: (k+1)th greedy choice maintains this
4. Conclude: Full greedy is optimal
```

## Complexity Quick Reference

| Pattern | Time | Space |
|---------|------|-------|
| **Sort + process** | O(n log n) | O(1) |
| **Heap operations** | O(n log n) or O(n log k) | O(n) or O(k) |
| **Single pass** | O(n) | O(1) |
| **Two pass** | O(n) | O(n) if need tracking |

## Edge Cases Checklist

- [ ] Empty input
- [ ] Single element
- [ ] All elements same
- [ ] Already optimal
- [ ] Impossible scenario (no solution)
- [ ] Ties (equal priorities)
- [ ] Negative values (if applicable)
- [ ] Circular/wraparound cases

## Interview Template

```python
def greedy_solution(items):
    # 1. Edge cases
    if not items:
        return default
    
    # 2. Sort (if needed)
    items.sort(key=lambda x: x.criterion)
    
    # 3. Initialize
    result = 0
    state = initial_state
    
    # 4. Greedy loop
    for item in items:
        if can_take(item, state):
            result = update(result, item)
            state = update_state(state, item)
    
    # 5. Return
    return result
```

## Common Greedy Moves

### Sorting Strategies
```python
# By end time (intervals)
intervals.sort(key=lambda x: x[1])

# By ratio (knapsack)
items.sort(key=lambda x: x.value/x.weight, reverse=True)

# By start time (meeting rooms)
intervals.sort(key=lambda x: x[0])

# Multi-criteria
items.sort(key=lambda x: (x.primary, -x.secondary))
```

### Heap Strategies
```python
import heapq

# Min heap (default)
heapq.heappush(heap, value)
smallest = heapq.heappop(heap)

# Max heap (negate values)
heapq.heappush(heap, -value)
largest = -heapq.heappop(heap)

# Heap with objects
heapq.heappush(heap, (priority, item))
```

### State Tracking
```python
# Running total
current_sum = 0
for item in items:
    current_sum += item.value
    if current_sum meets condition:
        take_action()

# Maximum reach
max_reach = 0
for i in range(len(arr)):
    if i > max_reach:
        return False
    max_reach = max(max_reach, i + arr[i])

# Last occurrence
last_pos = {item: i for i, item in enumerate(items)}
```

## Red Flags (Probably Not Greedy)

1. "Count number of ways" → Combinatorics/DP
2. "Exact sum equals target" → DP (subset sum)
3. "All possible solutions" → Backtracking
4. "Minimum operations to make equal" → Often DP
5. Multiple interleaved dependencies → DP
6. Need to explore all paths → DFS/BFS/DP

## Problem Recognition Keywords

### Definitely Consider Greedy
- "Maximum number of non-overlapping"
- "Minimum number to remove"
- "Earliest/latest deadline"
- "Optimal assignment"
- "Can reach end"

### Maybe Greedy
- "Maximize/minimize" (could be DP)
- "Optimal" (could be DP)
- "Fewest/most" (could be BFS/DP)

### Probably Not Greedy
- "Count ways"
- "All possible"
- "Exactly equal to"
- "Minimum operations to transform"

## Quick Problem Lookup

| LeetCode # | Name | Pattern |
|-----------|------|---------|
| 55 | Jump Game | Track max reach |
| 45 | Jump Game II | BFS-like greedy |
| 134 | Gas Station | Running balance |
| 135 | Candy | Two-pass greedy |
| 253 | Meeting Rooms II | Heap for overlaps |
| 435 | Non-overlapping Intervals | Sort by end |
| 452 | Minimum Arrows | Sort by end |
| 455 | Assign Cookies | Two-pointer |
| 621 | Task Scheduler | Frequency greedy |
| 763 | Partition Labels | Last occurrence |
| 860 | Lemonade Change | State tracking |

## Testing Strategy

1. **Try small examples** - Work through manually
2. **Look for counterexamples** - Try to break greedy
3. **Test edge cases** - Empty, single, all same
4. **Compare with brute force** - For small inputs
5. **Prove or explain** - Why greedy works

## When Stuck

1. **Identify the choice** - What decision are you making?
2. **What makes a choice good?** - Define your metric
3. **Try sorting** - By different criteria
4. **Try examples** - Walk through small cases
5. **Consider DP** - If greedy seems wrong
