"""
Climbing Stairs (LeetCode #70)

Problem:
You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways
can you climb to the top?

Example 1:
Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

Example 2:
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

Constraints:
- 1 <= n <= 45
"""


def climb_stairs_recursive(n):
    """
    Naive recursive approach - exponential time.

    Intuition:
    To reach step n, we must have come from either:
    - Step n-1 (then take 1 step)
    - Step n-2 (then take 2 steps)

    So: ways(n) = ways(n-1) + ways(n-2)
    This is the Fibonacci sequence!

    Problem: Massive redundant calculations
    - ways(5) calls ways(4) and ways(3)
    - ways(4) calls ways(3) and ways(2)
    - ways(3) is calculated twice, ways(2) even more times!

    Time Complexity: O(2^n) - exponential
    Space Complexity: O(n) - recursion call stack

    Args:
        n: Number of steps

    Returns:
        Number of distinct ways to climb to the top
    """
    # Base cases
    if n <= 2:
        return n

    # Recursive case: sum of two previous states
    return climb_stairs_recursive(n - 1) + climb_stairs_recursive(n - 2)


def climb_stairs_memoization(n, memo=None):
    """
    Top-down DP with memoization - store computed results.

    Approach:
    Same recursive logic, but store results in a dictionary to avoid
    recomputation. First time we compute ways(k), we save it. Next time
    we need ways(k), we just look it up.

    Why it works:
    - There are only n unique subproblems (ways(1), ways(2), ..., ways(n))
    - Each is computed once and stored
    - Lookups are O(1)

    Time Complexity: O(n) - compute each of n states once
    Space Complexity: O(n) - memo dictionary + recursion stack

    Args:
        n: Number of steps
        memo: Dictionary storing computed results

    Returns:
        Number of distinct ways to climb to the top
    """
    # Initialize memo on first call
    if memo is None:
        memo = {}

    # Base cases
    if n <= 2:
        return n

    # Check if already computed
    if n in memo:
        return memo[n]

    # Compute and store result
    memo[n] = climb_stairs_memoization(n - 1, memo) + \
              climb_stairs_memoization(n - 2, memo)

    return memo[n]


def climb_stairs_tabulation(n):
    """
    Bottom-up DP with tabulation - build table iteratively.

    Approach:
    Build a table from smallest subproblems up to n.
    - dp[i] = number of ways to reach step i
    - Start with base cases: dp[1] = 1, dp[2] = 2
    - For each step i, dp[i] = dp[i-1] + dp[i-2]

    Why bottom-up is better:
    - No recursion overhead
    - More cache-friendly (sequential access)
    - Easier to optimize space
    - Preferred in interviews

    Time Complexity: O(n) - single loop
    Space Complexity: O(n) - dp array

    Args:
        n: Number of steps

    Returns:
        Number of distinct ways to climb to the top
    """
    # Handle edge cases
    if n <= 2:
        return n

    # Create DP table
    dp = [0] * (n + 1)

    # Base cases
    dp[1] = 1  # One way to reach step 1
    dp[2] = 2  # Two ways to reach step 2

    # Fill table bottom-up
    for i in range(3, n + 1):
        # To reach step i, we can come from step i-1 or i-2
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def climb_stairs_optimized(n):
    """
    Space-optimized DP - only track last two values.

    Approach:
    Notice that to compute dp[i], we only need dp[i-1] and dp[i-2].
    We don't need the entire array! Just keep two variables for the
    last two values.

    Space Optimization:
    - Observation: dp[i] only depends on dp[i-1] and dp[i-2]
    - Don't need to store all values from 1 to n
    - Just keep track of previous two values
    - Update them as we go

    Time Complexity: O(n) - single loop
    Space Complexity: O(1) - only two variables

    Args:
        n: Number of steps

    Returns:
        Number of distinct ways to climb to the top
    """
    # Handle edge cases
    if n <= 2:
        return n

    # Only need last two values
    prev2 = 1  # ways(1)
    prev1 = 2  # ways(2)

    # Build up from 3 to n
    for i in range(3, n + 1):
        current = prev1 + prev2
        # Shift values for next iteration
        prev2 = prev1
        prev1 = current

    return prev1


def visualize_dp_table(n):
    """
    Helper function to visualize the DP table building process.
    Shows how each step builds on previous steps.
    """
    if n <= 0:
        return

    dp = [0] * (n + 1)
    dp[0] = 0
    if n >= 1:
        dp[1] = 1
    if n >= 2:
        dp[2] = 2

    print(f"Building DP table for n = {n}:")
    print(f"dp[0] = 0 (base)")
    if n >= 1:
        print(f"dp[1] = 1 (base)")
    if n >= 2:
        print(f"dp[2] = 2 (base)")
    print()

    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        print(f"dp[{i}] = dp[{i-1}] + dp[{i-2}] = {dp[i-1]} + {dp[i-2]} = {dp[i]}")

    print(f"\nFinal answer: {dp[n]} ways to climb {n} steps")
    print(f"Pattern is Fibonacci: 1, 2, 3, 5, 8, 13, 21, 34, ...")


def test_climbing_stairs():
    """Test cases covering various scenarios."""

    # Test all approaches give same answer
    test_cases = [1, 2, 3, 4, 5, 10, 20]

    for n in test_cases:
        result_memo = climb_stairs_memoization(n)
        result_tab = climb_stairs_tabulation(n)
        result_opt = climb_stairs_optimized(n)

        assert result_memo == result_tab == result_opt, \
            f"Mismatch for n={n}: memo={result_memo}, tab={result_tab}, opt={result_opt}"

    # Specific test cases
    assert climb_stairs_optimized(1) == 1
    assert climb_stairs_optimized(2) == 2
    assert climb_stairs_optimized(3) == 3
    assert climb_stairs_optimized(4) == 5
    assert climb_stairs_optimized(5) == 8
    assert climb_stairs_optimized(10) == 89

    print("All test cases passed!")


def compare_performance():
    """Compare execution characteristics of different approaches."""
    import time

    print("Performance Comparison:")
    print("=" * 60)

    # Test with n=30 (recursive would be too slow for larger values)
    n = 30

    # Memoization
    start = time.time()
    result_memo = climb_stairs_memoization(n)
    time_memo = time.time() - start

    # Tabulation
    start = time.time()
    result_tab = climb_stairs_tabulation(n)
    time_tab = time.time() - start

    # Optimized
    start = time.time()
    result_opt = climb_stairs_optimized(n)
    time_opt = time.time() - start

    print(f"n = {n}, Result = {result_memo}\n")
    print(f"Memoization: {time_memo*1000:.4f} ms (Top-down, recursive)")
    print(f"Tabulation:  {time_tab*1000:.4f} ms (Bottom-up, O(n) space)")
    print(f"Optimized:   {time_opt*1000:.4f} ms (Bottom-up, O(1) space)")
    print("\nNote: Optimized is usually fastest due to better cache locality")


if __name__ == "__main__":
    # Run tests
    test_climbing_stairs()
    print()

    # Visualize DP table
    visualize_dp_table(7)
    print()

    # Performance comparison
    compare_performance()
    print()

    # Example usage
    n = 5
    print(f"Example: n = {n}")
    print(f"Number of ways to climb {n} steps: {climb_stairs_optimized(n)}")
    print("\nThe ways are:")
    print("1. 1+1+1+1+1")
    print("2. 1+1+1+2")
    print("3. 1+1+2+1")
    print("4. 1+2+1+1")
    print("5. 2+1+1+1")
    print("6. 1+2+2")
    print("7. 2+1+2")
    print("8. 2+2+1")
