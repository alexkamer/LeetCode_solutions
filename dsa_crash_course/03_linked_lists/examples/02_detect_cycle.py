"""
LeetCode 141: Linked List Cycle
LeetCode 142: Linked List Cycle II

Problem 141:
Given head, the head of a linked list, determine if the linked list has a cycle in it.
There is a cycle in a linked list if there is some node in the list that can be reached
again by continuously following the next pointer.

Return true if there is a cycle in the linked list. Otherwise, return false.

Problem 142:
Given the head of a linked list, return the node where the cycle begins.
If there is no cycle, return null.

Example 1:
Input: head = [3,2,0,-4], pos = 1 (cycle at node with value 2)
Output: true (for 141), node with value 2 (for 142)
Explanation: There is a cycle, where the tail connects to the 1st node (0-indexed).

Example 2:
Input: head = [1,2], pos = 0 (cycle at node with value 1)
Output: true (for 141), node with value 1 (for 142)

Example 3:
Input: head = [1], pos = -1 (no cycle)
Output: false (for 141), null (for 142)

Constraints:
- The number of nodes in the list is in the range [0, 10^4]
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list

Follow-up for 141: Can you solve it using O(1) memory?
Follow-up for 142: Can you solve it without modifying the linked list?
"""


class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head):
    """
    Floyd's Cycle Detection Algorithm (Tortoise and Hare).

    Approach:
    Use two pointers: slow (moves 1 step) and fast (moves 2 steps).
    - If there's no cycle, fast will reach the end (None)
    - If there's a cycle, fast will eventually catch up to slow

    Why this works:
    - In a cycle, fast gains 1 position on slow each iteration
    - They will eventually meet inside the cycle

    Visualization:
    No cycle:
    slow -> 1 -> 2 -> 3 -> None
    fast -------> 3 -> None (reaches end)

    With cycle:
    slow -> 1 -> 2 -> 3 -> 4
                 ^         |
                 |_________|
    fast will eventually catch slow in the cycle

    Time Complexity: O(n)
    - If no cycle: fast reaches end in n/2 steps
    - If cycle: fast catches slow in at most n steps

    Space Complexity: O(1) - only two pointers

    Args:
        head: ListNode - head of the linked list

    Returns:
        bool - True if cycle exists, False otherwise
    """
    if not head or not head.next:
        return False

    slow = fast = head

    while fast and fast.next:
        slow = slow.next        # Move 1 step
        fast = fast.next.next   # Move 2 steps

        if slow == fast:
            return True  # Cycle detected

    return False  # fast reached end, no cycle


def detect_cycle_start(head):
    """
    Find the node where the cycle begins using Floyd's Algorithm.

    Approach:
    1. Use fast/slow pointers to detect if cycle exists
    2. If cycle exists, find the starting node:
       - Reset slow to head
       - Move both slow and fast one step at a time
       - They will meet at the cycle start

    Mathematical Proof:
    Let's say:
    - Distance from head to cycle start = a
    - Distance from cycle start to meeting point = b
    - Remaining cycle length = c
    - Cycle length = b + c

    When they meet:
    - Slow traveled: a + b
    - Fast traveled: a + b + k(b + c) where k is number of full cycles

    Since fast travels twice the distance of slow:
    2(a + b) = a + b + k(b + c)
    a + b = k(b + c)
    a = k(b + c) - b
    a = (k-1)(b + c) + c

    This means distance from head to cycle start (a) equals:
    - Starting from meeting point, going c steps (to cycle start)
    - Plus (k-1) full cycles

    Therefore, if we start one pointer at head and another at meeting point,
    moving both one step at a time, they'll meet at cycle start.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        head: ListNode - head of the linked list

    Returns:
        ListNode - node where cycle begins, or None if no cycle
    """
    if not head or not head.next:
        return None

    slow = fast = head

    # Phase 1: Detect if cycle exists
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            # Cycle detected, proceed to phase 2
            break
    else:
        # No cycle found
        return None

    # Phase 2: Find cycle start
    # Reset slow to head, move both one step at a time
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow  # This is the cycle start


def has_cycle_hash_set(head):
    """
    Alternative approach using hash set to track visited nodes.

    Approach:
    Store each visited node in a set.
    If we encounter a node we've seen before, there's a cycle.

    Time Complexity: O(n)
    Space Complexity: O(n) - store all nodes in set

    Note: This approach modifies the list structure in the set,
    but doesn't modify the actual nodes. Less optimal than Floyd's
    algorithm due to space complexity.

    Args:
        head: ListNode - head of the linked list

    Returns:
        bool - True if cycle exists, False otherwise
    """
    visited = set()
    current = head

    while current:
        if current in visited:
            return True  # Found a cycle
        visited.add(current)
        current = current.next

    return False  # Reached end, no cycle


# Helper functions for testing

def create_list_with_cycle(values, pos):
    """
    Create a linked list with a cycle.

    Args:
        values: list of node values
        pos: index where tail should point to (-1 for no cycle)

    Returns:
        ListNode - head of the created list
    """
    if not values:
        return None

    # Create all nodes
    nodes = [ListNode(val) for val in values]

    # Link nodes
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]

    # Create cycle if pos is valid
    if 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]

    return nodes[0]


