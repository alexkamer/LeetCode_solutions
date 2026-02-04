"""
Merge k Sorted Lists (LeetCode #23)

Problem:
You are given an array of k linked-lists lists, each linked-list is sorted
in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

Example 1:
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6

Example 2:
Input: lists = []
Output: []

Example 3:
Input: lists = [[]]
Output: []

Constraints:
- k == lists.length
- 0 <= k <= 10^4
- 0 <= lists[i].length <= 500
- -10^4 <= lists[i][j] <= 10^4
- lists[i] is sorted in ascending order
- The sum of lists[i].length will not exceed 10^4
"""


class ListNode:
    """Definition for singly-linked list."""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __lt__(self, other):
        """Enable comparison for heap (Python 3)."""
        return self.val < other.val

    def __repr__(self):
        """String representation for debugging."""
        return f"ListNode({self.val})"


def merge_k_lists_brute_force(lists):
    """
    Brute force: collect all values, sort, rebuild list.

    Approach:
    1. Collect all node values into array
    2. Sort array
    3. Build new linked list from sorted values

    Time Complexity: O(N log N) where N is total nodes
    Space Complexity: O(N) for array

    Args:
        lists: List of ListNode heads

    Returns:
        Head of merged sorted linked list
    """
    # Collect all values
    values = []
    for head in lists:
        current = head
        while current:
            values.append(current.val)
            current = current.next

    # Sort values
    values.sort()

    # Build linked list
    dummy = ListNode(0)
    current = dummy

    for val in values:
        current.next = ListNode(val)
        current = current.next

    return dummy.next


def merge_k_lists_merge_pairs(lists):
    """
    Merge lists in pairs (divide and conquer).

    Approach:
    1. Merge lists pairwise: [1,2,3,4] -> [12,34] -> [1234]
    2. Each merge is O(n) for two lists
    3. Log K levels of merging

    Time Complexity: O(N log K)
    - N total nodes, log K levels of merging
    Space Complexity: O(1) if not counting recursion

    Args:
        lists: List of ListNode heads

    Returns:
        Head of merged sorted linked list
    """

    def merge_two_lists(l1, l2):
        """Merge two sorted linked lists."""
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

        # Attach remaining
        current.next = l1 if l1 else l2

        return dummy.next

    if not lists:
        return None

    # Merge pairs until one list remains
    while len(lists) > 1:
        merged = []

        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two_lists(l1, l2))

        lists = merged

    return lists[0]


def merge_k_lists(lists):
    """
    Optimal heap approach - merge K sorted lists.

    Approach:
    1. Initialize min-heap with first node from each list
    2. Pop minimum node from heap
    3. Add it to result
    4. If popped node has next, add next to heap
    5. Repeat until heap is empty

    Why this works:
    - Heap maintains one node from each list
    - Minimum in heap is globally minimum among remaining nodes
    - Always have at most K nodes in heap
    - Each node processed exactly once

    Time Complexity: O(N log K)
    - N total nodes
    - Each node: O(log K) for heap operations
    - Much better than O(N log N) brute force

    Space Complexity: O(K) - heap stores at most K nodes

    Args:
        lists: List of ListNode heads

    Returns:
        Head of merged sorted linked list
    """
    import heapq

    # Handle empty input
    if not lists:
        return None

    # Min-heap: stores nodes, compares by value
    heap = []

    # Initialize heap with first node from each list
    for i, head in enumerate(lists):
        if head:
            # Store (value, list_index, node) to handle equal values
            heapq.heappush(heap, (head.val, i, head))

    # Build result list
    dummy = ListNode(0)
    current = dummy

    while heap:
        # Get node with minimum value
        val, list_idx, node = heapq.heappop(heap)

        # Add to result
        current.next = node
        current = current.next

        # If this list has more nodes, add next to heap
        if node.next:
            heapq.heappush(heap, (node.next.val, list_idx, node.next))

    return dummy.next


