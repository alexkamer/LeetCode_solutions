"""
LeetCode 206: Reverse Linked List

Problem:
Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:
Input: head = [1,2]
Output: [2,1]

Example 3:
Input: head = []
Output: []

Constraints:
- The number of nodes in the list is in the range [0, 5000]
- -5000 <= Node.val <= 5000

Follow-up: A linked list can be reversed either iteratively or recursively. Could you implement both?
"""


class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_iterative(head):
    """
    Iterative approach using three pointers.

    Approach:
    Use three pointers: prev (initially None), current (head), and next_node.
    For each node:
    1. Save the next node
    2. Reverse the current node's pointer to point to prev
    3. Move prev and current one step forward

    Visualization:
    Initial:  None <- prev   current -> next
                      1  ->  2  ->  3  ->  None

    Step 1:   None <- 1      2  ->  3  ->  None
                     prev  current

    Step 2:   None <- 1 <- 2      3  ->  None
                          prev  current

    Step 3:   None <- 1 <- 2 <- 3      None
                               prev  current

    Time Complexity: O(n) - visit each node once
    Space Complexity: O(1) - only use constant extra space

    Args:
        head: ListNode - head of the linked list

    Returns:
        ListNode - head of the reversed list
    """
    prev = None
    current = head

    while current:
        # Save next node before we change the pointer
        next_node = current.next

        # Reverse the pointer
        current.next = prev

        # Move prev and current forward
        prev = current
        current = next_node

    # prev is now pointing to the new head
    return prev


def reverse_recursive(head):
    """
    Recursive approach.

    Approach:
    The key insight is that reversing a list can be broken down into:
    1. Reverse the rest of the list (recursive call)
    2. Make the next node point back to current node
    3. Set current node's next to None

    Visualization:
    reverse(1 -> 2 -> 3 -> None)
        reverse(2 -> 3 -> None)
            reverse(3 -> None)
                return 3 (base case)
            3.next.next = 3, so: 3 <- 2
            2.next = None
            return 3
        2.next.next = 2, so: 3 <- 2 <- 1
        1.next = None
        return 3

    Time Complexity: O(n) - visit each node once
    Space Complexity: O(n) - recursion call stack

    Args:
        head: ListNode - head of the linked list

    Returns:
        ListNode - head of the reversed list
    """
    # Base case: empty list or single node
    if not head or not head.next:
        return head

    # Recursively reverse the rest of the list
    new_head = reverse_recursive(head.next)

    # Make the next node point back to current node
    # head.next is the node after head
    # head.next.next is what the node after head points to
    # We make it point back to head
    head.next.next = head

    # Set current node's next to None (will be updated by previous call)
    head.next = None

    return new_head


def reverse_recursive_cleaner(head, prev=None):
    """
    Alternative recursive approach with cleaner logic.

    Approach:
    Similar to iterative but using recursion:
    - Base case: when current node is None, return prev (new head)
    - Recursive case: save next, reverse pointer, recurse with next

    Time Complexity: O(n)
    Space Complexity: O(n) for call stack

    Args:
        head: ListNode - current node
        prev: ListNode - previous node (default None)

    Returns:
        ListNode - head of reversed list
    """
    # Base case: reached end of list
    if not head:
        return prev

    # Save next node
    next_node = head.next

    # Reverse pointer
    head.next = prev

    # Recurse with next node
    return reverse_recursive_cleaner(next_node, head)


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


def visualize_reversal(head):
    """
    Visualize the reversal process step by step.

    Args:
        head: ListNode - head of list to reverse
    """
    print("Original list:", end=" ")
    print_list(head)

    # Show iterative process
    print("\nIterative reversal process:")
    prev = None
    current = head
    step = 1

    while current:
        next_node = current.next
        current.next = prev

        # Print current state
        print(f"Step {step}: reversed", end=" ")
        print_list(prev)

        prev = current
        current = next_node
        step += 1

    print("Final reversed list:", end=" ")
    print_list(prev)


def test_reverse():
    """Test cases for reverse linked list."""

    print("Test 1: Normal list [1,2,3,4,5]")
    head = create_list([1, 2, 3, 4, 5])
    reversed_head = reverse_iterative(head)
    assert list_to_array(reversed_head) == [5, 4, 3, 2, 1]
    print("Iterative: PASSED")

    head = create_list([1, 2, 3, 4, 5])
    reversed_head = reverse_recursive(head)
    assert list_to_array(reversed_head) == [5, 4, 3, 2, 1]
    print("Recursive: PASSED\n")

    print("Test 2: Two nodes [1,2]")
    head = create_list([1, 2])
    reversed_head = reverse_iterative(head)
    assert list_to_array(reversed_head) == [2, 1]
    print("Iterative: PASSED")

    head = create_list([1, 2])
    reversed_head = reverse_recursive(head)
    assert list_to_array(reversed_head) == [2, 1]
    print("Recursive: PASSED\n")

    print("Test 3: Single node [1]")
    head = create_list([1])
    reversed_head = reverse_iterative(head)
    assert list_to_array(reversed_head) == [1]
    print("Iterative: PASSED")

    head = create_list([1])
    reversed_head = reverse_recursive(head)
    assert list_to_array(reversed_head) == [1]
    print("Recursive: PASSED\n")

    print("Test 4: Empty list []")
    head = create_list([])
    reversed_head = reverse_iterative(head)
    assert list_to_array(reversed_head) == []
    print("Iterative: PASSED")

    head = create_list([])
    reversed_head = reverse_recursive(head)
    assert list_to_array(reversed_head) == []
    print("Recursive: PASSED\n")

    print("Test 5: Large list")
    values = list(range(1, 101))
    head = create_list(values)
    reversed_head = reverse_iterative(head)
    assert list_to_array(reversed_head) == list(reversed(values))
    print("Iterative: PASSED")

    head = create_list(values)
    reversed_head = reverse_recursive(head)
    assert list_to_array(reversed_head) == list(reversed(values))
    print("Recursive: PASSED\n")

    print("Test 6: List with duplicates [1,1,1,2,2]")
    head = create_list([1, 1, 1, 2, 2])
    reversed_head = reverse_iterative(head)
    assert list_to_array(reversed_head) == [2, 2, 1, 1, 1]
    print("PASSED\n")

    print("All tests passed!")


if __name__ == "__main__":
    # Run tests
    test_reverse()

    print("\n" + "="*50)
    print("Visualization Example")
    print("="*50)

    # Visualize reversal
    head = create_list([1, 2, 3, 4])
    visualize_reversal(head)

    print("\n" + "="*50)
    print("Comparison of Approaches")
    print("="*50)

    print("\nIterative Approach:")
    print("Pros: O(1) space, easier to understand")
    print("Cons: None")
    print("\nRecursive Approach:")
    print("Pros: Elegant, concise code")
    print("Cons: O(n) space for call stack, risk of stack overflow")
    print("\nRecommendation: Use iterative in production, know both for interviews")
