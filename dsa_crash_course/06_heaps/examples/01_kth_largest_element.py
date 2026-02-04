"""
Kth Largest Element in an Array (LeetCode #215)

Problem:
Given an integer array nums and an integer k, return the kth largest element
in the array.

Note that it is the kth largest element in the sorted order, not the kth
distinct element.

Can you solve it without sorting?

Example 1:
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5

Example 2:
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4

Constraints:
- 1 <= k <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
"""


def find_kth_largest_sort(nums, k):
    """
    Sorting approach.

    Approach:
    1. Sort array in descending order
    2. Return element at index k-1

    Time Complexity: O(n log n) - sorting
    Space Complexity: O(1) or O(n) depending on sort implementation

    Args:
        nums: List of integers
        k: Kth largest element to find (1-indexed)

    Returns:
        The kth largest element
    """
    nums.sort(reverse=True)
    return nums[k - 1]


def find_kth_largest_heap_builtin(nums, k):
    """
    Using Python's heapq.nlargest (simplest approach).

    Approach:
    1. Use heapq.nlargest to find K largest elements
    2. Return the last one (Kth largest)

    Time Complexity: O(n log k) - heap operations
    Space Complexity: O(k) - heap size

    Args:
        nums: List of integers
        k: Kth largest element to find (1-indexed)

    Returns:
        The kth largest element
    """
    import heapq

    # nlargest returns K largest in descending order
    return heapq.nlargest(k, nums)[-1]


def find_kth_largest(nums, k):
    """
    Min-heap approach - optimal heap solution.

    Approach:
    1. Maintain min-heap of size K
    2. Heap always contains K largest elements seen so far
    3. Heap top is the Kth largest element
    4. For each number:
       - Add to heap
       - If heap size > K, remove minimum
    5. Return heap top

    Why min-heap for K largest?
    - We want to keep K largest elements
    - Smallest of these K elements is the Kth largest
    - Min-heap gives us O(1) access to smallest
    - We remove elements smaller than Kth largest

    Time Complexity: O(n log k)
    - n elements, each requires log k heap operations
    - Better than O(n log n) sort when k << n

    Space Complexity: O(k) - heap stores K elements

    Args:
        nums: List of integers
        k: Kth largest element to find (1-indexed)

    Returns:
        The kth largest element
    """
    import heapq

    # Min-heap to store K largest elements
    heap = []

    for num in nums:
        # Add current number
        heapq.heappush(heap, num)

        # If heap has more than K elements, remove smallest
        if len(heap) > k:
            heapq.heappop(heap)

    # Heap top is Kth largest
    return heap[0]


def find_kth_largest_quickselect(nums, k):
    """
    Quickselect approach - optimal average case.

    Approach:
    1. Use partition from quicksort
    2. Find position where element would be in sorted array
    3. If position is K-1, found answer
    4. If position > K-1, search left
    5. If position < K-1, search right

    Time Complexity: O(n) average, O(n²) worst case
    Space Complexity: O(1)

    This is the optimal solution but more complex to implement.

    Args:
        nums: List of integers
        k: Kth largest element to find (1-indexed)

    Returns:
        The kth largest element
    """
    import random

    def partition(left, right, pivot_idx):
        """Partition array around pivot."""
        pivot = nums[pivot_idx]

        # Move pivot to end
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        # Move all elements larger than pivot to the left
        store_idx = left
        for i in range(left, right):
            if nums[i] > pivot:
                nums[i], nums[store_idx] = nums[store_idx], nums[i]
                store_idx += 1

        # Move pivot to final position
        nums[store_idx], nums[right] = nums[right], nums[store_idx]

        return store_idx

    def select(left, right, k_smallest):
        """Select kth smallest element in nums[left:right+1]."""
        if left == right:
            return nums[left]

        # Random pivot for better average case
        pivot_idx = random.randint(left, right)

        # Find position of pivot in sorted array
        pivot_idx = partition(left, right, pivot_idx)

        # If pivot is at target position
        if k_smallest == pivot_idx:
            return nums[k_smallest]
        elif k_smallest < pivot_idx:
            # Target is in left part
            return select(left, pivot_idx - 1, k_smallest)
        else:
            # Target is in right part
            return select(pivot_idx + 1, right, k_smallest)

    # Kth largest is (k-1)th element in descending order
    return select(0, len(nums) - 1, k - 1)


