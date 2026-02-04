"""
Daily Temperatures (LeetCode #739)

Problem:
Given an array of integers temperatures represents the daily temperatures, return
an array answer such that answer[i] is the number of days you have to wait after
the ith day to get a warmer temperature. If there is no future day for which this
is possible, keep answer[i] == 0 instead.

Example 1:
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
Explanation:
- Day 0 (73): Next warmer is day 1 (74), wait 1 day
- Day 1 (74): Next warmer is day 2 (75), wait 1 day
- Day 2 (75): Next warmer is day 6 (76), wait 4 days
- Day 3 (71): Next warmer is day 5 (72), wait 2 days
- Day 4 (69): Next warmer is day 5 (72), wait 1 day
- Day 5 (72): Next warmer is day 6 (76), wait 1 day
- Day 6 (76): No warmer day, wait 0 days
- Day 7 (73): No warmer day, wait 0 days

Example 2:
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]

Example 3:
Input: temperatures = [30,60,90]
Output: [1,1,0]

Constraints:
- 1 <= temperatures.length <= 10^5
- 30 <= temperatures[i] <= 100
"""


def daily_temperatures(temperatures):
    """
    Monotonic stack approach - optimal solution.

    Approach:
    1. Use a stack to store indices of days (not temperatures)
    2. For each day, check if current temp is warmer than days in stack
    3. If warmer, pop those days and record the wait time (current - popped)
    4. Push current day's index to stack
    5. Days remaining in stack have no warmer future day

    Why this works:
    - Stack maintains indices in decreasing order of temperature
    - When we find a warmer day, it resolves all colder days in stack
    - Each index is pushed once and popped once = O(n) total

    This is a classic "next greater element" problem solved with
    monotonic decreasing stack.

    Time Complexity: O(n) - each element pushed and popped once
    Space Complexity: O(n) - worst case all elements in stack (decreasing sequence)

    Args:
        temperatures: List of daily temperatures

    Returns:
        List of days to wait for warmer temperature
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Store indices

    for i, temp in enumerate(temperatures):
        # While current temp is warmer than top of stack
        while stack and temperatures[stack[-1]] < temp:
            # Found warmer day for the day at top of stack
            prev_index = stack.pop()
            result[prev_index] = i - prev_index

        # Push current day to stack
        stack.append(i)

    # Days remaining in stack have no warmer future day (already 0)
    return result


def daily_temperatures_brute_force(temperatures):
    """
    Brute force approach - check all future days.

    Approach:
    For each day, scan all future days to find next warmer.

    Time Complexity: O(n²) - for each day, potentially scan all remaining days
    Space Complexity: O(1) - only output array

    This is too slow for large inputs but good for understanding the problem.
    """
    n = len(temperatures)
    result = [0] * n

    for i in range(n):
        # Look for next warmer day
        for j in range(i + 1, n):
            if temperatures[j] > temperatures[i]:
                result[i] = j - i
                break

    return result


def daily_temperatures_backward(temperatures):
    """
    Backward iteration with jump optimization.

    Approach:
    - Iterate backwards through temperatures
    - For each day, look forward but skip ahead using previous results
    - If next day is warmer, we're done
    - Otherwise, jump to when next day gets its warmer day

    Time Complexity: O(n) - amortized (each position visited limited times)
    Space Complexity: O(1) - only output array

    This is clever but less intuitive than monotonic stack.
    """
    n = len(temperatures)
    result = [0] * n

    for i in range(n - 1, -1, -1):
        j = i + 1

        while j < n:
            if temperatures[j] > temperatures[i]:
                result[i] = j - i
                break

            if result[j] == 0:
                # No warmer day found for j, so no warmer day for i
                break

            # Jump to when j gets its warmer day
            j += result[j]

    return result


def test_daily_temperatures():
    """Test cases covering various scenarios."""

    # Test all implementations
    implementations = [
        ("Monotonic Stack", daily_temperatures),
        ("Brute Force", daily_temperatures_brute_force),
        ("Backward Jump", daily_temperatures_backward)
    ]

    test_cases = [
        # (input, expected)
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),
        ([30, 60, 90], [1, 1, 0]),
        ([100], [0]),
        ([90, 80, 70, 60], [0, 0, 0, 0]),
        ([30, 30, 30, 30], [0, 0, 0, 0]),
        ([40, 35, 30, 25, 50], [4, 3, 2, 1, 0]),
        ([75, 71, 69, 72, 76], [4, 2, 1, 1, 0])
    ]

    for name, func in implementations:
        print(f"\nTesting {name}...")

        for temps, expected in test_cases:
            result = func(temps)
            assert result == expected, f"Failed for {temps}: got {result}, expected {expected}"

        print(f"  {name} passed all tests!")

    print("\nAll implementations passed!")


def demonstrate_stack_operations(temperatures):
    """Visualize how the monotonic stack works."""

    print(f"\n=== Stack Operations for {temperatures} ===\n")

    n = len(temperatures)
    result = [0] * n
    stack = []

    for i, temp in enumerate(temperatures):
        print(f"Day {i}: Temperature = {temp}")

        # Show what happens while stack has smaller temperatures
        resolved = []
        while stack and temperatures[stack[-1]] < temp:
            prev_idx = stack.pop()
            wait = i - prev_idx
            result[prev_idx] = wait
            resolved.append((prev_idx, temperatures[prev_idx], wait))

        if resolved:
            print(f"  Resolved days (found their warmer day):")
            for idx, prev_temp, wait in resolved:
                print(f"    Day {idx} ({prev_temp}) -> wait {wait} days")
        else:
            print(f"  No days resolved")

        stack.append(i)
        print(f"  Push day {i} to stack")
        print(f"  Stack (indices): {stack}")
        print(f"  Stack (temps): {[temperatures[idx] for idx in stack]}")
        print(f"  Result so far: {result}")
        print()

    if stack:
        print(f"Final: Days {stack} have no warmer future day")
        print(f"       Temperatures: {[temperatures[idx] for idx in stack]}")
        print()

    print(f"Final result: {result}")
    return result


def compare_approaches():
    """Compare different approaches with timing."""

    import time

    temperatures = [73, 74, 75, 71, 69, 72, 76, 73]

    print("\n=== Approach Comparison ===\n")

    # Monotonic stack
    start = time.perf_counter()
    result1 = daily_temperatures(temperatures)
    time1 = time.perf_counter() - start
    print(f"Monotonic Stack: {result1}")
    print(f"  Time: {time1*1000:.4f}ms")
    print(f"  Complexity: O(n)")
    print(f"  Each element pushed/popped once")
    print()

    # Brute force
    start = time.perf_counter()
    result2 = daily_temperatures_brute_force(temperatures)
    time2 = time.perf_counter() - start
    print(f"Brute Force: {result2}")
    print(f"  Time: {time2*1000:.4f}ms")
    print(f"  Complexity: O(n²)")
    print(f"  Nested loops checking all future days")
    print()

    # Backward jump
    start = time.perf_counter()
    result3 = daily_temperatures_backward(temperatures)
    time3 = time.perf_counter() - start
    print(f"Backward Jump: {result3}")
    print(f"  Time: {time3*1000:.4f}ms")
    print(f"  Complexity: O(n) amortized")
    print(f"  Clever jumping but less intuitive")
    print()

    print(f"All approaches produce same result: {result1 == result2 == result3}")


def explain_monotonic_stack():
    """Explain the monotonic stack concept."""

    print("\n=== Understanding Monotonic Stack ===\n")

    print("What is a Monotonic Stack?")
    print("  A stack that maintains elements in sorted order")
    print("  - Monotonic increasing: smallest to largest")
    print("  - Monotonic decreasing: largest to smallest")
    print()

    print("For Daily Temperatures:")
    print("  We use a DECREASING monotonic stack")
    print("  Stack stores indices in order of decreasing temperature")
    print()

    print("Key Insight:")
    print("  When we find a warmer day, it resolves ALL colder days in stack")
    print("  Those days were waiting for their next warmer day - found it!")
    print()

    print("Why O(n)?")
    print("  Each element is:")
    print("    - Pushed to stack exactly once")
    print("    - Popped from stack at most once")
    print("  Total operations: 2n = O(n)")
    print()

    print("Pattern Recognition:")
    print("  'Next greater/smaller element' problems → Monotonic stack")
    print("  'Daily temperatures' is 'next greater element'")
    print()


def related_problems():
    """Show related problems using same pattern."""

    print("\n=== Related Monotonic Stack Problems ===\n")

    problems = [
        {
            "name": "Next Greater Element I",
            "pattern": "Monotonic decreasing stack",
            "description": "Find next greater element for each element"
        },
        {
            "name": "Next Greater Element II",
            "pattern": "Monotonic decreasing stack + circular",
            "description": "Same but array is circular"
        },
        {
            "name": "Stock Span Problem",
            "pattern": "Monotonic decreasing stack",
            "description": "Days until previous higher price"
        },
        {
            "name": "Largest Rectangle in Histogram",
            "pattern": "Monotonic increasing stack",
            "description": "Find largest rectangle using heights"
        },
        {
            "name": "Trapping Rain Water",
            "pattern": "Monotonic decreasing stack",
            "description": "Calculate water trapped between bars"
        }
    ]

    for problem in problems:
        print(f"{problem['name']}")
        print(f"  Pattern: {problem['pattern']}")
        print(f"  Description: {problem['description']}")
        print()


if __name__ == "__main__":
    # Run tests
    test_daily_temperatures()

    # Explain concept
    explain_monotonic_stack()

    # Demonstrate with visualization
    demonstrate_stack_operations([73, 74, 75, 71, 69, 72, 76, 73])

    # Compare approaches
    compare_approaches()

    # Show related problems
    related_problems()
