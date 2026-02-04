"""
LeetCode 19: Remove Nth Node From End of List

Problem:
Given the head of a linked list, remove the nth node from the end of the list
and return its head.

Example 1:
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
Explanation: Remove the 4th node (2nd from end)

Example 2:
Input: head = [1], n = 1
Output: []
Explanation: Remove the only node

Example 3:
Input: head = [1,2], n = 1
Output: [1]
Explanation: Remove the last node

Constraints:
- The number of nodes in the list is sz
- 1 <= sz <= 30
- 0 <= Node.val <= 100
- 1 <= n <= sz

Follow-up: Could you do this in one pass?
"""


class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_nth_from_end_one_pass(head, n):
    """
    Remove nth node from end using two pointers (one pass).

    Approach:
    Use two pointers separated by n nodes:
    1. Move fast pointer n steps ahead
    2. Move both pointers until fast reaches end
    3. Slow pointer will be at node before the one to remove
    4. Skip the target node

    Key Insight: When fast is at the end, slow is n+1 nodes from end
    (which is the node before the one we want to remove)

    Visualization for [1,2,3,4,5], n=2:

    Step 1: Move fast n steps ahead
    slow          fast
     ↓             ↓
     1 -> 2 -> 3 -> 4 -> 5 -> None

    Step 2: Move both until fast reaches end
                slow       fast
                 ↓          ↓
     1 -> 2 -> 3 -> 4 -> 5 -> None

    Step 3: Remove node after slow
     1 -> 2 -> 3 -> X -> 5 -> None
                   ↓
                  (4)

    Use dummy node to handle edge case where head is removed.

    Time Complexity: O(L) where L is list length - single pass
    Space Complexity: O(1) - only using pointers

    Args:
        head: ListNode - head of the linked list
        n: int - position from end to remove (1-indexed)

    Returns:
        ListNode - head of modified list
    """
    # Use dummy node to handle head removal
    dummy = ListNode(0)
    dummy.next = head

    fast = slow = dummy

    # Move fast n+1 steps ahead (so slow will be at node before target)
    for _ in range(n + 1):
        fast = fast.next

    # Move both until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next

    # Remove the target node
    slow.next = slow.next.next

    return dummy.next


def remove_nth_from_end_two_pass(head, n):
    """
    Remove nth node from end using two passes.

    Approach:
    Pass 1: Count total nodes
    Pass 2: Navigate to (length - n)th node and remove next

    This is more straightforward but requires two passes.

    Time Complexity: O(L) - two passes, still linear
    Space Complexity: O(1)

    Args:
        head: ListNode - head of the linked list
        n: int - position from end to remove (1-indexed)

    Returns:
        ListNode - head of modified list
    """
    # Pass 1: Count nodes
    length = 0
    current = head
    while current:
        length += 1
        current = current.next

    # Special case: removing head
    if length == n:
        return head.next

    # Pass 2: Navigate to node before target
    current = head
    for _ in range(length - n - 1):
        current = current.next

    # Remove target node
    current.next = current.next.next

    return head


def remove_nth_from_end_recursive(head, n):
    """
    Remove nth node from end using recursion.

    Approach:
    1. Recursively reach the end
    2. Count back from end as recursion unwinds
    3. When count equals n, skip that node

    Time Complexity: O(L)
    Space Complexity: O(L) for call stack

    Args:
        head: ListNode - head of the linked list
        n: int - position from end to remove (1-indexed)

    Returns:
        ListNode - head of modified list
    """
    def helper(node):
        """
        Returns: (new_head, distance_from_end)
        """
        if not node:
            return None, 0

        # Recurse to end
        next_node, distance = helper(node.next)

        # Count distance from end
        distance += 1

        # If this is the node before target, skip next
        if distance == n + 1:
            node.next = next_node
            return node, distance

        # If this is the target node, skip it
        if distance == n:
            return next_node, distance

        # Otherwise, keep this node
        node.next = next_node
        return node, distance

    new_head, _ = helper(head)
    return new_head if new_head else head.next


# Helper functions for testing

def create_list(values):
    """Create a linked list from a list of values."""
    if not values:
        return None

    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next

    return head


def list_to_array(head):
    """Convert linked list to Python list."""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def print_list(head):
    """Print linked list in readable format."""
    values = []
    current = head
    while current:
        values.append(str(current.val))
        current = current.next
    print(" -> ".join(values) if values else "Empty list")