def merge_k_sorted_arrays(arrays):
    """
    Variation: Merge K sorted arrays (not linked lists).

    This is simpler and shows the core heap pattern.

    Time Complexity: O(N log K)
    Space Complexity: O(K) for heap + O(N) for result

    Args:
        arrays: List of sorted arrays

    Returns:
        Single merged sorted array
    """
    import heapq

    result = []
    heap = []

    # Initialize heap with first element from each array
    # Store (value, array_index, element_index)
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))

    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Add next element from same array
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))

    return result


# Helper functions for testing


def create_linked_list(values):
    """Create linked list from list of values."""
    if not values:
        return None

    head = ListNode(values[0])
    current = head

    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next

    return head


def linked_list_to_list(head):
    """Convert linked list to Python list."""
    result = []
    current = head

    while current:
        result.append(current.val)
        current = current.next

    return result


def visualize_merge_k_lists(list_arrays):
    """
    Visualize the merge K lists process with heap.

    Shows how heap maintains minimum among K candidates.
    """
    import heapq

    print(f"\nMerging {len(list_arrays)} sorted lists:")
    for i, arr in enumerate(list_arrays):
        print(f"  List {i}: {arr}")

    print("\n" + "=" * 60)

    # Convert to linked lists
    lists = [create_linked_list(arr) for arr in list_arrays]

    heap = []

    # Initialize heap
    print("\nInitializing heap with first from each list:")
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))
            print(f"  Added {head.val} from list {i}")

    print(f"\nInitial heap: {[(val, idx) for val, idx, _ in heap]}")

    result = []
    step = 1

    while heap:
        print(f"\n--- Step {step} ---")
        print(f"Heap: {[(val, idx) for val, idx, _ in heap]}")

        # Pop minimum
        val, list_idx, node = heapq.heappop(heap)
        result.append(val)

        print(f"Popped: {val} from list {list_idx}")
        print(f"Result so far: {result}")

        # Add next from same list
        if node.next:
            heapq.heappush(heap, (node.next.val, list_idx, node.next))
            print(
                f"Added: {node.next.val} from list {list_idx} "
                f"(next in same list)"
            )
        else:
            print(f"List {list_idx} exhausted")

        step += 1

    print(f"\n{'=' * 60}")
    print(f"Final merged list: {result}")


def compare_approaches(list_arrays):
    """
    Compare different approaches for merging K lists.
    """
    import time

    approaches = [
        ("Brute Force", merge_k_lists_brute_force),
        ("Merge Pairs", merge_k_lists_merge_pairs),
        ("Min-Heap", merge_k_lists),
    ]

    print(f"\nInput: {list_arrays}")
    print("=" * 60)

    # Convert to linked lists
    lists = [create_linked_list(arr) for arr in list_arrays]

    results = []
    for name, func in approaches:
        # Create fresh copies
        test_lists = [create_linked_list(arr) for arr in list_arrays]

        start = time.perf_counter()
        result_head = func(test_lists)
        result = linked_list_to_list(result_head)
        elapsed = time.perf_counter() - start

        results.append((name, result, elapsed))
        print(f"{name:20s}: {result} ({elapsed * 1000000:.2f} µs)")

    # Verify all give same result
    assert all(r[1] == results[0][1] for r in results), "Results don't match!"


