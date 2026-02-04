"""
LeetCode 21: Merge Two Sorted Lists

Problem:
You are given the heads of two sorted linked lists list1 and list2.
Merge the two lists into one sorted list. The list should be made by
splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:
Input: list1 = [], list2 = []
Output: []

Example 3:
Input: list1 = [], list2 = [0]
Output: [0]

Constraints:
- The number of nodes in both lists is in the range [0, 50]
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order
"""


class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists_iterative(list1, list2):
    """
    Merge two sorted lists iteratively using a dummy node.

    Approach:
    1. Create a dummy node to simplify edge cases
    2. Use a pointer to build the merged list
    3. Compare values from both lists and attach the smaller one
    4. Move the pointer forward
    5. Attach any remaining nodes from either list

    Visualization:
    list1: 1 -> 2 -> 4
    list2: 1 -> 3 -> 4

    Step 1: dummy -> 1 (from list1)
    Step 2: dummy -> 1 -> 1 (from list2)
    Step 3: dummy -> 1 -> 1 -> 2 (from list1)
    Step 4: dummy -> 1 -> 1 -> 2 -> 3 (from list2)
    Step 5: dummy -> 1 -> 1 -> 2 -> 3 -> 4 -> 4 (attach remaining)

    Time Complexity: O(n + m) where n, m are lengths of list1, list2
    Space Complexity: O(1) - only using pointers, reusing existing nodes

    Args:
        list1: ListNode - head of first sorted list
        list2: ListNode - head of second sorted list

    Returns:
        ListNode - head of merged sorted list
    """
    # Create dummy node to simplify edge cases
    dummy = ListNode(0)
    current = dummy

    # Merge while both lists have nodes
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    # Attach remaining nodes (at most one list has remaining nodes)
    current.next = list1 if list1 else list2

    return dummy.next  # Return head of merged list


def merge_two_lists_recursive(list1, list2):
    """
    Merge two sorted lists recursively.

    Approach:
    - Base case: if either list is empty, return the other list
    - Recursive case:
        - Compare first nodes
        - Choose smaller one
        - Recursively merge the rest

    Visualization:
    merge([1,2,4], [1,3,4])
        1 <= 1, choose list1's 1
        1.next = merge([2,4], [1,3,4])
            2 > 1, choose list2's 1
            1.next = merge([2,4], [3,4])
                2 < 3, choose list1's 2
                2.next = merge([4], [3,4])
                    4 > 3, choose list2's 3
                    3.next = merge([4], [4])
                        4 <= 4, choose list1's 4
                        4.next = merge([], [4])
                            return [4]

    Time Complexity: O(n + m)
    Space Complexity: O(n + m) for recursion call stack

    Args:
        list1: ListNode - head of first sorted list
        list2: ListNode - head of second sorted list

    Returns:
        ListNode - head of merged sorted list
    """
    # Base cases
    if not list1:
        return list2
    if not list2:
        return list1

    # Recursive case: choose smaller head and recurse
    if list1.val <= list2.val:
        list1.next = merge_two_lists_recursive(list1.next, list2)
        return list1
    else:
        list2.next = merge_two_lists_recursive(list1, list2.next)
        return list2


def merge_two_lists_inplace(list1, list2):
    """
    Alternative iterative approach without dummy node.

    Approach:
    Handle head separately, then merge rest.
    More complex due to head edge case.

    Time Complexity: O(n + m)
    Space Complexity: O(1)

    Args:
        list1: ListNode - head of first sorted list
        list2: ListNode - head of second sorted list

    Returns:
        ListNode - head of merged sorted list
    """
    # Handle empty lists
    if not list1:
        return list2
    if not list2:
        return list1

    # Determine head of merged list
    if list1.val <= list2.val:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next

    current = head

    # Merge rest
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    # Attach remaining
    current.next = list1 if list1 else list2

    return head


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


def visualize_merge(list1_vals, list2_vals):
    """
    Visualize the merge process step by step.

    Args:
        list1_vals: list of values for first list
        list2_vals: list of values for second list
    """
    print(f"List 1: {list1_vals}")
    print(f"List 2: {list2_vals}")
    print("\nMerge process:")

    list1 = create_list(list1_vals)
    list2 = create_list(list2_vals)

    dummy = ListNode(0)
    current = dummy
    step = 1

    l1, l2 = list1, list2

    while l1 and l2:
        if l1.val <= l2.val:
            print(f"Step {step}: Choose {l1.val} from list1")
            current.next = l1
            l1 = l1.next
        else:
            print(f"Step {step}: Choose {l2.val} from list2")
            current.next = l2
            l2 = l2.next
        current = current.next
        step += 1

    # Show remaining
    if l1:
        print(f"Step {step}: Attach remaining from list1: {list_to_array(l1)}")
    elif l2:
        print(f"Step {step}: Attach remaining from list2: {list_to_array(l2)}")

    current.next = l1 if l1 else l2

    print("\nFinal merged list:", end=" ")
    print_list(dummy.next)


