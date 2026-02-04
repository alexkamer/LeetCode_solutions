# Stacks and Queues

Stacks and queues are fundamental linear data structures that control how elements are added and removed. They're essential for many algorithms and appear frequently in coding interviews, especially for problems involving ordering, parsing, and state management.

## 📖 What Are Stacks?

A **stack** is a linear data structure that follows the **LIFO (Last In, First Out)** principle. The last element added is the first one to be removed, like a stack of plates.

### Key Properties

- **LIFO ordering** - Last element added is first removed
- **Two main operations** - Push (add) and pop (remove)
- **One access point** - Only the top element is accessible
- **No random access** - Cannot access middle elements directly

### Stack Operations

```python
# Using Python list as stack
stack = []

# Push - O(1)
stack.append(5)
stack.append(10)
stack.append(15)

# Pop - O(1)
top = stack.pop()  # Returns 15

# Peek - O(1)
top = stack[-1] if stack else None  # Returns 10 without removing

# Check if empty - O(1)
is_empty = len(stack) == 0

# Size - O(1)
size = len(stack)
```

### When to Use a Stack

- **Function call stack** - Recursion, backtracking
- **Undo/Redo operations** - Text editors, browser history
- **Expression evaluation** - Parentheses matching, infix to postfix
- **DFS traversal** - Graph/tree depth-first search
- **Monotonic stack problems** - Next greater element, stock span
- **Syntax parsing** - Compilers, interpreters

## 📖 What Are Queues?

A **queue** is a linear data structure that follows the **FIFO (First In, First Out)** principle. The first element added is the first one to be removed, like a line of people waiting.

### Key Properties

- **FIFO ordering** - First element added is first removed
- **Two main operations** - Enqueue (add) and dequeue (remove)
- **Two access points** - Front (remove) and back (add)
- **No random access** - Cannot access middle elements directly

### Queue Operations

```python
from collections import deque

# Using deque (recommended for queues in Python)
queue = deque()

# Enqueue - O(1)
queue.append(5)
queue.append(10)
queue.append(15)

# Dequeue - O(1)
first = queue.popleft()  # Returns 5

# Peek - O(1)
first = queue[0] if queue else None  # Returns 10 without removing

# Check if empty - O(1)
is_empty = len(queue) == 0

# Size - O(1)
size = len(queue)
```

### When to Use a Queue

- **BFS traversal** - Graph/tree breadth-first search
- **Task scheduling** - Job queues, process scheduling
- **Stream processing** - Real-time data processing
- **Request handling** - Web servers, print queues
- **Level-order traversal** - Trees and graphs
- **Sliding window problems** - With deque for both ends access

## 🐍 Python's collections.deque

Python's `collections.deque` (double-ended queue) is the recommended implementation for both stacks and queues. It's optimized for O(1) operations at both ends.

### Why Use deque?

- **O(1) operations at both ends** - Unlike list which is O(n) for `pop(0)`
- **Thread-safe** - Atomic append/pop operations
- **Memory efficient** - Better than list for frequent operations
- **Versatile** - Can be used as stack, queue, or deque

### deque Features

```python
from collections import deque

# Create deque
dq = deque([1, 2, 3])
dq = deque(maxlen=5)  # Bounded deque (auto-removes oldest)

# Add elements - O(1)
dq.append(4)       # Add to right: [1, 2, 3, 4]
dq.appendleft(0)   # Add to left: [0, 1, 2, 3, 4]

# Remove elements - O(1)
dq.pop()           # Remove from right: returns 4
dq.popleft()       # Remove from left: returns 0

# Extend - O(k) where k is length of iterable
dq.extend([5, 6])        # Add multiple to right
dq.extendleft([7, 8])    # Add multiple to left (reversed)

# Rotate - O(k)
dq.rotate(1)   # Rotate right by 1
dq.rotate(-1)  # Rotate left by 1

# Access - O(1) at ends, O(n) in middle
first = dq[0]
last = dq[-1]
```

### Stack with deque

```python
from collections import deque

stack = deque()
stack.append(x)     # Push
x = stack.pop()     # Pop
top = stack[-1]     # Peek
```

### Queue with deque

```python
from collections import deque

queue = deque()
queue.append(x)        # Enqueue
x = queue.popleft()    # Dequeue
front = queue[0]       # Peek
```

## ⏱️ Time Complexity

### Stack Operations

| Operation | List | deque | Notes |
|-----------|------|-------|-------|
| Push/append | O(1)* | O(1) | Amortized for list |
| Pop | O(1) | O(1) | From top/right end |
| Peek | O(1) | O(1) | Access top element |
| Search | O(n) | O(n) | Must scan through |
| Size | O(1) | O(1) | Stored as attribute |

### Queue Operations

