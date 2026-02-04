"""
Koko Eating Bananas (LeetCode #875)

Problem:
Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas.
The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile
of bananas and eats k bananas from that pile. If the pile has less than k bananas, she
eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the
guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

Example 1:
Input: piles = [3,6,7,11], h = 8
Output: 4
Explanation:
- Pile 0: ceil(3/4) = 1 hour
- Pile 1: ceil(6/4) = 2 hours
- Pile 2: ceil(7/4) = 2 hours
- Pile 3: ceil(11/4) = 3 hours
Total: 1 + 2 + 2 + 3 = 8 hours

Example 2:
Input: piles = [30,11,23,4,20], h = 5
Output: 30
Explanation: With k=30, Koko eats one pile per hour (5 piles in 5 hours).

Example 3:
Input: piles = [30,11,23,4,20], h = 6
Output: 23
Explanation: With k=23, she takes ceil(30/23)=2 + ceil(11/23)=1 + ceil(23/23)=1 +
ceil(4/23)=1 + ceil(20/23)=1 = 6 hours total.

Constraints:
- 1 <= piles.length <= 10^4
- piles.length <= h <= 10^9
- 1 <= piles[i] <= 10^9
"""

import math


def min_eating_speed(piles, h):
    """
    Binary search on the answer space to find minimum eating speed.

    Key Insight:
    This is a "minimize the maximum" problem. We're searching for the minimum
    speed k that allows Koko to finish in time. The answer space is [1, max(piles)].

    Why Binary Search?
    - If speed k works, any speed > k also works (monotonic property)
    - If speed k doesn't work, any speed < k also doesn't work
    - This monotonic property allows binary search

    Approach:
    1. Search space: [1, max(piles)] (min speed is 1, max needed is max pile)
    2. For each candidate speed k, calculate time needed
    3. If time <= h, try slower (search left)
    4. If time > h, need faster (search right)

    Time Complexity: O(n * log m)
    - Binary search: O(log m) where m = max(piles)
    - Each iteration checks all piles: O(n)

    Space Complexity: O(1)

    Args:
        piles: List of pile sizes
        h: Hours available

    Returns:
        Minimum eating speed k
    """
    # Search space: [1, max(piles)]
    # Min speed: 1 banana/hour
    # Max speed needed: eat the largest pile in 1 hour
    left = 1
    right = max(piles)

    while left < right:
        mid = left + (right - left) // 2

        # Calculate hours needed at speed mid
        hours_needed = 0
        for pile in piles:
            # Time to eat this pile: ceil(pile / mid)
            hours_needed += math.ceil(pile / mid)

        # If we can finish in time with speed mid
        if hours_needed <= h:
            # Try slower speed (search left)
            right = mid
        else:
            # Need faster speed (search right)
            left = mid + 1

    # When left == right, we found the minimum speed
    return left


def min_eating_speed_no_math_import(piles, h):
    """
    Same algorithm but without using math.ceil().

    Ceiling division trick: ceil(a/b) = (a + b - 1) // b

    This is useful when you want to avoid imports or in languages
    without a built-in ceiling function.

    Time Complexity: O(n * log m)
    Space Complexity: O(1)
    """
    left = 1
    right = max(piles)

    while left < right:
        mid = left + (right - left) // 2

        hours_needed = 0
        for pile in piles:
            # Ceiling division: (pile + mid - 1) // mid
            hours_needed += (pile + mid - 1) // mid

        if hours_needed <= h:
            right = mid
        else:
            left = mid + 1

    return left


def min_eating_speed_with_explanation(piles, h):
    """
    Same algorithm with detailed explanation of each step.
    Useful for understanding the process.
    """
    left = 1
    right = max(piles)

    print(f"Finding minimum eating speed for:")
    print(f"Piles: {piles}")
    print(f"Hours available: {h}")
    print(f"Search space: [1, {right}] (speeds in bananas/hour)")
    print("=" * 70)

    iteration = 0

    while left < right:
        iteration += 1
        mid = left + (right - left) // 2

        # Calculate hours needed at this speed
        hours_breakdown = []
        hours_needed = 0
        for i, pile in enumerate(piles):
            pile_hours = math.ceil(pile / mid)
            hours_needed += pile_hours
            hours_breakdown.append(f"pile[{i}]={pile} → {pile_hours}h")

        print(f"\nIteration {iteration}: Testing speed k={mid}")
        print(f"  Time breakdown: {', '.join(hours_breakdown)}")
        print(f"  Total hours needed: {hours_needed}")

        if hours_needed <= h:
            print(f"  ✓ {hours_needed} <= {h}: This speed works!")
            print(f"  → Try slower speed (search left half)")
            right = mid
        else:
            print(f"  ✗ {hours_needed} > {h}: Too slow!")
            print(f"  → Need faster speed (search right half)")
            left = mid + 1

        print(f"  New search space: [{left}, {right}]")

    print(f"\n{'='*70}")
    print(f"Minimum eating speed: {left} bananas/hour")
    return left


