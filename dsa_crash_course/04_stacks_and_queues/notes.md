# Stacks and Queues - Quick Reference

## Complexity Cheat Sheet

### Stack Operations
```
Push:       O(1)
Pop:        O(1)
Peek:       O(1)
Search:     O(n)
Space:      O(n)
```

### Queue Operations
```
Enqueue:    O(1)
Dequeue:    O(1)  (with deque, O(n) with list!)
Peek:       O(1)
Search:     O(n)
Space:      O(n)
```

## Python Quick Reference

### Stack (use list or deque)
```python
# Create
stack = []

# Operations
stack.append(x)              # Push - O(1)
x = stack.pop()              # Pop - O(1)
top = stack[-1]              # Peek - O(1)
is_empty = not stack         # Check empty - O(1)
size = len(stack)            # Size - O(1)
```

### Queue (ALWAYS use deque!)
```python
from collections import deque

# Create
queue = deque()

# Operations
queue.append(x)              # Enqueue - O(1)
x = queue.popleft()          # Dequeue - O(1)
front = queue[0]             # Peek front - O(1)
is_empty = not queue         # Check empty - O(1)
size = len(queue)            # Size - O(1)
```

### Deque (double-ended queue)
```python
from collections import deque

dq = deque([1, 2, 3])
dq = deque(maxlen=5)         # Bounded deque

dq.append(x)                 # Add right - O(1)
dq.appendleft(x)             # Add left - O(1)
dq.pop()                     # Remove right - O(1)
dq.popleft()                 # Remove left - O(1)
dq[0], dq[-1]                # Access ends - O(1)
dq.rotate(1)                 # Rotate right - O(k)
dq.rotate(-1)                # Rotate left - O(k)
```

## Common Patterns

### 1. Monotonic Stack Template

**Monotonic Decreasing** (for next greater element):
```python
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []  # Store indices

    for i, num in enumerate(nums):
        # Pop smaller elements
        while stack and nums[stack[-1]] < num:
            idx = stack.pop()
            result[idx] = num
        stack.append(i)

    return result
```

**Monotonic Increasing** (for next smaller element):
```python
def next_smaller(nums):
    result = [-1] * len(nums)
    stack = []

    for i, num in enumerate(nums):
        # Pop larger elements
        while stack and nums[stack[-1]] > num:
            idx = stack.pop()
            result[idx] = num
        stack.append(i)

    return result
```

### 2. Valid Parentheses Template
```python
def is_valid(s):
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}

    for char in s:
        if char in pairs:
            stack.append(char)
        elif not stack or pairs[stack.pop()] != char:
            return False

    return not stack
```