| Operation | List | deque | Notes |
|-----------|------|-------|-------|
| Enqueue/append | O(1)* | O(1) | Amortized for list |
| Dequeue | O(n) | O(1) | List needs shifting, deque doesn't |
| Peek front | O(1) | O(1) | Access first element |
| Peek back | O(1) | O(1) | Access last element |
| Search | O(n) | O(n) | Must scan through |
| Size | O(1) | O(1) | Stored as attribute |

**Note:** For queues, always prefer `deque` over `list` because `list.pop(0)` is O(n).

## 💾 Space Complexity

- **Stack/Queue**: O(n) where n is the number of elements
- **Auxiliary space**: Usually O(1) unless copying/cloning

## 🎯 Common Patterns and Techniques

### 1. Monotonic Stack

A stack that maintains elements in monotonically increasing or decreasing order.

**When to use:**
- Next greater/smaller element problems
- Stock span problems
- Largest rectangle in histogram
- Daily temperatures

**Pattern:**
```python
def next_greater_elements(nums):
    """
    Find the next greater element for each element.
    Maintains decreasing monotonic stack.
    """
    result = [-1] * len(nums)
    stack = []  # Store indices

    for i, num in enumerate(nums):
        # Pop smaller elements - they found their next greater
        while stack and nums[stack[-1]] < num:
            idx = stack.pop()
            result[idx] = num

        stack.append(i)

    return result

# Example: [2, 1, 2, 4, 3] -> [4, 2, 4, -1, -1]
```

**Two types:**
- **Monotonic increasing** - Stack grows in increasing order (pop when current > top)
- **Monotonic decreasing** - Stack grows in decreasing order (pop when current < top)

### 2. Valid Parentheses / Bracket Matching

Use stack to match opening and closing brackets.

**Pattern:**
```python
def is_valid_parentheses(s):
    """
    Check if string has valid parentheses.
    """
    stack = []
    matching = {'(': ')', '[': ']', '{': '}'}

    for char in s:
        if char in matching:
            # Opening bracket - push to stack
            stack.append(char)
        else:
            # Closing bracket - check if matches top
            if not stack or matching[stack.pop()] != char:
                return False

    # Stack should be empty if all matched
    return len(stack) == 0
```

**When to use:**
- Parentheses validation
- HTML/XML tag matching
- Expression parsing

### 3. Min/Max Stack

Stack that can retrieve minimum or maximum in O(1) time.

**Pattern:**
```python
class MinStack:
    """
    Stack with O(1) min retrieval.
    Maintains parallel stack of minimums.
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        # Store current minimum
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

**When to use:**
- Need to track min/max over time
- Sliding window minimum/maximum
- Stock price problems

### 4. Implement Queue Using Stacks

Two stacks can simulate a queue.

**Pattern:**
```python
class QueueUsingStacks:
    """
    Queue implementation using two stacks.
    Amortized O(1) for all operations.
    """
    def __init__(self):
        self.stack_in = []   # For enqueue
        self.stack_out = []  # For dequeue

    def enqueue(self, x):
        self.stack_in.append(x)

    def dequeue(self):
        self._move_if_needed()
        return self.stack_out.pop()

    def peek(self):
        self._move_if_needed()
        return self.stack_out[-1]

    def _move_if_needed(self):
        # Move elements from in to out when out is empty
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
```

**When to use:**
- Understanding amortized analysis
- Interview classic question

### 5. Sliding Window with Deque

Deque is perfect for sliding window problems requiring both ends access.

**When to use:**
- Sliding window maximum/minimum
- Window with constraints on both ends
- Moving average with outlier removal

**Pattern:**
```python
def sliding_window_maximum(nums, k):
    """
    Find maximum in each sliding window of size k.
    Uses deque to maintain decreasing order.
    """
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

### 6. BFS with Queue

Standard pattern for level-order traversal.

**Pattern:**
```python
from collections import deque

def bfs(graph, start):
    """
    Breadth-first search using queue.
    """
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        process(node)  # Do something with node

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

def level_order_traversal(root):
    """
    Tree level-order traversal.
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

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

### 7. Expression Evaluation

Use stack to evaluate expressions.

**Pattern:**
```python
def evaluate_postfix(tokens):
    """
    Evaluate postfix (Reverse Polish) notation.
    Example: ["2", "1", "+", "3", "*"] = (2 + 1) * 3 = 9
    """
    stack = []

    for token in tokens:
        if token in ['+', '-', '*', '/']:
            # Pop two operands
            right = stack.pop()
            left = stack.pop()

            # Compute and push result
            if token == '+':
                stack.append(left + right)
            elif token == '-':
                stack.append(left - right)
            elif token == '*':
                stack.append(left * right)
            else:  # '/'
                stack.append(int(left / right))  # Truncate toward zero
        else:
            # Number - push to stack
            stack.append(int(token))

    return stack[0]
