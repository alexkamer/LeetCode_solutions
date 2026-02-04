# Greedy Algorithms

Greedy algorithms make locally optimal choices at each step with the hope of finding a global optimum. They are powerful tools for optimization problems and often provide elegant, efficient solutions when applicable.

## 📖 What is a Greedy Algorithm?

A **greedy algorithm** builds up a solution piece by piece, always choosing the next piece that offers the most immediate benefit. The key characteristic is making the locally optimal choice at each step without reconsidering previous choices.

### Key Characteristics

- **Locally optimal choice** - At each step, make the choice that looks best right now
- **No backtracking** - Once a choice is made, it's never reconsidered
- **Irrevocable decisions** - Committed choices cannot be undone
- **Hope for global optimum** - The sequence of local optima leads to a global optimum

### Simple Example: Coin Change

Given coins of denominations [25, 10, 5, 1] and amount 41:
- **Greedy approach**: Take largest coin possible at each step
  - Take 25 → remaining 16
  - Take 10 → remaining 6
  - Take 5 → remaining 1
  - Take 1 → done
  - Result: 4 coins [25, 10, 5, 1]

This works for standard US coins, but greedy doesn't always work for arbitrary denominations!

## 🎯 When Does Greedy Work?

Greedy algorithms work when a problem exhibits two key properties:

### 1. Greedy Choice Property

**Definition**: A global optimum can be arrived at by making locally optimal choices.

In other words, you can assemble a globally optimal solution by repeatedly making locally optimal choices. You don't need to know about future choices to make the current choice.

**Example (Activity Selection):**
- When selecting non-overlapping activities, choosing the activity that ends earliest is always safe
- This choice never prevents us from finding an optimal solution

### 2. Optimal Substructure

**Definition**: An optimal solution to the problem contains optimal solutions to subproblems.

This means that after making a greedy choice, you're left with a smaller problem of the same type.

**Example (Fractional Knapsack):**
- Take items by value/weight ratio
- After taking an item (or fraction), the remaining problem is the same: maximize value with remaining capacity

### Testing If Greedy Works

1. **Make the greedy choice** - Identify what the locally optimal choice is
2. **Prove it's safe** - Show this choice is part of some optimal solution
3. **Solve the subproblem** - Show the remaining problem has the same structure
4. **Counterexample test** - Try to find a case where greedy fails

## 🔄 Greedy vs Dynamic Programming

Both require **optimal substructure**, but they differ in how they make choices:

| Aspect | Greedy | Dynamic Programming |
|--------|--------|-------------------|
| **Choices** | Irrevocable, made once | All possibilities explored |
| **Future knowledge** | Not needed | Considers all future consequences |
| **Efficiency** | Usually O(n) or O(n log n) | Often O(n²) or higher |
| **Correctness** | Hard to prove, doesn't always work | Always finds optimal if formulated correctly |
| **When to use** | When greedy choice property holds | When greedy doesn't work |

### Classic Comparison: Knapsack Problem

**0/1 Knapsack (must take whole item):**
- Greedy: Take by value/weight ratio → **DOESN'T WORK**
- DP: Try all combinations → **WORKS**
- Counterexample: capacity=10, items=[{w:9,v:10}, {w:5,v:6}, {w:5,v:6}]
  - Greedy: Takes first item (ratio 1.11) → value 10
  - Optimal: Takes last two items → value 12

**Fractional Knapsack (can take portions):**
- Greedy: Take by value/weight ratio → **WORKS**
- DP: Not needed
- Taking highest ratio first is always optimal

## 📋 Proving Greedy Correctness

### Method 1: Exchange Argument (Greedy Stays Ahead)

Prove that swapping any non-greedy choice with a greedy choice maintains or improves the solution.

**Template:**
1. Suppose optimal solution differs from greedy solution
2. Find first point where they differ
3. Show you can exchange optimal's choice with greedy's choice
4. Prove new solution is at least as good
5. Conclude greedy solution is optimal