def get_cycle_length(head):
    """
    Get the length of the cycle if it exists.

    Args:
        head: ListNode - head of the linked list

    Returns:
        int - length of cycle, or 0 if no cycle
    """
    if not has_cycle(head):
        return 0

    slow = fast = head

    # Find meeting point
    while True:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break

    # Count cycle length
    count = 1
    current = slow.next
    while current != slow:
        count += 1
        current = current.next

    return count


def visualize_cycle_detection(head, pos):
    """
    Visualize the cycle detection process.

    Args:
        head: ListNode - head of the list
        pos: int - position where cycle starts (-1 for no cycle)
    """
    print(f"List values: {[node.val for node in get_nodes(head, 10)]}")
    if pos >= 0:
        print(f"Cycle at position: {pos}")
    else:
        print("No cycle")

    print("\nDetecting cycle...")

    # Simulate Floyd's algorithm
    slow = fast = head
    step = 0
    max_steps = 20  # Prevent infinite loop for visualization

    while fast and fast.next and step < max_steps:
        slow = slow.next
        fast = fast.next.next
        step += 1

        print(f"Step {step}: slow at {slow.val if slow else None}, "
              f"fast at {fast.val if fast else None}")

        if slow == fast and slow is not None:
            print(f"Cycle detected at step {step}!")
            print(f"Meeting point value: {slow.val}")

            # Find cycle start
            if pos >= 0:
                cycle_start = detect_cycle_start(head)
                print(f"Cycle starts at node with value: {cycle_start.val}")
            break
    else:
        if step >= max_steps:
            print("(Visualization limited to 20 steps)")
        else:
            print("No cycle found - reached end of list")


def get_nodes(head, limit=10):
    """
    Get up to 'limit' nodes from list (for visualization).

    Args:
        head: ListNode - head of the list
        limit: int - maximum nodes to retrieve

    Returns:
        list of ListNode - retrieved nodes
    """
    nodes = []
    current = head
    visited = set()

    while current and len(nodes) < limit:
        if current in visited:
            break
        nodes.append(current)
        visited.add(current)
        current = current.next

    return nodes


def test_cycle_detection():
    """Test cases for cycle detection."""

    print("Test 1: List with cycle at position 1")
    head = create_list_with_cycle([3, 2, 0, -4], 1)
    assert has_cycle(head) == True
    assert has_cycle_hash_set(head) == True
    cycle_start = detect_cycle_start(head)
    assert cycle_start.val == 2
    print("PASSED\n")

    print("Test 2: List with cycle at position 0")
    head = create_list_with_cycle([1, 2], 0)
    assert has_cycle(head) == True
    cycle_start = detect_cycle_start(head)
    assert cycle_start.val == 1
    print("PASSED\n")

    print("Test 3: Single node with no cycle")
    head = create_list_with_cycle([1], -1)
    assert has_cycle(head) == False
    assert has_cycle_hash_set(head) == False
    assert detect_cycle_start(head) == None
    print("PASSED\n")

    print("Test 4: Multiple nodes with no cycle")
    head = create_list_with_cycle([1, 2, 3, 4, 5], -1)
    assert has_cycle(head) == False
    assert detect_cycle_start(head) == None
    print("PASSED\n")

    print("Test 5: Empty list")
    head = create_list_with_cycle([], -1)
    assert has_cycle(head) == False
    assert detect_cycle_start(head) == None
    print("PASSED\n")

    print("Test 6: Large cycle")
    head = create_list_with_cycle(list(range(100)), 50)
    assert has_cycle(head) == True
    cycle_start = detect_cycle_start(head)
    assert cycle_start.val == 50
    print("PASSED\n")

    print("Test 7: Self-loop (single node cycle)")
    head = create_list_with_cycle([1], 0)
    assert has_cycle(head) == True
    cycle_start = detect_cycle_start(head)
    assert cycle_start.val == 1
    print("PASSED\n")

    print("All tests passed!")


if __name__ == "__main__":
    # Run tests
    test_cycle_detection()

    print("\n" + "="*50)
    print("Visualization Example")
    print("="*50 + "\n")

    # Visualize cycle detection
    print("Example 1: List with cycle")
    head = create_list_with_cycle([3, 2, 0, -4], 1)
    visualize_cycle_detection(head, 1)

    print("\n" + "-"*50 + "\n")

    print("Example 2: List without cycle")
    head = create_list_with_cycle([1, 2, 3, 4], -1)
    visualize_cycle_detection(head, -1)

    print("\n" + "="*50)
    print("Algorithm Comparison")
    print("="*50)

    print("\nFloyd's Cycle Detection (Tortoise and Hare):")
    print("Time: O(n), Space: O(1)")
    print("Pros: Optimal space complexity, elegant")
    print("Cons: Less intuitive")

    print("\nHash Set Approach:")
    print("Time: O(n), Space: O(n)")
    print("Pros: More intuitive, easier to understand")
    print("Cons: Uses extra space")

    print("\nRecommendation: Use Floyd's algorithm for optimal solution")
