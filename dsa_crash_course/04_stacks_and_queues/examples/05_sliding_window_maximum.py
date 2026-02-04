"""
Sliding Window Maximum (LeetCode #239)

Problem:
You are given an array of integers nums, there is a sliding window of size k which
is moving from the very left of the array to the very right. You can only see the
k numbers in the window. Each time the sliding window moves right by one position.

Return the max sliding window.

Example 1:
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
Explanation:
Window position                Max
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7

Example 2:
Input: nums = [1], k = 1
Output: [1]

Example 3:
Input: nums = [1,-1], k = 1
Output: [1,-1]

Example 4:
Input: nums = [9,11], k = 2
Output: [11]

Example 5:
Input: nums = [4,-2], k = 2
Output: [4]

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- 1 <= k <= nums.length
"""

from collections import deque


def max_sliding_window(nums, k):
    """
    Deque-based approach with monotonic decreasing order - optimal solution.

    Approach:
    1. Use a deque to store indices (not values) of useful elements
    2. "Useful" = could be maximum of some future window
    3. Maintain deque in decreasing order of values
    4. For each position:
       a. Remove indices outside current window (left side)
       b. Remove indices with smaller values (right side)
       c. Add current index
       d. Front of deque is maximum of current window

    Why this works:
    - Deque stores potential maximums in decreasing order
    - If new element is larger, all smaller ones can never be maximum
    - Front of deque is always the maximum in current window
    - Each element added/removed at most once = O(n)

    Time Complexity: O(n) - each element added and removed once
    Space Complexity: O(k) - deque stores at most k elements

    Args:
        nums: Array of integers
        k: Window size

    Returns:
        List of maximum values for each window
    """
    if not nums or k == 0:
        return []

    if k == 1:
        return nums

    result = []
    dq = deque()  # Store indices

    for i, num in enumerate(nums):
        # Remove indices outside current window from front
        # Window is [i-k+1, i], so remove indices < i-k+1
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove indices with smaller values from back
        # They can never be maximum if current is larger
        while dq and nums[dq[-1]] < num:
            dq.pop()

        # Add current index
        dq.append(i)

        # Start adding to result when first window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


def max_sliding_window_brute_force(nums, k):
    """
    Brute force approach - check maximum in each window.

    Approach:
    For each window, scan all k elements to find maximum.

    Time Complexity: O(n*k) - n windows, each takes O(k) to find max
    Space Complexity: O(1) - only output array

    This is too slow for large inputs but demonstrates the problem clearly.
    """
    if not nums or k == 0:
        return []

    result = []
    n = len(nums)

    for i in range(n - k + 1):
        # Find max in window [i, i+k)
        window_max = max(nums[i:i+k])
        result.append(window_max)

    return result


def max_sliding_window_heap(nums, k):
    """
    Heap-based approach using max heap.

    Approach:
    1. Use a max heap to track elements in window
    2. For each position, add current element
    3. Remove elements outside window
    4. Top of heap is maximum (after cleanup)

    Time Complexity: O(n log n) - n elements, each heap operation O(log n)
    Space Complexity: O(n) - heap can grow to n elements

    Note: Not as efficient as deque approach, but good to know.
    Python's heapq is min heap, so we use negative values for max heap.
    """
    import heapq

    if not nums or k == 0:
        return []

    result = []
    heap = []  # Store (-value, index) for max heap behavior

    for i, num in enumerate(nums):
        # Add current element (negative for max heap)
        heapq.heappush(heap, (-num, i))

        # Start adding to result when first window is complete
        if i >= k - 1:
            # Remove elements outside window
            while heap and heap[0][1] <= i - k:
                heapq.heappop(heap)

            # Top of heap is maximum in window
            result.append(-heap[0][0])

    return result


def test_sliding_window_maximum():
    """Test cases covering various scenarios."""

    # Test all implementations
    implementations = [
        ("Deque (Optimal)", max_sliding_window),
        ("Brute Force", max_sliding_window_brute_force),
        ("Heap", max_sliding_window_heap)
    ]

    test_cases = [
        # (nums, k, expected)
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([1], 1, [1]),
        ([1, -1], 1, [1, -1]),
        ([9, 11], 2, [11]),
        ([4, -2], 2, [4]),
        ([1, 3, 1, 2, 0, 5], 3, [3, 3, 2, 5]),
        ([7, 2, 4], 2, [7, 4]),
        ([1, 2, 3, 4, 5], 3, [3, 4, 5]),
        ([5, 4, 3, 2, 1], 3, [5, 4, 3]),
        ([1, 1, 1, 1, 1], 3, [1, 1, 1])
    ]

    for name, func in implementations:
        print(f"\nTesting {name}...")

        for nums, k, expected in test_cases:
            result = func(nums, k)
            assert result == expected, f"Failed for {nums}, k={k}: got {result}, expected {expected}"

        print(f"  {name} passed all tests!")

    print("\nAll implementations passed!")


def visualize_deque_operations(nums, k):
    """Visualize how the deque changes for each window."""

    print(f"\n=== Deque Operations for nums={nums}, k={k} ===\n")

    if not nums or k == 0:
        return []

    result = []
    dq = deque()

    for i, num in enumerate(nums):
        print(f"Step {i+1}: Processing nums[{i}] = {num}")

        # Remove indices outside window
        removed_front = []
        while dq and dq[0] <= i - k:
            removed_front.append(dq.popleft())

        if removed_front:
            print(f"  Removed from front (outside window): {removed_front}")

        # Remove indices with smaller values
        removed_back = []
        while dq and nums[dq[-1]] < num:
            idx = dq.pop()
            removed_back.append((idx, nums[idx]))

        if removed_back:
            print(f"  Removed from back (smaller values): {removed_back}")

        # Add current index
        dq.append(i)
        print(f"  Added index {i} to deque")

        # Show deque state
        dq_values = [(idx, nums[idx]) for idx in dq]
        print(f"  Deque (index, value): {dq_values}")

        # Add to result if window is complete
        if i >= k - 1:
            max_val = nums[dq[0]]
            result.append(max_val)
            print(f"  Window [{i-k+1}:{i+1}] = {nums[i-k+1:i+1]}")
            print(f"  Maximum: {max_val} (at index {dq[0]})")

        print()

    print(f"Final result: {result}")
    return result