**Example (Activity Selection):**
```
Claim: Choosing activity with earliest finish time is optimal

Proof:
- Let A = greedy solution (earliest finish first)
- Let O = some optimal solution
- If A ≠ O, let a₁ be first activity in A, o₁ be first in O
- If a₁ ≠ o₁, then finish(a₁) ≤ finish(o₁) (greedy choice)
- We can replace o₁ with a₁ in O
- This leaves at least as much time for remaining activities
- Therefore, modified O is still optimal
- By induction, greedy is optimal
```

### Method 2: Induction

Prove that at each step, the greedy choice maintains optimality.

**Template:**
1. **Base case**: First greedy choice is part of some optimal solution
2. **Inductive hypothesis**: After k greedy choices, we have part of optimal solution
3. **Inductive step**: The (k+1)th greedy choice maintains this property
4. **Conclusion**: Full greedy solution is optimal

### Method 3: Contradiction

Assume greedy is not optimal, derive a contradiction.

**Template:**
1. Assume greedy solution is not optimal
2. Let optimal solution differ from greedy
3. Show this leads to a contradiction
4. Conclude greedy must be optimal

## 🎨 Common Greedy Patterns

### 1. Interval Scheduling

**Problem Type**: Select maximum number of non-overlapping intervals

**Greedy Strategy**: Always pick the interval that ends earliest

**Why it works**: Earliest end leaves maximum room for future choices

```python
def max_non_overlapping_intervals(intervals):
    """
    Select maximum number of non-overlapping intervals.

    Time: O(n log n) for sorting
    Space: O(1) excluding input
    """
    if not intervals:
        return 0

    # Sort by end time
    intervals.sort(key=lambda x: x[1])

    count = 1
    last_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start >= last_end:  # Non-overlapping
            count += 1
            last_end = end

    return count
```

**Variations:**
- Minimum number of intervals to remove (n - max_non_overlapping)
- Minimum meeting rooms needed (count maximum overlaps)
- Maximum profit with weighted intervals

### 2. Huffman Coding / Merging

**Problem Type**: Combine elements with minimum cost, where cost of combining depends on sizes

**Greedy Strategy**: Always combine the two smallest elements

**Why it works**: Smallest elements should be deepest in tree to minimize total cost

```python
import heapq

def minimum_cost_to_merge(arr):
    """
    Minimum cost to merge all elements into one.
    Cost of merging two elements is their sum.

    Time: O(n log n)
    Space: O(n)
    """
    if len(arr) <= 1:
        return 0

    heap = list(arr)
    heapq.heapify(heap)

    total_cost = 0

    while len(heap) > 1:
        # Take two smallest
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)

        # Merge them
        merged = first + second
        total_cost += merged

        # Put back
        heapq.heappush(heap, merged)

    return total_cost
```

**Variations:**
- Huffman encoding (build optimal prefix-free code)
- Merge stones
- Connect ropes with minimum cost

### 3. Two-Pointer / Partitioning

**Problem Type**: Partition or rearrange elements optimally

**Greedy Strategy**: Process from extremes (largest and smallest)

```python
def array_pair_sum(nums):
    """
    Pair elements to maximize sum of minimums.
    [1,2,3,4] → (1,2), (3,4) → min(1,2) + min(3,4) = 1+3 = 4

    Greedy: Sort and pair consecutive elements.

    Time: O(n log n)
    Space: O(1)
    """
    nums.sort()
    return sum(nums[i] for i in range(0, len(nums), 2))
```

**Variations:**
- Assign cookies (smallest cookie to smallest greed)
- Boats to save people (heaviest + lightest)
- Two city scheduling

### 4. Maximize/Minimize with Constraints

**Problem Type**: Achieve maximum/minimum value subject to constraints

**Greedy Strategy**: Sort by relevant metric, process in order

```python
def max_units(box_types, truck_size):
    """
    Maximum units that can be put on truck.
    Each box type has [numberOfBoxes, unitsPerBox].

    Greedy: Take boxes with most units first.

    Time: O(n log n)
    Space: O(1)
    """
    # Sort by units per box (descending)
    box_types.sort(key=lambda x: x[1], reverse=True)

    total_units = 0

    for num_boxes, units_per_box in box_types:
        # Take as many boxes of this type as possible
        boxes_to_take = min(num_boxes, truck_size)
        total_units += boxes_to_take * units_per_box
        truck_size -= boxes_to_take

        if truck_size == 0:
            break

    return total_units
```