### 3. Min/Max Stack Template
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return self.min_stack[-1]
```

### 4. Queue Using Two Stacks Template
```python
class MyQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x):
        self.in_stack.append(x)

    def pop(self):
        self._move()
        return self.out_stack.pop()

    def peek(self):
        self._move()
        return self.out_stack[-1]

    def _move(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
```

### 5. Sliding Window Maximum Template (Deque)
```python
from collections import deque

def max_sliding_window(nums, k):
    result = []
    dq = deque()  # Store indices

    for i, num in enumerate(nums):
        # Remove elements outside window
        if dq and dq[0] <= i - k:
            dq.popleft()

        # Remove smaller elements (not useful)
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Add to result when window is full
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

### 6. BFS Template
```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        # Process node

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**Level-Order BFS:**
```python
def level_order(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level = []
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

### 7. Expression Evaluation Template
```python
def eval_rpn(tokens):
    stack = []
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b)
    }

    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))

    return stack[0]
```

## Problem Recognition Guide

### Use Stack When You See:
- "Valid parentheses/brackets"
- "Next greater/smaller element"
- "Remove adjacent duplicates"
- "Evaluate expression"
- "Daily temperatures"
- "Stock span"
- "Largest rectangle"
- "Trapping rain water"
- "Decode string"
- "Asteroid collision"
- Anything with nested structures or matching pairs

### Use Queue When You See:
- "Level-order traversal"
- "BFS" or "shortest path" in unweighted graph
- "First-come-first-served"
- "Task scheduling"
- "Moving average"
- "Number of islands"
- "Rotting oranges"
- "Word ladder"
- Anything requiring processing in arrival order

### Use Deque When You See:
- "Sliding window maximum/minimum"
- "Access both ends"
- "Palindrome checking"
- "Shortest subarray"
- Anything requiring O(1) operations at both ends

### Use Monotonic Stack When You See:
- "Next greater/smaller element"
- "Previous greater/smaller element"
- "Maximum/minimum in range"
- "Stock span problem"
- "Largest rectangle in histogram"
- "Trapping rain water"
- "Daily temperatures"
- "Remove K digits"

## Key Insights

### Stack Insights
1. Stack = Last In, First Out (LIFO)
2. Perfect for reversing order
3. Natural for nested/recursive structures
4. Can convert recursion to iteration
5. Use for parsing and matching

### Queue Insights
1. Queue = First In, First Out (FIFO)
2. Perfect for level-by-level processing
3. Use for BFS (shortest path in unweighted graph)
4. Always use `deque` in Python (not list!)
5. Natural for scheduling and streaming

### Monotonic Stack Insights
1. Maintains increasing or decreasing order
2. O(n) time for next greater/smaller problems
3. Each element pushed and popped at most once
4. Key: what to do when popping (found answer!)
5. Decreasing stack → next greater
6. Increasing stack → next smaller

### Deque Insights
1. Double-ended queue (both ends accessible)
2. O(1) for append/pop at both ends
3. Perfect for sliding window problems
4. Can serve as stack AND queue
5. Bounded deque auto-removes oldest

## Common Edge Cases

1. Empty input
2. Single element
3. All elements the same
4. Nested structures
5. Invalid/unmatched input
6. Maximum/minimum values
7. Duplicate elements
8. Very large input

## Time Complexity Rules

### Stack
- Push: O(1)
- Pop: O(1)
- Peek: O(1)
- All n elements: O(n) total (amortized O(1) each)

### Queue
- Enqueue: O(1)
- Dequeue: O(1) with deque, O(n) with list
- Peek: O(1)

### Monotonic Stack
- Overall: O(n) for n elements
- Each element: Push once, pop once = O(1) amortized

### BFS
- Time: O(V + E) for graph (V=vertices, E=edges)
- Space: O(V) for queue

## When to Use What

| Problem Type | Data Structure | Example |
|--------------|---------------|---------|
| Matching pairs | Stack | Valid parentheses |
| Next greater | Monotonic stack | Daily temperatures |
| DFS | Stack | Graph traversal |
| BFS | Queue | Level-order |
| Both ends access | Deque | Sliding window max |
| LIFO needed | Stack | Undo/redo |
| FIFO needed | Queue | Task scheduling |
| Min/max tracking | Min/max stack | Stock prices |

## Python Gotchas

1. **DON'T use list for queue**: `list.pop(0)` is O(n)!
2. **DO use deque for queue**: `deque.popleft()` is O(1)
3. **Check empty before pop**: Avoid IndexError
4. **Peek doesn't remove**: Use `stack[-1]` or `queue[0]`
5. **deque indexing**: Fast at ends, slow in middle
6. **maxlen deque**: Auto-removes when full (bounded)

## Interview Checklist

- [ ] Clarify input constraints (size, values, types)
- [ ] Identify if LIFO (stack) or FIFO (queue) is needed
- [ ] Consider monotonic stack for next greater/smaller
- [ ] Remember to use deque for queues in Python
- [ ] Check edge cases (empty, single element)
- [ ] Verify time/space complexity
- [ ] Test with examples
- [ ] Consider auxiliary data structures (min stack, etc.)