def visualize_removal(values, n):
    """
    Visualize the removal process.

    Args:
        values: list of values for the list
        n: int - position from end to remove
    """
    print(f"Original list: {values}")
    print(f"Remove {n}{'st' if n == 1 else 'nd' if n == 2 else 'rd' if n == 3 else 'th'} from end")

    # Calculate which node will be removed
    length = len(values)
    remove_index = length - n
    print(f"This is node at index {remove_index} (0-indexed): {values[remove_index]}")

    print("\nOne-pass algorithm visualization:")
    print("="*50)

    head = create_list(values)
    dummy = ListNode(0)
    dummy.next = head

    # Visualize pointer movement
    fast = slow = dummy
    nodes = [dummy] + [node for node in get_all_nodes(head)]

    # Step 1: Move fast n+1 steps
    print(f"\nStep 1: Move fast pointer {n+1} steps ahead")
    for i in range(n + 1):
        fast = fast.next
    print(f"Slow at: dummy, Fast at: {fast.val if fast else 'None'}")

    # Step 2: Move both until fast reaches end
    print(f"\nStep 2: Move both pointers until fast reaches end")
    step = 1
    while fast:
        fast = fast.next
        slow = slow.next
        print(f"  Move {step}: Slow at {slow.val}, Fast at {fast.val if fast else 'None'}")
        step += 1

    # Step 3: Remove
    print(f"\nStep 3: Slow is at node before target")
    print(f"Remove node: {slow.next.val}")
    slow.next = slow.next.next

    print("\nResult:", end=" ")
    print_list(dummy.next)


def get_all_nodes(head):
    """Get all nodes in a list (for visualization)."""
    nodes = []
    current = head
    while current:
        nodes.append(current)
        current = current.next
    return nodes


def test_remove_nth_from_end():
    """Test cases for removing nth node from end."""

    approaches = [
        ("One pass (two pointers)", remove_nth_from_end_one_pass),
        ("Two pass", remove_nth_from_end_two_pass),
        ("Recursive", remove_nth_from_end_recursive)
    ]

    for name, func in approaches:
        print(f"\nTesting {name}:")

        # Test 1: Remove from middle
        head = create_list([1, 2, 3, 4, 5])
        result = func(head, 2)
        assert list_to_array(result) == [1, 2, 3, 5]
        print("Test 1 (remove from middle): PASSED")

        # Test 2: Remove only node
        head = create_list([1])
        result = func(head, 1)
        assert list_to_array(result) == []
        print("Test 2 (remove only node): PASSED")

        # Test 3: Remove last node
        head = create_list([1, 2])
        result = func(head, 1)
        assert list_to_array(result) == [1]
        print("Test 3 (remove last): PASSED")

        # Test 4: Remove first node (head)
        head = create_list([1, 2, 3])
        result = func(head, 3)
        assert list_to_array(result) == [2, 3]
        print("Test 4 (remove head): PASSED")

        # Test 5: Large list
        head = create_list(list(range(1, 31)))
        result = func(head, 15)
        expected = list(range(1, 16)) + list(range(17, 31))
        assert list_to_array(result) == expected
        print("Test 5 (large list): PASSED")

        # Test 6: Remove from end of two nodes
        head = create_list([1, 2])
        result = func(head, 2)
        assert list_to_array(result) == [2]
        print("Test 6 (two nodes, remove first): PASSED")

    print("\nAll tests passed!")


def compare_approaches():
    """Compare different removal approaches."""
    print("\n" + "="*50)
    print("Approach Comparison")
    print("="*50)

    print("\n1. One Pass with Two Pointers (RECOMMENDED)")
    print("   Time: O(L), Space: O(1)")
    print("   Pros: Single pass, optimal, elegant")
    print("   Cons: Slightly less intuitive")
    print("   Best for: Interviews, production code")

    print("\n2. Two Pass")
    print("   Time: O(L), Space: O(1)")
    print("   Pros: Very intuitive, straightforward")
    print("   Cons: Requires two passes (still O(L) though)")
    print("   Best for: When clarity is most important")

    print("\n3. Recursive")
    print("   Time: O(L), Space: O(L) call stack")
    print("   Pros: Interesting approach, functional style")
    print("   Cons: Extra space, more complex")
    print("   Best for: Academic interest, functional programming")


if __name__ == "__main__":
    # Run tests
    test_remove_nth_from_end()

    print("\n" + "="*50)
    print("Visualization Example")
    print("="*50 + "\n")

    # Visualize removal
    visualize_removal([1, 2, 3, 4, 5], 2)

    print("\n" + "-"*50 + "\n")

    visualize_removal([1, 2, 3, 4, 5], 5)

    # Compare approaches
    compare_approaches()

    print("\n" + "="*50)
    print("Key Insights")
    print("="*50)
    print("\n1. Two pointers n nodes apart is a powerful pattern")
    print("2. When fast reaches end, slow is n+1 from end")
    print("3. Dummy node handles edge case of removing head")
    print("4. This pattern works for many 'nth from end' problems")
    print("5. Drawing the pointers on paper makes it clear")

    print("\n" + "="*50)
    print("Common Mistakes")
    print("="*50)
    print("\n1. Moving fast exactly n steps (need n+1 for one-pass)")
    print("2. Not using dummy node (complicates head removal)")
    print("3. Off-by-one errors with pointer positions")
    print("4. Not checking if n is valid (problem guarantees it)")