**Variations:**
- Maximum ice cream bars
- Task scheduler
- Jump game

### 5. State-Based Greedy

**Problem Type**: Make decisions based on current state

**Greedy Strategy**: Track state, make locally optimal choice based on state

```python
def best_time_to_buy_sell_stock_ii(prices):
    """
    Maximum profit with unlimited transactions.
    Can buy and sell on same day.

    Greedy: Capture every upward movement.

    Time: O(n)
    Space: O(1)
    """
    profit = 0

    for i in range(1, len(prices)):
        # If price increased, capture the profit
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]

    return profit
```

**Variations:**
- Gas station (track running balance)
- Jump game (track maximum reach)
- Candy distribution

## 🚨 When Greedy Fails

Greedy doesn't always work! Here are common scenarios where greedy fails:

### 1. Future Choices Matter

**Problem**: Longest path in a graph
- Greedy: Choose edge with maximum weight
- Issue: May lead to dead end while alternative path is longer

### 2. Dependencies Between Choices

**Problem**: 0/1 Knapsack
- Greedy: Choose by value/weight ratio
- Issue: Can't take fractions, so ratio doesn't guarantee optimal

### 3. Need to Reconsider Decisions

**Problem**: Coin change with arbitrary denominations [1, 3, 4] and amount 6
- Greedy: Take 4, then 1, then 1 → 3 coins
- Optimal: Take 3, then 3 → 2 coins

### 4. Multiple Competing Objectives

**Problem**: Maximize sum while minimizing count
- Greedy on one objective may conflict with the other

## 💡 Greedy Algorithm Design Process

1. **Identify the greedy choice**
   - What is the locally optimal decision?
   - What metric should you optimize at each step?

2. **Define the ordering/selection rule**
   - Sort by finish time? Start time? Ratio? Value?
   - Process largest first or smallest first?

3. **Prove correctness (or test extensively)**
   - Use exchange argument
   - Find counterexamples to disprove
   - Compare with brute force on small inputs

4. **Implement efficiently**
   - Often involves sorting: O(n log n)
   - Sometimes needs heap: O(n log n)
   - Best case: O(n) single pass

5. **Handle edge cases**
   - Empty input
   - Single element
   - All elements same
   - Impossible to satisfy constraints

## 🎓 Problem-Solving Template

```python
def greedy_solution(items):
    """
    General greedy algorithm template.
    """
    # Step 1: Handle edge cases
    if not items:
        return default_value

    # Step 2: Sort by greedy criterion (if needed)
    # Common sorts:
    # - By end time: items.sort(key=lambda x: x.end)
    # - By ratio: items.sort(key=lambda x: x.value/x.weight, reverse=True)
    # - By start time: items.sort(key=lambda x: x.start)
    items.sort(key=lambda x: x.greedy_metric)

    # Step 3: Initialize result and state
    result = initial_value
    state = initial_state

    # Step 4: Process items in greedy order
    for item in items:
        # Make greedy choice based on current state
        if can_take(item, state):
            take(item, state)
            update_result(result, item)

    # Step 5: Return result
    return result
```

## 📊 Complexity Analysis

Most greedy algorithms follow these patterns:

### Time Complexity
- **With sorting**: O(n log n)
- **With heap**: O(n log n) typically, or O(n log k) if k is heap size
- **Single pass**: O(n) if no sorting needed
- **Nested with sorting**: O(n² log n) for complex cases

### Space Complexity
- **In-place sorting**: O(1) extra space (or O(log n) for recursion stack)
- **With heap**: O(n) or O(k) depending on heap size
- **Additional tracking**: O(n) if need to mark/track elements

## 🔍 Recognizing Greedy Problems

Look for these keywords and patterns:

### Keywords
- "Maximum number of..."
- "Minimum number of..."
- "Largest/smallest..."
- "Optimal..."
- "Maximize/minimize..."