def explain_monotonic_deque():
    """Explain the monotonic deque concept."""

    print("\n=== Understanding Monotonic Deque ===\n")

    print("What is a Monotonic Deque?")
    print("  A deque that maintains elements in sorted order")
    print("  Can remove from both ends (unlike stack)")
    print()

    print("For Sliding Window Maximum:")
    print("  We maintain a DECREASING monotonic deque")
    print("  Deque stores indices in order of decreasing values")
    print()

    print("Key Operations:")
    print("  1. Remove from FRONT: indices outside window")
    print("  2. Remove from BACK: indices with smaller values")
    print("  3. Add to BACK: current index")
    print("  4. Front of deque: maximum in current window")
    print()

    print("Why Remove Smaller Values?")
    print("  If current element is larger than some element X in deque,")
    print("  X can NEVER be maximum of any future window because:")
    print("    - Current element is larger than X")
    print("    - Current element entered later (will stay longer)")
    print("  So we can safely discard X")
    print()

    print("Why O(n)?")
    print("  Each element:")
    print("    - Added to deque once: n operations")
    print("    - Removed from deque once: n operations")
    print("  Total: 2n = O(n)")
    print()


def compare_approaches():
    """Compare different approaches with timing."""

    import time

    test_cases = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3),
        (list(range(1000)), 10),
        (list(range(1000, 0, -1)), 10)
    ]

    print("\n=== Approach Comparison ===\n")

    for nums, k in test_cases:
        print(f"Input: n={len(nums)}, k={k}")
        print()

        # Deque approach
        start = time.perf_counter()
        result1 = max_sliding_window(nums, k)
        time1 = time.perf_counter() - start
        print(f"  Deque:       {time1*1000:.4f}ms - O(n)")

        # Heap approach
        start = time.perf_counter()
        result2 = max_sliding_window_heap(nums, k)
        time2 = time.perf_counter() - start
        print(f"  Heap:        {time2*1000:.4f}ms - O(n log n)")

        # Brute force (skip for large inputs)
        if len(nums) <= 100:
            start = time.perf_counter()
            result3 = max_sliding_window_brute_force(nums, k)
            time3 = time.perf_counter() - start
            print(f"  Brute Force: {time3*1000:.4f}ms - O(n*k)")

        print(f"  All produce same result: {result1 == result2}")
        print()


def demonstrate_edge_cases():
    """Demonstrate important edge cases."""

    print("\n=== Edge Cases Demonstration ===\n")

    cases = [
        {
            "name": "Single element",
            "nums": [1],
            "k": 1,
            "explanation": "Window size equals array size"
        },
        {
            "name": "Window size 1",
            "nums": [1, -1, 3],
            "k": 1,
            "explanation": "Each element is its own maximum"
        },
        {
            "name": "Increasing sequence",
            "nums": [1, 2, 3, 4, 5],
            "k": 3,
            "explanation": "Rightmost is always maximum"
        },
        {
            "name": "Decreasing sequence",
            "nums": [5, 4, 3, 2, 1],
            "k": 3,
            "explanation": "Leftmost is always maximum"
        },
        {
            "name": "All same",
            "nums": [3, 3, 3, 3],
            "k": 2,
            "explanation": "All windows have same maximum"
        }
    ]

    for case in cases:
        result = max_sliding_window(case["nums"], case["k"])
        print(f"{case['name']}: {case['nums']}, k={case['k']}")
        print(f"  Result: {result}")
        print(f"  Note: {case['explanation']}")
        print()


def related_problems():
    """Show related problems using deque."""

    print("\n=== Related Deque Problems ===\n")

    problems = [
        {
            "name": "Sliding Window Minimum",
            "pattern": "Monotonic increasing deque",
            "description": "Find minimum instead of maximum"
        },
        {
            "name": "Shortest Subarray with Sum at Least K",
            "pattern": "Monotonic deque",
            "description": "Find shortest subarray with sum >= k"
        },
        {
            "name": "Jump Game VI",
            "pattern": "Monotonic deque + DP",
            "description": "Maximum score jumping with window constraint"
        },
        {
            "name": "Constrained Subsequence Sum",
            "pattern": "Monotonic deque + DP",
            "description": "Maximum sum with distance constraint"
        }
    ]

    for problem in problems:
        print(f"{problem['name']}")
        print(f"  Pattern: {problem['pattern']}")
        print(f"  Description: {problem['description']}")
        print()


if __name__ == "__main__":
    # Run tests
    test_sliding_window_maximum()

    # Explain concept
    explain_monotonic_deque()

    # Demonstrate with visualization
    visualize_deque_operations([1, 3, -1, -3, 5, 3, 6, 7], 3)

    # Compare approaches
    compare_approaches()

    # Demonstrate edge cases
    demonstrate_edge_cases()

    # Show related problems
    related_problems()

    print("\n=== Key Takeaways ===\n")
    print("1. Use deque for O(1) operations at both ends")
    print("2. Maintain monotonic decreasing order")
    print("3. Remove from front: elements outside window")
    print("4. Remove from back: smaller elements (never useful)")
    print("5. Front of deque: maximum in window")
    print("6. Each element added/removed once = O(n)")