```

## 🚨 Edge Cases to Consider

1. **Empty stack/queue** - Pop from empty
2. **Single element** - Edge case for many operations
3. **All same elements** - For monotonic stack problems
4. **Maximum size constraints** - Memory limits
5. **Negative numbers** - In calculation problems
6. **Integer overflow** - In evaluation problems
7. **Invalid input** - Unmatched brackets, invalid expressions
8. **Circular dependencies** - In dependency resolution problems

## 🎓 When to Use Stack vs Queue

### Use a Stack when:
- Need LIFO behavior (most recent first)
- Implementing recursion iteratively
- Backtracking algorithms
- Parsing nested structures
- Reversing order
- DFS traversal

### Use a Queue when:
- Need FIFO behavior (first come, first served)
- BFS traversal
- Level-order processing
- Task scheduling
- Stream processing
- Shortest path in unweighted graphs

### Use a Deque when:
- Need access to both ends
- Sliding window problems
- Palindrome checking
- Maintaining maximum/minimum in window
- Can serve as both stack and queue

## 📊 Implementation Comparison

### Stack Implementations

| Implementation | Push | Pop | Peek | Space | Notes |
|----------------|------|-----|------|-------|-------|
| Python list | O(1)* | O(1) | O(1) | O(n) | Simple, amortized |
| collections.deque | O(1) | O(1) | O(1) | O(n) | Better for large data |
| Linked list | O(1) | O(1) | O(1) | O(n) | No resize overhead |

### Queue Implementations

| Implementation | Enqueue | Dequeue | Peek | Space | Notes |
|----------------|---------|---------|------|-------|-------|
| Python list | O(1)* | O(n) | O(1) | O(n) | BAD: Slow dequeue |
| collections.deque | O(1) | O(1) | O(1) | O(n) | BEST choice |
| Two stacks | O(1) | O(1)* | O(1) | O(n) | Amortized, interview question |
| Linked list | O(1) | O(1) | O(1) | O(n) | Need tail pointer |

**Always use `collections.deque` for queues in Python!**

## 📚 LeetCode Problem Categories

### Easy
- Valid Parentheses (Stack)
- Implement Queue using Stacks
- Implement Stack using Queues
- Baseball Game
- Remove All Adjacent Duplicates

### Medium
- Min Stack
- Daily Temperatures (Monotonic Stack)
- Evaluate Reverse Polish Notation
- Decode String
- Asteroid Collision
- Basic Calculator II
- Number of Islands (BFS)
- Rotting Oranges (BFS)

### Hard
- Largest Rectangle in Histogram (Monotonic Stack)
- Trapping Rain Water (Monotonic Stack)
- Sliding Window Maximum (Deque)
- Basic Calculator
- Serialize and Deserialize Binary Tree

## 🔧 Python-Specific Tips

```python
from collections import deque

# Creating stacks
stack = []                    # List as stack
stack = deque()              # Deque as stack (better)

# Creating queues
queue = deque()              # ALWAYS use deque for queues
# DON'T use list for queues! pop(0) is O(n)

# Deque tricks
dq = deque(maxlen=5)         # Bounded deque (auto-removes)
dq.rotate(1)                 # Rotate right
dq.rotate(-1)                # Rotate left
list(dq)                     # Convert to list

# Check if empty
if not stack:                # Pythonic way
if len(stack) == 0:          # Explicit way

# Peek without removing
top = stack[-1] if stack else None    # Stack
front = queue[0] if queue else None   # Queue

# Copy stack/queue
new_stack = stack.copy()              # Shallow copy
new_stack = deque(stack)              # Create new deque
```

## 💡 Interview Tips

1. **Clarify the problem**
   - Can I use built-in stack/queue?
   - Are there size constraints?
   - What should happen on empty pop/dequeue?
   - Should I handle invalid input?

2. **Choose the right data structure**
   - Need LIFO? → Stack
   - Need FIFO? → Queue
   - Need both ends? → Deque
   - Need to maintain order? → Monotonic stack

3. **Consider space-time tradeoffs**
   - Extra stack for O(1) min? Worth it
   - Two stacks for queue? Sometimes necessary

4. **Think about patterns**
   - Matching/nesting → Stack
   - Level traversal → Queue
   - Next greater/smaller → Monotonic stack
   - Window problems → Deque

5. **Watch out for edge cases**
   - Empty data structure
   - Single element
   - All elements the same
   - Very large input

6. **Write clean code**
   - Use deque for queues (not list!)
   - Use meaningful names (stack vs queue)
   - Check empty before pop
   - Handle errors gracefully

## 🔗 Related Topics

- **Trees and Graphs** - BFS/DFS traversal
- **Dynamic Programming** - State transitions
- **Recursion** - Call stack, iterative conversion
- **Parsing** - Expression evaluation, syntax checking
- **Binary Search** - Sometimes combined with monotonic stack

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems!