def can_finish_in_time(piles, h, k):
    """
    Helper function: Check if Koko can finish with speed k in h hours.

    This is the feasibility check function used in binary search.

    Args:
        piles: List of pile sizes
        h: Hours available
        k: Eating speed (bananas per hour)

    Returns:
        True if can finish in time, False otherwise
    """
    hours_needed = sum(math.ceil(pile / k) for pile in piles)
    return hours_needed <= h


def find_all_valid_speeds(piles, h):
    """
    Find all valid eating speeds (for visualization purposes).

    This is NOT efficient for large inputs (O(n * m) where m = max pile).
    Only use for small examples to understand the problem.

    Returns:
        List of (speed, hours_needed) tuples
    """
    results = []
    max_speed = max(piles)

    for speed in range(1, max_speed + 1):
        hours_needed = sum(math.ceil(pile / speed) for pile in piles)
        valid = "✓" if hours_needed <= h else "✗"
        results.append((speed, hours_needed, valid))

    return results


def visualize_eating_process(piles, h, k):
    """
    Visualize how Koko eats bananas at a given speed.
    """
    print(f"\nSimulating Koko eating at speed k={k}:")
    print(f"Piles: {piles}, Hours available: {h}")
    print("=" * 60)

    total_hours = 0
    for i, pile in enumerate(piles):
        hours_for_pile = math.ceil(pile / k)
        total_hours += hours_for_pile

        print(f"\nPile {i}: {pile} bananas")
        print(f"  At speed {k}/hour: needs {hours_for_pile} hours")

        # Show hour-by-hour breakdown
        remaining = pile
        hour = 0
        while remaining > 0:
            hour += 1
            eaten = min(k, remaining)
            remaining -= eaten
            print(f"    Hour {hour}: eat {eaten} bananas, {remaining} left")

    print(f"\n{'='*60}")
    print(f"Total time: {total_hours} hours")

    if total_hours <= h:
        print(f"✓ Success! Finished in time ({total_hours} <= {h})")
    else:
        print(f"✗ Failed! Too slow ({total_hours} > {h})")

    return total_hours


def visualize_speed_analysis(piles, h):
    """
    Show how different speeds affect the total time.
    Only practical for small examples.
    """
    print(f"\nAnalyzing all speeds for piles={piles}, h={h}")
    print("=" * 60)

    max_speed = max(piles)
    print(f"\nSpeed | Hours Needed | Valid?")
    print("-" * 40)

    min_valid = None

    for speed in range(1, min(max_speed + 1, 20)):  # Limit to 20 for readability
        hours = sum(math.ceil(pile / speed) for pile in piles)
        valid = hours <= h

        status = "✓ YES" if valid else "✗ NO"
        marker = " ← Minimum" if valid and min_valid is None else ""

        if valid and min_valid is None:
            min_valid = speed

        print(f"{speed:5d} | {hours:12d} | {status:6s}{marker}")

    print(f"\nMinimum valid speed: {min_valid}")


def test_min_eating_speed():
    """Comprehensive test cases."""

    # Test case 1: Standard case
    assert min_eating_speed([3, 6, 7, 11], 8) == 4

    # Test case 2: Exactly one pile per hour
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30

    # Test case 3: One more hour available
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23

    # Test case 4: Plenty of time
    assert min_eating_speed([3, 6, 7, 11], 100) == 1

    # Test case 5: Minimal time (one hour per pile)
    assert min_eating_speed([3, 6, 7, 11], 4) == 11

    # Test case 6: Single pile
    assert min_eating_speed([100], 10) == 10
    assert min_eating_speed([100], 5) == 20

    # Test case 7: All piles same size
    assert min_eating_speed([5, 5, 5, 5], 8) == 3
    assert min_eating_speed([5, 5, 5, 5], 4) == 5

    # Test case 8: Two piles
    assert min_eating_speed([3, 6], 3) == 3
    assert min_eating_speed([3, 6], 4) == 3

    # Test case 9: Large numbers
    piles = [1000000000]
    h = 2
    expected = 500000000
    assert min_eating_speed(piles, h) == expected

    # Verify both implementations match
    test_cases = [
        ([3, 6, 7, 11], 8),
        ([30, 11, 23, 4, 20], 5),
        ([30, 11, 23, 4, 20], 6),
    ]

    for piles, h in test_cases:
        result1 = min_eating_speed(piles, h)
        result2 = min_eating_speed_no_math_import(piles, h)
        assert result1 == result2, f"Mismatch for {piles}, {h}"

    print("All test cases passed!")


