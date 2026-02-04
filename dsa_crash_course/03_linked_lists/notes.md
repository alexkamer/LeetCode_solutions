# Linked Lists - Quick Reference

## Complexity Cheat Sheet

### Time Complexity

| Operation | Singly LL | Doubly LL | Array |
|-----------|-----------|-----------|-------|
| Access | O(n) | O(n) | O(1) |
| Search | O(n) | O(n) | O(n) |
| Insert at head | O(1) | O(1) | O(n) |
| Insert at tail | O(n)* | O(1)** | O(1)*** |
| Delete at head | O(1) | O(1) | O(n) |
| Delete at tail | O(n) | O(1)** | O(1) |
| Delete node | O(n) | O(1)**** | O(n) |

*O(1) with tail pointer
**With tail pointer
***Amortized
****If have reference to node

### Space Complexity

- Singly: O(n) - one pointer per node
- Doubly: O(n) - two pointers per node
- Most algorithms: O(1) extra space

## Pattern Recognition

### Use Fast/Slow Pointers When:
- Finding middle of list
- Detecting cycles
- Finding nth from end
- Checking palindrome
- Finding cycle start

### Use Dummy Node When:
- Head might be deleted
- Merging lists
- Removing nodes
- Building new list

### Use Reversal When:
- Reverse entire list
- Reverse sublist
- Palindrome check
- Reordering problems

### Use Runner Technique When:
- Need two pointers at different positions
- Comparing pairs
- K-node operations

## Common Patterns & Templates

### 1. Fast/Slow Pointers

```python
# Find middle
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# Detect cycle
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Nth from end (one pass)
def nth_from_end(head, n):
    first = second = head
    # Move first n steps ahead
    for _ in range(n):
        first = first.next
    # Move both until first reaches end
    while first:
        first = first.next
        second = second.next
    return second
```

### 2. Reversal Template

```python
# Iterative (preferred - O(1) space)
def reverse(head):
    prev = None
    current = head

    while current:
        next_node = current.next  # Save next
        current.next = prev       # Reverse pointer
        prev = current            # Move prev
        current = next_node       # Move current

    return prev  # New head

# Recursive (O(n) call stack)
def reverse_recursive(head):
    if not head or not head.next:
        return head

    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None

    return new_head
```

### 3. Dummy Node Template

```python
def operation_on_list(head):
    dummy = ListNode(0)
    dummy.next = head
    current = dummy

    while current.next:
        # Do operation
        if condition:
            current.next = current.next.next
        else:
            current = current.next

    return dummy.next  # New head
```

### 4. Merge Template

```python
def merge_two_lists(l1, l2):
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

    current.next = l1 if l1 else l2
    return dummy.next
```

### 5. Cycle Detection (Floyd's)

```python
# Detect cycle
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Find cycle start
def detect_cycle_start(head):
    slow = fast = head

    # Find meeting point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle

    # Find start: reset slow to head
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow
```

## Edge Cases Checklist

- [ ] Empty list (head = None)
- [ ] Single node (head.next = None)
- [ ] Two nodes (minimum for some operations)
- [ ] All same values
- [ ] Cycle exists
- [ ] Even vs odd length
- [ ] Head gets modified/deleted
- [ ] Very long list (performance)

## Common Mistakes

1. **Not checking for None**
   ```python
   # WRONG
   if head.next.val == x:

   # RIGHT
   if head.next and head.next.val == x:
   ```

2. **Losing references**
   ```python
   # WRONG - lost reference to next
   current.next = current.next.next

   # RIGHT
   next_node = current.next
   current.next = next_node.next
   ```

3. **Infinite loops**
   ```python
   # Always check termination
   while current:  # Good
   while True:     # Need break condition
   ```

4. **Forgetting return value**
   ```python
   def reverse(head):
       # ... logic ...
       return prev  # Don't forget!
   ```

5. **Off-by-one with middle**
   - For even length, which middle node?
   - Adjust fast pointer initialization

## Problem Categories

### Pattern: Fast/Slow Pointers
- Middle of Linked List
- Linked List Cycle
- Linked List Cycle II
- Happy Number
- Palindrome Linked List

### Pattern: Dummy Node
- Merge Two Sorted Lists
- Remove Linked List Elements
- Partition List
- Insertion Sort List

### Pattern: Reversal
- Reverse Linked List
- Reverse Linked List II
- Swap Nodes in Pairs
- Reverse Nodes in k-Group

### Pattern: Two Pointers
- Remove Nth Node From End
- Intersection of Two Linked Lists
- Delete Node in Linked List

### Pattern: Merge/Divide
- Merge Two Sorted Lists
- Merge k Sorted Lists
- Sort List (merge sort)

## Node Definition

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## Helper Functions

```python
# Create from list
def create_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Convert to list
def to_list(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

# Print list
def print_list(head):
    values = []
    while head:
        values.append(str(head.val))
        head = head.next
    print(" -> ".join(values))

# Get length
def get_length(head):
    length = 0
    while head:
        length += 1
        head = head.next
    return length
```

## Interview Strategy

1. **Draw it out** - Always visualize
2. **Ask questions**
   - Can it be empty?
   - Can there be cycles?
   - Is it sorted?
   - Do we know the length?

3. **Choose pattern**
   - Finding middle? → Fast/slow
   - Removing nodes? → Dummy
   - Reversing? → Three pointers
   - Cycle? → Floyd's

4. **Handle edge cases**
   - Empty list
   - Single node
   - Head modification

5. **Trace through code**
   - Use small example (2-3 nodes)
   - Check pointer movements

## Quick Tips

- Always check `None` before accessing `.next`
- Use dummy node when head might change
- Save references before modifying pointers
- Fast/slow solves many problems
- Draw pointer movements on paper
- Test with empty, single, two nodes
- Consider iterative over recursive (O(1) space)

## When to Use Linked Lists vs Arrays

**Choose Linked Lists:**
- Frequent insertions/deletions at beginning
- Unknown/dynamic size
- No random access needed
- Fragmented memory OK

**Choose Arrays:**
- Need random access
- Frequent iteration
- Memory limited (no pointer overhead)
- Binary search needed

## Top LeetCode Problems

**Must Know (Easy):**
- 206: Reverse Linked List
- 21: Merge Two Sorted Lists
- 141: Linked List Cycle
- 876: Middle of Linked List

**Important (Medium):**
- 2: Add Two Numbers
- 19: Remove Nth Node From End
- 143: Reorder List
- 148: Sort List

**Advanced (Hard):**
- 23: Merge k Sorted Lists
- 25: Reverse Nodes in k-Group