def test_merge_k_lists():
    """Test cases covering various scenarios."""

    # Test case 1: Basic example
    lists = [
        create_linked_list([1, 4, 5]),
        create_linked_list([1, 3, 4]),
        create_linked_list([2, 6]),
    ]
    result = linked_list_to_list(merge_k_lists(lists))
    assert result == [1, 1, 2, 3, 4, 4, 5, 6]

    # Test case 2: Empty input
    assert merge_k_lists([]) is None

    # Test case 3: Single empty list
    lists = [create_linked_list([])]
    assert merge_k_lists(lists) is None

    # Test case 4: Single list
    lists = [create_linked_list([1, 2, 3])]
    result = linked_list_to_list(merge_k_lists(lists))
    assert result == [1, 2, 3]

    # Test case 5: Two lists
    lists = [create_linked_list([1, 3]), create_linked_list([2, 4])]
    result = linked_list_to_list(merge_k_lists(lists))
    assert result == [1, 2, 3, 4]

    # Test case 6: Different lengths
    lists = [
        create_linked_list([1]),
        create_linked_list([2, 3, 4]),
        create_linked_list([5, 6, 7, 8]),
    ]
    result = linked_list_to_list(merge_k_lists(lists))
    assert result == [1, 2, 3, 4, 5, 6, 7, 8]

    # Test case 7: Negative numbers
    lists = [create_linked_list([-2, -1]), create_linked_list([-3, 0])]
    result = linked_list_to_list(merge_k_lists(lists))
    assert result == [-3, -2, -1, 0]

    # Test case 8: All same values
    lists = [
        create_linked_list([1, 1]),
        create_linked_list([1, 1]),
        create_linked_list([1, 1]),
    ]
    result = linked_list_to_list(merge_k_lists(lists))
    assert result == [1, 1, 1, 1, 1, 1]

    # Test case 9: Merge arrays (simpler version)
    arrays = [[1, 4, 5], [1, 3, 4], [2, 6]]
    result = merge_k_sorted_arrays(arrays)
    assert result == [1, 1, 2, 3, 4, 4, 5, 6]

    # Test case 10: Many lists
    lists = [create_linked_list([i]) for i in range(10)]
    result = linked_list_to_list(merge_k_lists(lists))
    assert result == list(range(10))

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_merge_k_lists()

    # Example with visualization
    list_arrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    print("\n" + "=" * 60)
    print("EXAMPLE WITH VISUALIZATION")
    print("=" * 60)
    visualize_merge_k_lists(list_arrays)

    # Compare approaches
    print("\n" + "=" * 60)
    print("COMPARING APPROACHES")
    print("=" * 60)

    test_cases = [
        [[1, 4, 5], [1, 3, 4], [2, 6]],
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[1], [2], [3]],
    ]

    for list_arrays in test_cases:
        compare_approaches(list_arrays)

    # Performance comparison
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS")
    print("=" * 60)
    print("""
Approach          Time              Space      Notes
------------------------------------------------------------
Brute Force       O(N log N)        O(N)       Collect all, sort
Merge Pairs       O(N log K)        O(1)       Divide and conquer
Min-Heap          O(N log K)        O(K)       Optimal, elegant

Where:
- N = total number of nodes across all lists
- K = number of lists

Key Insights:
1. Heap maintains one candidate from each list (K elements)
2. Minimum in heap is globally minimum among remaining
3. Each node enters and exits heap exactly once
4. Heap size is always at most K, not N

Min-Heap Approach:
- Initialize: Add first node from each list to heap
- Loop: Pop minimum, add to result, push next from same list
- Heap invariant: Always contains the "frontier" of each list
- Time per node: O(log K) for heap operations
- Total: N nodes × O(log K) = O(N log K)

Why Heap is Better than Sort:
- Don't need to collect all values (streaming)
- Can handle infinite streams
- Better complexity when K << N
- More elegant and demonstrates algorithmic thinking

This is the "K-way merge" pattern:
- Merge K sorted sequences into one
- Heap tracks minimum among K candidates
- Replace used element with next from same sequence
- Common in external sorting, log merging, etc.

Comparison:
- Brute force: Simple but wasteful O(N log N)
- Merge pairs: Good, optimal complexity O(N log K)
- Min-heap: Optimal and most elegant O(N log K)

When to use each:
- Brute force: Very simple case, K small
- Merge pairs: When heap not available
- Min-heap: Interview favorite, production code
    """)