def demonstrate_binary_search_pattern():
    """
    Explain why this is a binary search problem.
    """
    print("\n" + "="*60)
    print("WHY BINARY SEARCH?")
    print("="*60)

    print("\nThis problem has the 'monotonic property':")
    print("\n1. If speed k works (finishes in time):")
    print("   → Any speed > k also works (faster is always better)")
    print("\n2. If speed k doesn't work (too slow):")
    print("   → Any speed < k also doesn't work (slower is worse)")

    print("\nThis creates a sorted answer space:")
    print("  [1, 2, 3, ..., k-1, k, k+1, ..., max]")
    print("   ✗  ✗  ✗  ...  ✗   ✓   ✓   ...  ✓")
    print("                      ↑")
    print("                 Find this!")

    print("\nWe use binary search to find the FIRST valid speed.")
    print("This is the 'leftmost True' binary search pattern.")


def demonstrate_ceiling_division():
    """
    Explain the ceiling division trick.
    """
    print("\n" + "="*60)
    print("CEILING DIVISION TRICK")
    print("="*60)

    print("\nWhen dividing pile by speed, we need ceiling:")
    print("- If pile=7 and speed=4: takes ceil(7/4)=ceil(1.75)=2 hours")
    print("- Regular division 7//4=1 is wrong (underestimates time)")

    print("\nTwo ways to compute ceiling:")

    examples = [(7, 4), (8, 4), (11, 3), (10, 5)]

    print(f"\n{'Pile':>5} | {'Speed':>5} | {'math.ceil':>10} | {'Trick':>10}")
    print("-" * 45)

    for pile, speed in examples:
        method1 = math.ceil(pile / speed)
        method2 = (pile + speed - 1) // speed
        print(f"{pile:5d} | {speed:5d} | {method1:10d} | {method2:10d}")

    print("\nTrick: ceil(a/b) = (a + b - 1) // b")
    print("This avoids floating point and imports!")


def compare_with_linear_search():
    """
    Show why binary search is better than linear search.
    """
    import time

    print("\n" + "="*60)
    print("BINARY SEARCH vs LINEAR SEARCH")
    print("="*60)

    piles = [10**9] * 100  # Large piles
    h = 10**9

    # Linear search (would be too slow in practice)
    print("\nLinear search: Try speeds 1, 2, 3, ... until one works")
    print("  Time complexity: O(n * m) where m = max(piles)")
    print("  For this example: ~10^9 iterations - TOO SLOW!")

    # Binary search
    print("\nBinary search: Use monotonic property")
    print("  Time complexity: O(n * log m)")
    start = time.time()
    result = min_eating_speed(piles[:10], h)  # Use smaller subset
    elapsed = time.time() - start
    print(f"  For subset of 10 piles: {elapsed*1000:.4f} ms")
    print(f"  Result: {result}")

    print("\nBinary search is MUCH faster for large inputs!")


if __name__ == "__main__":
    # Run tests
    test_min_eating_speed()

    # Demonstrate why binary search works
    demonstrate_binary_search_pattern()

    # Explain ceiling division
    demonstrate_ceiling_division()

    # Visualization examples
    print("\n" + "="*60)
    print("VISUALIZATION EXAMPLES")
    print("="*60)

    print("\nExample 1: Standard case")
    print("-" * 60)
    piles1 = [3, 6, 7, 11]
    h1 = 8
    visualize_speed_analysis(piles1, h1)

    print("\n" + "-" * 60)
    print("\nExample 2: Eating process at k=4")
    print("-" * 60)
    visualize_eating_process(piles1, h1, 4)

    print("\n" + "-" * 60)
    print("\nExample 3: Too slow (k=3)")
    print("-" * 60)
    visualize_eating_process(piles1, h1, 3)

    # Show detailed search process
    print("\n" + "="*60)
    print("DETAILED SEARCH PROCESS")
    print("="*60)

    print("\nExample 1: piles=[3,6,7,11], h=8")
    print("-" * 60)
    min_eating_speed_with_explanation([3, 6, 7, 11], 8)

    print("\n" + "-" * 60)
    print("\nExample 2: piles=[30,11,23,4,20], h=6")
    print("-" * 60)
    min_eating_speed_with_explanation([30, 11, 23, 4, 20], 6)

    # Compare approaches
    print("\n" + "="*60)
    compare_with_linear_search()