### Problem Characteristics
- **Optimization problem** - Looking for max or min
- **Choice at each step** - Can make incremental decisions
- **Local choice seems obvious** - One choice seems clearly better
- **No dependencies** - Current choice doesn't depend on future
- **Monotonic property** - More/less of something is always better

### Red Flags (Greedy Won't Work)
- "Exact count/sum" problems often need DP
- Need to satisfy multiple constraints simultaneously
- Choices have complex dependencies
- Problem asks for "number of ways" (usually DP/combinatorics)

## 🎯 Common Greedy Problem Types

### Easy Problems
- Assign Cookies
- Lemonade Change
- Maximum Units on Truck
- Largest Number (with sorting)

### Medium Problems
- Jump Game
- Jump Game II
- Gas Station
- Partition Labels
- Non-overlapping Intervals
- Meeting Rooms II
- Task Scheduler
- Minimum Number of Arrows

### Hard Problems
- Candy Distribution
- Create Maximum Number
- Remove K Digits
- Smallest Range Covering Elements

## 🛠️ Implementation Tips

### 1. Sorting is Your Friend
Most greedy algorithms start with sorting. Choose the right key:
```python
# By end time
intervals.sort(key=lambda x: x[1])

# By ratio (descending)
items.sort(key=lambda x: x.value/x.weight, reverse=True)

# By multiple criteria
items.sort(key=lambda x: (x.priority, -x.value))
```

### 2. Use Heaps for Dynamic Greedy
When the greedy choice changes as you process:
```python
import heapq

heap = []
for item in items:
    heapq.heappush(heap, (item.priority, item))

while heap:
    priority, item = heapq.heappop(heap)
    process(item)
```

### 3. Track State Carefully
Many greedy algorithms need to track current state:
```python
current_end = 0
max_reach = 0
rooms_needed = 0
```

### 4. Handle Ties Consistently
When elements are equal, ensure consistent behavior:
```python
# Use tuple for stable sorting
items.sort(key=lambda x: (x.primary, x.secondary))
```

## 📚 LeetCode Problem List

### Easy (Foundational)
1. **455. Assign Cookies** - Basic greedy with sorting
2. **860. Lemonade Change** - State-based greedy
3. **1323. Maximum 69 Number** - Simple greedy choice

### Medium (Core Patterns)
4. **55. Jump Game** - Greedy tracking maximum reach
5. **45. Jump Game II** - Greedy with BFS-like approach
6. **134. Gas Station** - Circular array greedy
7. **763. Partition Labels** - Interval merging
8. **435. Non-overlapping Intervals** - Classic interval scheduling
9. **452. Minimum Number of Arrows** - Interval intersection
10. **253. Meeting Rooms II** - Count maximum overlaps
11. **621. Task Scheduler** - Greedy with constraints
12. **406. Queue Reconstruction** - Multi-criteria sorting

### Hard (Advanced)
13. **135. Candy** - Two-pass greedy
14. **402. Remove K Digits** - Monotonic stack greedy
15. **321. Create Maximum Number** - Complex greedy with merging
16. **757. Set Intersection Size** - Interval + set cover

## 💭 Interview Tips

1. **Always ask if greedy works**
   - Don't assume it's greedy just because it's an optimization problem
   - Try to find counterexamples quickly

2. **Explain your greedy choice**
   - What metric are you optimizing locally?
   - Why is this choice safe?

3. **Prove (or convince) correctness**
   - Use exchange argument if you can
   - At minimum, explain intuition
   - Test edge cases mentally

4. **Consider alternatives**
   - Could DP work better?
   - Is brute force feasible for small n?

5. **Analyze complexity**
   - Usually O(n log n) from sorting
   - Mention if you can optimize to O(n)

## 🔗 Related Topics

- **Dynamic Programming** - When greedy doesn't work
- **Sorting** - Foundation of many greedy algorithms
- **Heaps** - For dynamic greedy choices
- **Interval Problems** - Common greedy application
- **Graph Algorithms** - Dijkstra's and Prim's are greedy

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems with detailed explanations and proofs!
