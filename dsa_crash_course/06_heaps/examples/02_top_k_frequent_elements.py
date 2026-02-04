"""
Top K Frequent Elements (LeetCode #347)

Problem:
Given an integer array nums and an integer k, return the k most frequent
elements. You may return the answer in any order.

Example 1:
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Example 2:
Input: nums = [1], k = 1
Output: [1]

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in the range [1, the number of unique elements in the array]
- It is guaranteed that the answer is unique

Follow up: Your algorithm's time complexity must be better than O(n log n),
where n is the array's size.
"""


def top_k_frequent_sort(nums, k):
    """
    Sorting approach using Counter.

    Approach:
    1. Count frequency of each element
    2. Sort by frequency
    3. Return top K

    Time Complexity: O(n log n) - sorting unique elements
    Space Complexity: O(n) - frequency map

    Args:
        nums: List of integers
        k: Number of most frequent elements to return

    Returns:
        List of k most frequent elements
    """
    from collections import Counter

    # Count frequencies
    freq = Counter(nums)

    # Sort by frequency (descending)
    sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # Return top K elements
    return [num for num, count in sorted_items[:k]]


def top_k_frequent_heap_builtin(nums, k):
    """
    Using heapq.nlargest (simplest approach).

    Approach:
    1. Count frequencies
    2. Use heapq.nlargest with frequency as key

    Time Complexity: O(n log k) where n is array length
    Space Complexity: O(n) - frequency map

    Args:
        nums: List of integers
        k: Number of most frequent elements to return

    Returns:
        List of k most frequent elements
    """
    from collections import Counter
    import heapq

    # Count frequencies
    freq = Counter(nums)

    # Get K elements with highest frequency
    return heapq.nlargest(k, freq.keys(), key=freq.get)


def top_k_frequent(nums, k):
    """
    Min-heap approach - optimal heap solution.

    Approach:
    1. Count frequency of each element
    2. Use min-heap of size K
    3. Heap stores (frequency, element) tuples
    4. Maintain K most frequent by removing minimum
    5. Extract elements from final heap

    Why min-heap?
    - Want to keep K most frequent elements
    - Smallest frequency in heap is the Kth highest frequency
    - Remove any element with lower frequency
    - Min-heap gives O(1) access to minimum frequency

    Time Complexity: O(n log k)
    - O(n) to count frequencies
    - O(m log k) for heap operations where m is unique elements
    - Better than O(n log n) sort

    Space Complexity: O(n) - frequency map and heap

    Args:
        nums: List of integers
        k: Number of most frequent elements to return

    Returns:
        List of k most frequent elements
    """
    from collections import Counter
    import heapq

    # Count frequencies: O(n)
    freq = Counter(nums)

    # Min-heap to store K most frequent
    # Store (frequency, element) so heap compares by frequency
    heap = []

    for num, count in freq.items():
        # Add (frequency, element)
        heapq.heappush(heap, (count, num))

        # If heap has more than K elements, remove least frequent
        if len(heap) > k:
            heapq.heappop(heap)

    # Extract elements (not frequencies) from heap
    return [num for count, num in heap]


def top_k_frequent_bucket_sort(nums, k):
    """
    Bucket sort approach - optimal for this problem.

    Approach:
    1. Count frequencies
    2. Create buckets where bucket[i] contains elements with frequency i
    3. Iterate from highest frequency down, collect K elements

    Time Complexity: O(n) - better than heap!
    Space Complexity: O(n) - buckets array

    This is optimal because frequencies are bounded by n.

    Args:
        nums: List of integers
        k: Number of most frequent elements to return

    Returns:
        List of k most frequent elements
    """
    from collections import Counter

    # Count frequencies
    freq = Counter(nums)

    # Create buckets: bucket[i] = elements with frequency i
    # Maximum frequency is len(nums)
    buckets = [[] for _ in range(len(nums) + 1)]

    for num, count in freq.items():
        buckets[count].append(num)

    # Collect K most frequent from high to low frequency
    result = []
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result

    return result


def top_k_frequent_max_heap(nums, k):
    """
    Alternative: Max-heap approach (extract K times).

    Approach:
    1. Count frequencies
    2. Build max-heap of all (frequency, element) pairs
    3. Extract K times

    Time Complexity: O(n + m log m) where m is unique elements
    - O(n) to count
    - O(m) to build heap
    - O(k log m) to extract K times

    Space Complexity: O(n)

    Args:
        nums: List of integers
        k: Number of most frequent elements to return

    Returns:
        List of k most frequent elements
    """
    from collections import Counter
    import heapq

    # Count frequencies
    freq = Counter(nums)

    # Create max-heap (negate frequencies)
    heap = [(-count, num) for num, count in freq.items()]
    heapq.heapify(heap)

    # Extract K most frequent
    result = []
    for _ in range(k):
        count, num = heapq.heappop(heap)
        result.append(num)

    return result


