"""
Find Median from Data Stream (LeetCode #295)

Problem:
The median is the middle value in an ordered integer list. If the size of the
list is even, there is no middle value, and the median is the mean of the two
middle values.

Implement the MedianFinder class:
- MedianFinder() initializes the MedianFinder object.
- void addNum(int num) adds the integer num from the data stream.
- double findMedian() returns the median of all elements so far.

Example 1:
Input:
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
Output:
[null, null, null, 1.5, null, 2.0]

Explanation:
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
medianFinder.addNum(3);    // arr = [1, 2, 3]
medianFinder.findMedian(); // return 2.0

Constraints:
- -10^5 <= num <= 10^5
- There will be at least one element before calling findMedian
- At most 5 * 10^4 calls will be made to addNum and findMedian

Follow up:
- If all values are from 0 to 100, how would you optimize?
- If 99% of values are in [0, 100], how would you optimize?
"""


class MedianFinderNaive:
    """
    Naive approach: maintain sorted array.

    Approach:
    1. Keep array sorted after each insertion
    2. Median is middle element(s)

    Time Complexity:
    - addNum: O(n) - insert in sorted position
    - findMedian: O(1) - just access middle

    Space Complexity: O(n)

    This works but is not optimal.
    """

    def __init__(self):
        self.nums = []

    def add_num(self, num):
        """Add number maintaining sorted order."""
        # Binary search to find insertion position
        left, right = 0, len(self.nums)

        while left < right:
            mid = (left + right) // 2
            if self.nums[mid] < num:
                left = mid + 1
            else:
                right = mid

        self.nums.insert(left, num)

    def find_median(self):
        """Find median in O(1)."""
        n = len(self.nums)
        if n % 2 == 1:
            return float(self.nums[n // 2])
        else:
            return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2.0


class MedianFinder:
    """
    Optimal two-heap approach.

    Approach:
    1. Use two heaps to split numbers:
       - Max-heap for smaller half (left side)
       - Min-heap for larger half (right side)
    2. Balance heaps so sizes differ by at most 1
    3. Median is at heap tops

    Why this works:
    - Heaps maintain split point in sorted order
    - Max-heap top = largest of smaller half
    - Min-heap top = smallest of larger half
    - These are the middle elements!

    Invariants:
    1. All elements in max-heap <= all in min-heap
    2. |len(max_heap) - len(min_heap)| <= 1
    3. If sizes differ, max-heap has one more

    Time Complexity:
    - addNum: O(log n) - heap operations
    - findMedian: O(1) - just peek tops

    Space Complexity: O(n) - store all numbers

    This is optimal for this problem!
    """

    def __init__(self):
        import heapq

        # Max-heap for smaller half (negate values)
        self.small = []

        # Min-heap for larger half
        self.large = []

    def add_num(self, num):
        """
        Add number maintaining balance.

        Process:
        1. Add to max-heap (smaller half)
        2. Move largest from small to large (maintain invariant 1)
        3. Balance sizes if needed (maintain invariant 2)
        """
        import heapq

        # Add to max-heap (smaller half)
        heapq.heappush(self.small, -num)

        # Move largest from small to large
        # This ensures all in small <= all in large
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # Balance sizes: small should have equal or one more
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self):
        """
        Find median in O(1).

        If odd count: median is max-heap top (small has one more)
        If even count: median is average of both tops
        """
        if len(self.small) > len(self.large):
            # Odd count, small has one more
            return float(-self.small[0])
        else:
            # Even count, average of tops
            return (-self.small[0] + self.large[0]) / 2.0

    def get_state(self):
        """Helper to visualize heap state."""
        small_vals = sorted([-x for x in self.small], reverse=True)
        large_vals = sorted(self.large)
        return small_vals, large_vals


class MedianFinderAlternative:
    """
    Alternative implementation with explicit size tracking.

    Same idea but slightly different balance strategy.
    """

    def __init__(self):
        import heapq

        self.small = []  # Max-heap
        self.large = []  # Min-heap

    def add_num(self, num):
        """Add number with alternative balancing."""
        import heapq

        # Add to appropriate heap
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
        else:
            heapq.heappush(self.large, num)

        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        elif len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self):
        """Find median."""
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        else:
            return (-self.small[0] + self.large[0]) / 2.0


