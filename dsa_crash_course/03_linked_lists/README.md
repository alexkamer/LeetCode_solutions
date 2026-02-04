# Linked Lists

Linked lists are fundamental data structures that store elements in nodes, where each node points to the next node in the sequence. Unlike arrays, linked lists don't require contiguous memory and excel at insertions and deletions.

## What Are Linked Lists?

A **linked list** is a linear data structure where elements (nodes) are connected via pointers. Each node contains:
1. **Data** - The value stored in the node
2. **Pointer(s)** - Reference to the next (and sometimes previous) node

### Types of Linked Lists

#### 1. Singly Linked List

Each node points to the next node. The last node points to `None`.

```
HEAD -> [1|•] -> [2|•] -> [3|•] -> [4|None]
```

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

**Pros:**
- Simple implementation
- Less memory per node (one pointer)
- Efficient forward traversal

**Cons:**
- Can only traverse forward
- No direct access to previous node

#### 2. Doubly Linked List

Each node has pointers to both next and previous nodes.

```
       ←----------←----------←----------←
None ←-|•|1|•|- ←-|•|2|•|- ←-|•|3|•|- ←-|•|4|•|-> None
       →----------→----------→----------→
```

```python
class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

**Pros:**
- Bidirectional traversal
- Easier deletion (have reference to previous node)
- Can traverse backward

**Cons:**
- More memory (two pointers per node)
- More complex implementation
- More pointers to maintain

#### 3. Circular Linked List

Last node points back to the first node, forming a circle.

```
     ┌─────────────────────┐
     ↓                     ↑
HEAD -> [1|•] -> [2|•] -> [3|•]
```

**Use cases:**
- Round-robin scheduling
- Circular buffers
- Music playlists on repeat

### Node Structure in Python

```python
# Standard singly linked list node (most common in interviews)
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Creating a linked list: 1 -> 2 -> 3 -> None
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)

# Or using a helper function
def create_linked_list(values):
    """Create a linked list from a list of values."""
    dummy = ListNode(0)
    current = dummy
    for val in values:
        current.next = ListNode(val)
        current = current.next
    return dummy.next

head = create_linked_list([1, 2, 3, 4, 5])
```

## Time Complexity

| Operation | Array | Singly Linked List | Doubly Linked List |
|-----------|-------|-------------------|-------------------|
| Access by index | O(1) | O(n) | O(n) |
| Search | O(n) | O(n) | O(n) |
| Insert at head | O(n) | O(1) | O(1) |
| Insert at tail | O(1)* | O(n) or O(1)** | O(1)*** |
| Insert at position | O(n) | O(n) | O(n) |
| Delete at head | O(n) | O(1) | O(1) |
| Delete at tail | O(1) | O(n) | O(1)*** |
| Delete at position | O(n) | O(n) | O(n) |

*Amortized for dynamic arrays
**O(1) if we maintain a tail pointer
***With tail pointer

## Space Complexity

- **Singly Linked List**: O(n) where n is number of nodes (one pointer per node)
- **Doubly Linked List**: O(n) where n is number of nodes (two pointers per node)
- Most linked list algorithms use O(1) extra space (just a few pointers)

## When to Use Linked Lists vs Arrays

### Use Linked Lists When:

1. **Frequent insertions/deletions at beginning** - O(1) vs O(n) for arrays
2. **Unknown or dynamic size** - No reallocation needed
3. **No need for random access** - Sequential access is sufficient
4. **Memory is fragmented** - Don't need contiguous memory
5. **Implementing queues/stacks** - Natural fit

### Use Arrays When:

1. **Need random access** - O(1) access by index
2. **Iterate frequently** - Better cache locality
3. **Memory is limited** - No pointer overhead
4. **Binary search needed** - Requires random access
5. **Size is known/fixed** - Arrays more efficient

## Common Patterns and Techniques

### 1. Two Pointer (Fast and Slow)

Use two pointers moving at different speeds to solve problems.

```python
def find_middle(head):
    """
    Find the middle node using fast/slow pointers.
    Slow moves 1 step, fast moves 2 steps.
    When fast reaches end, slow is at middle.
    """
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow  # Middle node
```

**When to use:**
- Finding middle of list
- Detecting cycles
- Finding kth from end
- Checking for palindrome

**Key insight:** When fast pointer reaches end (moving 2x speed), slow pointer is at middle.

### 2. Dummy Node

Use a dummy/sentinel node to simplify edge cases.

```python
def remove_elements(head, val):
    """
    Remove all nodes with value = val.
    Dummy node simplifies head deletion.
    """
    dummy = ListNode(0)
    dummy.next = head
    current = dummy

    while current.next:
        if current.next.val == val:
            current.next = current.next.next
        else:
            current = current.next

    return dummy.next  # New head