def test_merge_two_lists():
    """Test cases for merge two sorted lists."""

    # Test all three approaches
    approaches = [
        ("Iterative with dummy", merge_two_lists_iterative),
        ("Recursive", merge_two_lists_recursive),
        ("Iterative without dummy", merge_two_lists_inplace)
    ]

    for name, func in approaches:
        print(f"\nTesting {name}:")

        # Test 1: Normal merge
        list1 = create_list([1, 2, 4])
        list2 = create_list([1, 3, 4])
        result = func(list1, list2)
        assert list_to_array(result) == [1, 1, 2, 3, 4, 4]
        print("Test 1 (normal merge): PASSED")

        # Test 2: Both empty
        list1 = create_list([])
        list2 = create_list([])
        result = func(list1, list2)
        assert list_to_array(result) == []
        print("Test 2 (both empty): PASSED")

        # Test 3: One empty
        list1 = create_list([])
        list2 = create_list([0])
        result = func(list1, list2)
        assert list_to_array(result) == [0]
        print("Test 3 (one empty): PASSED")

        # Test 4: Different lengths
        list1 = create_list([1, 2, 3, 4, 5])
        list2 = create_list([6, 7])
        result = func(list1, list2)
        assert list_to_array(result) == [1, 2, 3, 4, 5, 6, 7]
        print("Test 4 (different lengths): PASSED")

        # Test 5: No overlap
        list1 = create_list([1, 2, 3])
        list2 = create_list([4, 5, 6])
        result = func(list1, list2)
        assert list_to_array(result) == [1, 2, 3, 4, 5, 6]
        print("Test 5 (no overlap): PASSED")

        # Test 6: All same values
        list1 = create_list([1, 1, 1])
        list2 = create_list([1, 1])
        result = func(list1, list2)
        assert list_to_array(result) == [1, 1, 1, 1, 1]
        print("Test 6 (all same): PASSED")

        # Test 7: Negative numbers
        list1 = create_list([-10, -5, 0])
        list2 = create_list([-8, -3, 2])
        result = func(list1, list2)
        assert list_to_array(result) == [-10, -8, -5, -3, 0, 2]
        print("Test 7 (negative numbers): PASSED")

    print("\nAll tests passed!")


def compare_approaches():
    """Compare different merge approaches."""
    print("\n" + "="*50)
    print("Approach Comparison")
    print("="*50)

    print("\n1. Iterative with Dummy Node (RECOMMENDED)")
    print("   Time: O(n+m), Space: O(1)")
    print("   Pros: Clean code, handles edge cases elegantly")
    print("   Cons: One extra node allocation (minimal)")
    print("   Best for: Most situations, especially interviews")

    print("\n2. Recursive")
    print("   Time: O(n+m), Space: O(n+m) call stack")
    print("   Pros: Elegant, concise")
    print("   Cons: Stack overflow risk for very long lists")
    print("   Best for: Short lists, functional programming style")

    print("\n3. Iterative without Dummy")
    print("   Time: O(n+m), Space: O(1)")
    print("   Pros: No extra node, slightly more efficient")
    print("   Cons: More complex, harder to maintain")
    print("   Best for: When every byte matters (rare)")


if __name__ == "__main__":
    # Run tests
    test_merge_two_lists()

    print("\n" + "="*50)
    print("Visualization Example")
    print("="*50 + "\n")

    # Visualize merge
    visualize_merge([1, 2, 4], [1, 3, 4])

    print("\n" + "-"*50 + "\n")

    visualize_merge([1, 3, 5], [2, 4, 6])

    # Compare approaches
    compare_approaches()

    print("\n" + "="*50)
    print("Key Insights")
    print("="*50)
    print("\n1. Dummy node simplifies edge cases significantly")
    print("2. Both lists are already sorted - just pick smaller head each time")
    print("3. Don't forget to attach remaining nodes at the end")
    print("4. Works in-place - no new nodes created (except dummy)")
    print("5. Common pattern: use dummy + current pointer to build result")