def visualize_kth_largest(nums, k):
    """
    Helper function to visualize the kth largest process with min-heap.

    Shows how heap maintains K largest elements.
    """
    import heapq

    print(f"\nFinding {k}th largest in {nums}")
    print("=" * 60)

    heap = []

    for i, num in enumerate(nums):
        print(f"\nStep {i + 1}: Processing {num}")

        # Add to heap
        heapq.heappush(heap, num)
        print(f"  After push: {heap}")

        # Remove if size exceeds K
        if len(heap) > k:
            removed = heapq.heappop(heap)
            print(f"  Removed {removed} (heap size > {k})")
            print(f"  After pop: {heap}")

        print(f"  Current {k} largest: {sorted(heap, reverse=True)}")
        print(f"  Current {k}th largest: {heap[0]}")

    print(f"\n{'=' * 60}")
    print(f"Final answer: {heap[0]}")

    # Verify with sorted array
    sorted_nums = sorted(nums, reverse=True)
    print(f"Verification: Sorted array = {sorted_nums}")
    print(f"              {k}th element = {sorted_nums[k - 1]}")


def compare_approaches(nums, k):
    """
    Compare different approaches for finding kth largest.
    """
    import time

    approaches = [
        ("Sort", find_kth_largest_sort),
        ("heapq.nlargest", find_kth_largest_heap_builtin),
        ("Min-heap", find_kth_largest),
        ("Quickselect", find_kth_largest_quickselect),
    ]

    print(f"\nInput: nums = {nums}, k = {k}")
    print("=" * 60)

    results = []
    for name, func in approaches:
        # Make copy to avoid modifying original
        test_nums = nums[:]

        start = time.perf_counter()
        result = func(test_nums, k)
        elapsed = time.perf_counter() - start

        results.append((name, result, elapsed))
        print(f"{name:20s}: {result} ({elapsed * 1000000:.2f} µs)")

    # Verify all give same result
    assert all(r[1] == results[0][1] for r in results), "Results don't match!"


def test_kth_largest():
    """Test cases covering various scenarios."""

    # Test case 1: Basic example
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest_quickselect([3, 2, 1, 5, 6, 4], 2) == 5

    # Test case 2: With duplicates
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

    # Test case 3: K = 1 (largest)
    assert find_kth_largest([7, 6, 5, 4, 3, 2, 1], 1) == 7

    # Test case 4: K = length (smallest)
    assert find_kth_largest([7, 6, 5, 4, 3, 2, 1], 7) == 1

    # Test case 5: Single element
    assert find_kth_largest([1], 1) == 1

    # Test case 6: All same elements
    assert find_kth_largest([5, 5, 5, 5, 5], 3) == 5

    # Test case 7: Negative numbers
    assert find_kth_largest([-1, -5, -2, -8, -3], 2) == -2

    # Test case 8: Mixed positive and negative
    assert find_kth_largest([-3, -2, -1, 0, 1, 2, 3], 4) == 0

    # Test case 9: Large K
    nums = list(range(1, 101))
    assert find_kth_largest(nums, 50) == 51

    # Test case 10: Two elements
    assert find_kth_largest([2, 1], 1) == 2
    assert find_kth_largest([2, 1], 2) == 1

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_kth_largest()

    # Example with visualization
    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    print("\n" + "=" * 60)
    print("EXAMPLE WITH VISUALIZATION")
    print("=" * 60)
    visualize_kth_largest(nums, k)

    # Compare approaches
    print("\n" + "=" * 60)
    print("COMPARING APPROACHES")
    print("=" * 60)

    test_cases = [
        ([3, 2, 1, 5, 6, 4], 2),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4),
        ([7, 6, 5, 4, 3, 2, 1], 1),
    ]

    for nums, k in test_cases:
        compare_approaches(nums, k)

    # Performance comparison
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS")
    print("=" * 60)
    print("""
Approach          Time         Space      Best For
----------------------------------------------------------
Sort              O(n log n)   O(1)       Simple, small arrays
heapq.nlargest    O(n log k)   O(k)       Clean code, good for k << n
Min-heap          O(n log k)   O(k)       Best when k << n
Quickselect       O(n) avg     O(1)       Optimal average, modifies array
                  O(n²) worst

Key Insights:
1. Min-heap of size K keeps K largest elements
2. Heap top is always Kth largest (smallest of K largest)
3. When k is small, heap is much faster than sort
4. Quickselect is optimal but more complex
5. heapq.nlargest is simplest for practical use

When to use each:
- Sort: Simple solution, need sorted array anyway
- heapq.nlargest: Cleanest code, good default choice
- Min-heap: Understanding the pattern, interviews
- Quickselect: Optimal solution when you need best performance

Min-Heap Intuition:
- Keep K largest elements in heap
- Smallest of these K is the Kth largest
- Remove any element smaller than current Kth largest
- Min-heap gives O(1) access to minimum for removal
    """)