```

**When to use:**
- Operations that might modify head
- Deleting nodes
- Merging lists
- Inserting at arbitrary positions

**Why it helps:** Eliminates special case handling for head node.

### 3. Reversal

Reverse a linked list iteratively or recursively.

```python
def reverse_iterative(head):
    """
    Iterative reversal using three pointers.

    Time: O(n), Space: O(1)
    """
    prev = None
    current = head

    while current:
        # Save next node
        next_node = current.next
        # Reverse the pointer
        current.next = prev
        # Move prev and current forward
        prev = current
        current = next_node

    return prev  # New head

def reverse_recursive(head):
    """
    Recursive reversal.

    Time: O(n), Space: O(n) for call stack
    """
    # Base case: empty list or single node
    if not head or not head.next:
        return head

    # Recursively reverse rest of list
    new_head = reverse_recursive(head.next)

    # Reverse the connection
    head.next.next = head
    head.next = None

    return new_head
```

**When to use:**
- Reverse entire list
- Reverse sublist (between positions)
- Palindrome checking
- Reordering problems

### 4. Multiple Passes

Sometimes multiple passes simplify the problem.

```python
def remove_nth_from_end(head, n):
    """
    Remove nth node from end using two passes.

    Pass 1: Count total nodes
    Pass 2: Remove node at position (length - n)
    """
    # Pass 1: Get length
    length = 0
    current = head
    while current:
        length += 1
        current = current.next

    # Special case: remove head
    if length == n:
        return head.next

    # Pass 2: Find and remove node
    current = head
    for _ in range(length - n - 1):
        current = current.next
    current.next = current.next.next

    return head
```

**Alternative:** Use two pointers n nodes apart (one pass).

### 5. Runner Technique

Use two pointers starting at different positions or moving at same speed.

```python
def reorder_list(head):
    """
    Reorder list: L0 → L1 → ... → Ln-1 → Ln
    to: L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...

    Strategy:
    1. Find middle (slow/fast pointers)
    2. Reverse second half
    3. Merge two halves
    """
    if not head or not head.next:
        return

    # Step 1: Find middle
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Step 2: Reverse second half
    second = reverse_iterative(slow.next)
    slow.next = None

    # Step 3: Merge
    first = head
    while second:
        temp1, temp2 = first.next, second.next
        first.next = second
        second.next = temp1
        first, second = temp1, temp2
```

### 6. Cycle Detection (Floyd's Algorithm)

Detect cycles using fast and slow pointers.

```python
def has_cycle(head):
    """
    Detect cycle using Floyd's algorithm.
    If there's a cycle, fast and slow will meet.
    """
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False

def detect_cycle_start(head):
    """
    Find the node where cycle begins.

    Math: When they meet, reset one pointer to head.
    Move both at same speed; they'll meet at cycle start.
    """
    slow = fast = head

    # Find meeting point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle

    # Find cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow
```

**Why this works:** Mathematical proof based on distances traveled.

### 7. Merge Technique

Merge two or more sorted lists.

```python
def merge_two_lists(l1, l2):
    """
    Merge two sorted lists.
    Use dummy node for simplicity.
    """
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    # Attach remaining nodes
    current.next = l1 if l1 else l2

    return dummy.next
```

## Essential Techniques

### Traversal

```python
# Print all values
def print_list(head):
    current = head
    values = []
    while current:
        values.append(str(current.val))
        current = current.next
    print(" -> ".join(values))

# Convert to Python list
def to_list(head):
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result
```

### Finding Length

```python
def get_length(head):
    length = 0
    current = head
    while current:
        length += 1
        current = current.next
    return length
```

### Finding Nth Node from End (One Pass)

```python
def nth_from_end(head, n):
    """
    Use two pointers n nodes apart.
    """
    # Move first pointer n steps ahead
    first = head
    for _ in range(n):
        if not first:
            return None
        first = first.next

    # Move both pointers until first reaches end
    second = head
    while first:
        first = first.next
        second = second.next

    return second