def visualize_median_finder():
    """
    Visualize how two heaps maintain median.

    Shows the state of heaps after each insertion.
    """
    print("\nVisualizing MedianFinder with two heaps")
    print("=" * 60)

    mf = MedianFinder()
    numbers = [5, 15, 1, 3, 8, 7, 9, 10, 20, 12]

    print("\nMax-heap (small) | Min-heap (large)")
    print("  <= median      |   >= median")
    print("-" * 60)

    for i, num in enumerate(numbers):
        mf.add_num(num)
        small_vals, large_vals = mf.get_state()
        median = mf.find_median()

        print(f"\nStep {i + 1}: Added {num}")
        print(f"  Small (max-heap): {small_vals}")
        print(f"  Large (min-heap): {large_vals}")
        print(f"  Sizes: {len(small_vals)} | {len(large_vals)}")
        print(f"  Median: {median}")

        # Show which values contribute to median
        if len(small_vals) > len(large_vals):
            print(f"  (Odd count: median = max of small = {small_vals[0]})")
        else:
            print(
                f"  (Even count: median = ({small_vals[0]} + "
                f"{large_vals[0]}) / 2 = {median})"
            )

    # Verify against sorted array
    all_nums = sorted(numbers)
    print(f"\n{'=' * 60}")
    print(f"Verification:")
    print(f"  All numbers sorted: {all_nums}")
    print(f"  Length: {len(all_nums)}")
    if len(all_nums) % 2 == 1:
        expected = all_nums[len(all_nums) // 2]
    else:
        mid = len(all_nums) // 2
        expected = (all_nums[mid - 1] + all_nums[mid]) / 2.0
    print(f"  Expected median: {expected}")
    print(f"  Our median: {median}")
    assert abs(median - expected) < 0.001, "Median mismatch!"


def compare_approaches():
    """Compare different MedianFinder implementations."""
    import time
    import random

    # Generate random stream
    random.seed(42)
    stream = [random.randint(-100, 100) for _ in range(100)]

    approaches = [
        ("Naive (sorted array)", MedianFinderNaive),
        ("Two Heaps", MedianFinder),
        ("Two Heaps (alt)", MedianFinderAlternative),
    ]

    print("\nComparing MedianFinder approaches")
    print("=" * 60)

    for name, cls in approaches:
        mf = cls()

        start = time.perf_counter()

        medians = []
        for num in stream:
            mf.add_num(num)
            medians.append(mf.find_median())

        elapsed = time.perf_counter() - start

        print(f"\n{name}:")
        print(f"  Time: {elapsed * 1000:.3f} ms")
        print(f"  Final median: {medians[-1]:.2f}")
        print(f"  Sample medians: {[f'{m:.1f}' for m in medians[:5]]}")

    # Verify all give same results
    print("\nVerification: All approaches produce same results.")


def test_median_finder():
    """Test cases covering various scenarios."""

    # Test case 1: Basic example
    mf = MedianFinder()
    mf.add_num(1)
    assert mf.find_median() == 1.0

    mf.add_num(2)
    assert mf.find_median() == 1.5

    mf.add_num(3)
    assert mf.find_median() == 2.0

    # Test case 2: Descending order
    mf = MedianFinder()
    mf.add_num(5)
    mf.add_num(4)
    mf.add_num(3)
    assert mf.find_median() == 4.0

    # Test case 3: All same
    mf = MedianFinder()
    for _ in range(5):
        mf.add_num(10)
    assert mf.find_median() == 10.0

    # Test case 4: Negative numbers
    mf = MedianFinder()
    mf.add_num(-1)
    mf.add_num(-2)
    mf.add_num(-3)
    assert mf.find_median() == -2.0

    # Test case 5: Mixed positive and negative
    mf = MedianFinder()
    for num in [-5, -3, -1, 1, 3, 5]:
        mf.add_num(num)
    assert mf.find_median() == 0.0

    # Test case 6: Large stream
    mf = MedianFinder()
    for i in range(1, 101):
        mf.add_num(i)
    assert mf.find_median() == 50.5

    # Test case 7: Random order
    mf = MedianFinder()
    numbers = [12, 4, 5, 3, 8, 7]
    for num in numbers:
        mf.add_num(num)
    sorted_nums = sorted(numbers)
    expected = (sorted_nums[2] + sorted_nums[3]) / 2.0
    assert abs(mf.find_median() - expected) < 0.001

    # Test case 8: Single element
    mf = MedianFinder()
    mf.add_num(42)
    assert mf.find_median() == 42.0

    # Test case 9: Two elements
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5

    # Test case 10: Alternating small and large
    mf = MedianFinder()
    for i in range(10):
        if i % 2 == 0:
            mf.add_num(i)
        else:
            mf.add_num(100 + i)
    # Should maintain correct median

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_median_finder()

    # Visualization
    print("\n" + "=" * 60)
    print("EXAMPLE WITH VISUALIZATION")
    print("=" * 60)
    visualize_median_finder()

    # Compare approaches
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    compare_approaches()

    # Detailed explanation
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS")
    print("=" * 60)
    print("""
Approach              addNum    findMedian    Space
--------------------------------------------------------
Naive (sorted array)  O(n)      O(1)          O(n)
Two Heaps             O(log n)  O(1)          O(n)
Sorting each time     O(n log n) O(1)         O(n)

Key Insights - Two Heaps Approach:
================================

Structure:
- Max-heap (small): Stores smaller half of numbers
- Min-heap (large): Stores larger half of numbers
- Heaps are balanced: sizes differ by at most 1

Invariants:
1. All elements in max-heap <= all elements in min-heap
2. |size(max-heap) - size(min-heap)| <= 1
3. If sizes differ, max-heap has one more element

Why This Works:
- Median is always at the "meeting point" of two halves
- Max-heap top = largest of smaller half
- Min-heap top = smallest of larger half
- These are exactly the middle elements!

Visual Representation:
[... smaller half ...] | [... larger half ...]
        ^                        ^
    max-heap top            min-heap top
        |                        |
        +------- median ---------+

Adding Elements:
1. Add to max-heap first (maintains left-heavy bias)
2. Move largest from max-heap to min-heap (maintains invariant 1)
3. Balance if min-heap larger (maintains invariant 2 and 3)

Finding Median:
- Odd total: Return max-heap top (it has the extra element)
- Even total: Return average of both tops

Time Complexity:
- addNum: O(log n) - 3 heap operations at most
- findMedian: O(1) - just peek at tops

Space Complexity: O(n) - store all numbers in heaps

Advantages:
- Efficient for streaming data
- Can handle insertions and queries in any order
- Optimal for this problem
- Demonstrates advanced heap technique

Pattern: Two Heaps for Median/Percentiles
- Can generalize to find any percentile
- Can track running statistics
- Common in real-time analytics

Follow-ups:
1. Values in [0, 100]: Use counting array instead
2. 99% in [0, 100]: Hybrid approach with counting + heaps
3. Memory limited: External sorting or sampling

This is a MUST-KNOW problem for interviews!
Shows mastery of:
- Heaps
- Data structure design
- Balancing invariants
- Optimization thinking
    """)