def visualize_top_k_frequent(nums, k):
    """
    Helper function to visualize the top K frequent process.

    Shows how min-heap maintains K most frequent elements.
    """
    from collections import Counter
    import heapq

    print(f"\nFinding {k} most frequent in {nums}")
    print("=" * 60)

    # Count frequencies
    freq = Counter(nums)
    print(f"\nFrequencies: {dict(freq)}")

    heap = []

    print(f"\nBuilding min-heap of size {k}:")
    for i, (num, count) in enumerate(freq.items()):
        print(f"\nStep {i + 1}: Element {num} with frequency {count}")

        # Add to heap
        heapq.heappush(heap, (count, num))
        print(f"  After push: {heap}")

        # Remove if size exceeds K
        if len(heap) > k:
            removed_count, removed_num = heapq.heappop(heap)
            print(
                f"  Removed {removed_num} (freq={removed_count}, "
                f"heap size > {k})"
            )
            print(f"  After pop: {heap}")

        # Show current state
        current = sorted(heap, reverse=True)
        print(f"  Current {k} most frequent: {[(n, c) for c, n in current]}")
        if heap:
            print(
                f"  Minimum frequency in heap: {heap[0][0]} "
                f"(element {heap[0][1]})"
            )

    print(f"\n{'=' * 60}")
    result = [num for count, num in heap]
    print(f"Final answer: {result}")


def compare_approaches(nums, k):
    """
    Compare different approaches for finding top K frequent.
    """
    import time

    approaches = [
        ("Sort", top_k_frequent_sort),
        ("heapq.nlargest", top_k_frequent_heap_builtin),
        ("Min-heap", top_k_frequent),
        ("Bucket Sort", top_k_frequent_bucket_sort),
        ("Max-heap", top_k_frequent_max_heap),
    ]

    print(f"\nInput: nums = {nums}, k = {k}")
    print("=" * 60)

    results = []
    for name, func in approaches:
        start = time.perf_counter()
        result = sorted(func(nums[:], k))  # Sort for consistent comparison
        elapsed = time.perf_counter() - start

        results.append((name, result, elapsed))
        print(f"{name:20s}: {result} ({elapsed * 1000000:.2f} µs)")

    # Verify all give same result (when sorted)
    assert all(r[1] == results[0][1] for r in results), "Results don't match!"


def test_top_k_frequent():
    """Test cases covering various scenarios."""

    # Test case 1: Basic example
    result = sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2))
    assert result == [1, 2]

    # Test case 2: Single element
    assert top_k_frequent([1], 1) == [1]

    # Test case 3: All unique
    result = sorted(top_k_frequent([1, 2, 3, 4, 5], 3))
    assert len(result) == 3
    assert all(x in [1, 2, 3, 4, 5] for x in result)

    # Test case 4: K = 1
    assert top_k_frequent([1, 1, 1, 2, 2, 3], 1) == [1]

    # Test case 5: All same frequency
    result = sorted(top_k_frequent([1, 2, 3], 2))
    assert len(result) == 2

    # Test case 6: Negative numbers
    result = sorted(top_k_frequent([-1, -1, -2, -2, -2, 0], 2))
    assert result == [-2, -1]

    # Test case 7: Large frequency difference
    result = sorted(top_k_frequent([1] * 10 + [2] * 5 + [3] * 1, 2))
    assert result == [1, 2]

    # Test case 8: Two elements, same frequency
    result = sorted(top_k_frequent([1, 1, 2, 2], 2))
    assert result == [1, 2]

    # Test case 9: Bucket sort approach
    result = sorted(top_k_frequent_bucket_sort([1, 1, 1, 2, 2, 3], 2))
    assert result == [1, 2]

    # Test case 10: Many duplicates
    nums = [1] * 100 + [2] * 90 + [3] * 80 + [4] * 10
    result = sorted(top_k_frequent(nums, 3))
    assert result == [1, 2, 3]

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_top_k_frequent()

    # Example with visualization
    nums = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]
    k = 2
    print("\n" + "=" * 60)
    print("EXAMPLE WITH VISUALIZATION")
    print("=" * 60)
    visualize_top_k_frequent(nums, k)

    # Compare approaches
    print("\n" + "=" * 60)
    print("COMPARING APPROACHES")
    print("=" * 60)

    test_cases = [
        ([1, 1, 1, 2, 2, 3], 2),
        ([1], 1),
        ([1, 2, 3, 4, 5], 3),
    ]

    for nums, k in test_cases:
        compare_approaches(nums, k)

    # Performance comparison
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS")
    print("=" * 60)
    print("""
Approach          Time              Space      Notes
------------------------------------------------------------
Sort              O(n log n)        O(n)       Simple, works for any K
heapq.nlargest    O(n log k)        O(n)       Clean code
Min-heap          O(n log k)        O(n)       Best for k << unique elements
Bucket Sort       O(n)              O(n)       Optimal! Uses bounded frequencies
Max-heap          O(n + m log m)    O(n)       m = unique elements

Key Insights:
1. Min-heap of size K keeps K most frequent elements
2. Heap top has minimum frequency among K most frequent
3. Remove any element with lower frequency than current Kth
4. Bucket sort is optimal because frequencies are bounded by n

Min-Heap Approach:
- Store (frequency, element) tuples
- Min-heap compares by frequency
- Maintain K elements with highest frequencies
- Remove elements with lowest frequency when heap > K

Bucket Sort Approach (Optimal):
- Create buckets for each frequency (0 to n)
- Place elements in bucket based on their frequency
- Collect K elements from highest frequency buckets
- O(n) time because we only iterate through buckets once

When to use each:
- Sort: Quick implementation, small arrays
- heapq.nlargest: Cleanest code for production
- Min-heap: Interview favorite, demonstrates understanding
- Bucket Sort: Optimal solution, show advanced knowledge
- Max-heap: When you need all elements in frequency order

Pattern Recognition:
This problem combines two patterns:
1. Frequency counting with Counter
2. Top K elements with heap or bucket sort
    """)