```

### Checking for Palindrome

```python
def is_palindrome(head):
    """
    1. Find middle using slow/fast
    2. Reverse second half
    3. Compare both halves
    """
    # Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    second = reverse_iterative(slow)

    # Compare
    first = head
    while second:  # second half might be shorter
        if first.val != second.val:
            return False
        first = first.next
        second = second.next

    return True
```

## Edge Cases to Consider

1. **Empty list** - `head = None`
2. **Single node** - `head.next = None`
3. **Two nodes** - Minimum for some operations
4. **Cycle** - Infinite loop if not handled
5. **Even vs odd length** - Middle node calculation
6. **Head modification** - When head gets deleted/changed
7. **Same values** - All nodes have same value
8. **Overlapping lists** - Intersection problems
9. **Memory management** - In languages like C++, need to free nodes

## Problem-Solving Strategies

### Step 1: Understand the Problem

- Draw the list on paper
- Trace through examples
- Identify edge cases

### Step 2: Choose a Pattern

- Does it involve finding middle? → Fast/slow pointers
- Modifying/deleting head? → Dummy node
- Detecting cycle? → Floyd's algorithm
- Merging lists? → Two pointers with comparison
- Reversing? → Iterative with three pointers

### Step 3: Handle Edge Cases

- Check for `None` before accessing `node.next`
- Use dummy node to simplify head operations
- Consider empty list and single node

### Step 4: Optimize

- Can you do it in one pass instead of two?
- Can you use O(1) space instead of O(n)?
- Is recursion appropriate (consider call stack)?

## Common Mistakes to Avoid

1. **Losing references** - Save `next` before modifying pointers
   ```python
   # WRONG
   current.next = current.next.next  # Lost reference to next node

   # RIGHT
   next_node = current.next
   current.next = next_node.next
   ```

2. **Not checking for None**
   ```python
   # WRONG
   if head.next.val == target:  # Crashes if head.next is None

   # RIGHT
   if head.next and head.next.val == target:
   ```

3. **Infinite loops in cycles**
   ```python
   # Always have a termination condition
   while current:  # Good
   while True:     # Dangerous without break condition
   ```

4. **Forgetting to return new head**
   ```python
   def reverse(head):
       # ... reversal logic ...
       return prev  # Don't forget to return new head!
   ```

5. **Off-by-one errors**
   - Be careful with loop conditions
   - Draw out small examples to verify

## Comparison with Arrays

| Aspect | Array | Linked List |
|--------|-------|-------------|
| Memory | Contiguous | Scattered |
| Access | O(1) by index | O(n) sequential only |
| Insert at start | O(n) | O(1) |
| Insert at end | O(1)* | O(n) or O(1)** |
| Delete | O(n) | O(1) if have pointer |
| Memory overhead | None | One/two pointers per node |
| Cache friendliness | Excellent | Poor |
| Resizing | Expensive | Not needed |

*Amortized
**With tail pointer

## Linked Lists in Python

Python doesn't have a built-in linked list (uses `list` which is a dynamic array). For interviews:

```python
# Node definition (usually provided)
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Helper to create list from array
def create_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Helper to convert list to array (for testing)
def list_to_array(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result
```

## LeetCode Problem Categories

### Easy
- Reverse Linked List (206)
- Merge Two Sorted Lists (21)
- Remove Linked List Elements (203)
- Middle of the Linked List (876)
- Palindrome Linked List (234)

### Medium
- Add Two Numbers (2)
- Remove Nth Node From End (19)
- Reorder List (143)
- Odd Even Linked List (328)
- Swap Nodes in Pairs (24)
- Sort List (148)

### Hard
- Merge k Sorted Lists (23)
- Reverse Nodes in k-Group (25)
- Copy List with Random Pointer (138)

## Interview Tips

1. **Always draw it out** - Visualize pointer changes
2. **Use descriptive variable names** - `prev`, `current`, `next_node`
3. **Check for None** - Before accessing `.next`
4. **Consider dummy node** - Simplifies many problems
5. **Test with small examples** - Empty, one node, two nodes
6. **Trace through your code** - Step by step with example
7. **Ask about constraints** - Can list have cycles? Sorted?

## Related Topics

- **Stacks and Queues** - Can be implemented with linked lists
- **Hash Tables** - Often use linked lists for collision handling
- **Trees** - Similar pointer-based structure
- **Graphs** - Adjacency lists use similar concepts

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems!