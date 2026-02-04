"""
House Robber (LeetCode #198)

Problem:
You are a professional robber planning to rob houses along a street. Each house has
a certain amount of money stashed, the only constraint stopping you from robbing each
of them is that adjacent houses have security systems connected and it will automatically
contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the
maximum amount of money you can rob tonight without alerting the police.

Example 1:
Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

Example 2:
Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 400

KEY INSIGHT:
At each house, you have two choices:
1. Rob this house: Take money + max from houses before previous (can't rob adjacent)
2. Skip this house: Take max from houses including previous

Choose the option that gives more money.
"""


def rob(nums):
    """
    Dynamic Programming solution - iterative with array.

    State Definition:
    dp[i] = maximum money that can be robbed from houses 0 to i

    Recurrence Relation:
    dp[i] = max(
        dp[i-1],              # Skip current house
        nums[i] + dp[i-2]     # Rob current house + max from i-2
    )

    Base Cases:
    dp[0] = nums[0]              # Only one house, rob it
    dp[1] = max(nums[0], nums[1]) # Two houses, rob the richer one

    Example: nums = [2,7,9,3,1]

    House:    0  1  2  3  4
    Money:    2  7  9  3  1

    dp[0] = 2                           (rob house 0)
    dp[1] = max(2, 7) = 7               (rob house 1)
    dp[2] = max(7, 9+2) = 11            (rob houses 0,2)
    dp[3] = max(11, 3+7) = 11           (keep previous)
    dp[4] = max(11, 1+11) = 12          (rob houses 0,2,4)

    Time Complexity: O(n)
    - Single pass through array

    Space Complexity: O(n)
    - DP array of size n

    Args:
        nums: Array of money in each house

    Returns:
        Maximum money that can be robbed
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    n = len(nums)
    dp = [0] * n

    # Base cases
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])

    # Fill dp array
    for i in range(2, n):
        # Choose max of:
        # 1. Skip current house: dp[i-1]
        # 2. Rob current house: nums[i] + dp[i-2]
        dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])

    return dp[n - 1]


def rob_space_optimized(nums):
    """
    Space-optimized solution using only two variables.

    Observation: We only need the last two values, not the entire array.

    Time Complexity: O(n)
    Space Complexity: O(1) - only two variables

    This is the preferred solution in interviews.
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    # prev2: max money from houses 0 to i-2
    # prev1: max money from houses 0 to i-1
    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        current = max(prev1, nums[i] + prev2)
        prev2 = prev1
        prev1 = current

    return prev1


def rob_with_houses(nums):
    """
    Extension: Return both max money AND which houses to rob.

    This requires tracking the actual choices made.

    Returns:
        Tuple of (max_money, list_of_house_indices)
    """
    if not nums:
        return 0, []
    if len(nums) == 1:
        return nums[0], [0]

    n = len(nums)
    dp = [0] * n
    choice = [False] * n  # Track if house i is robbed

    # Base cases
    dp[0] = nums[0]
    choice[0] = True

    dp[1] = max(nums[0], nums[1])
    choice[1] = nums[1] > nums[0]

    # Fill arrays
    for i in range(2, n):
        if nums[i] + dp[i - 2] > dp[i - 1]:
            # Rob current house
            dp[i] = nums[i] + dp[i - 2]
            choice[i] = True
        else:
            # Skip current house
            dp[i] = dp[i - 1]
            choice[i] = False

    # Reconstruct which houses were robbed
    robbed_houses = []
    i = n - 1

    while i >= 0:
        if choice[i]:
            robbed_houses.append(i)
            i -= 2  # Skip adjacent house
        else:
            i -= 1

    robbed_houses.reverse()
    return dp[n - 1], robbed_houses


def rob_recursive(nums):
    """
    Recursive solution with memoization (top-down DP).

    This is more intuitive but less efficient due to recursion overhead.

    Time Complexity: O(n)
    Space Complexity: O(n) for memo + O(n) for recursion stack
    """
    memo = {}

    def dp(i):
        """
        Returns max money that can be robbed from houses i to end.
        """
        # Base cases
        if i >= len(nums):
            return 0

        # Check memo
        if i in memo:
            return memo[i]

        # Two choices:
        # 1. Rob house i: nums[i] + dp(i+2)
        # 2. Skip house i: dp(i+1)
        result = max(
            nums[i] + dp(i + 2),  # Rob this house
            dp(i + 1)              # Skip this house
        )

        memo[i] = result
        return result

    return dp(0)


def visualize_rob(nums):
    """
    Visualize the decision-making process step by step.
    """
    print(f"\nRobbing houses: {nums}")
    print("=" * 70)

    if not nums:
        print("No houses to rob!")
        return 0

    if len(nums) == 1:
        print(f"Only one house: rob it for ${nums[0]}")
        return nums[0]

    n = len(nums)
    dp = [0] * n

    # Base cases
    dp[0] = nums[0]
    print(f"\nHouse 0: Money = ${nums[0]}")
    print(f"  dp[0] = {dp[0]} (rob this house)")

    dp[1] = max(nums[0], nums[1])
    print(f"\nHouse 1: Money = ${nums[1]}")
    print(f"  Option 1: Rob house 0 = ${nums[0]}")
    print(f"  Option 2: Rob house 1 = ${nums[1]}")
    print(f"  dp[1] = max({nums[0]}, {nums[1]}) = {dp[1]}")

    # Process remaining houses
    for i in range(2, n):
        skip = dp[i - 1]
        rob = nums[i] + dp[i - 2]

        print(f"\nHouse {i}: Money = ${nums[i]}")
        print(f"  Option 1 (skip): Take dp[{i-1}] = ${skip}")
        print(f"  Option 2 (rob):  Take ${nums[i]} + dp[{i-2}] = ${nums[i]} + ${dp[i-2]} = ${rob}")

        dp[i] = max(skip, rob)

        if rob > skip:
            print(f"  ✓ Rob this house! dp[{i}] = ${dp[i]}")
        else:
            print(f"  ✓ Skip this house. dp[{i}] = ${dp[i]}")

        # Show running dp array
        print(f"  Current DP: {dp[:i+1]}")

    print("\n" + "=" * 70)
    print(f"Maximum money: ${dp[n - 1]}")

    # Show which houses were robbed
    _, robbed = rob_with_houses(nums)
    print(f"Houses to rob: {robbed}")
    print(f"Money from each: {[nums[i] for i in robbed]}")
    print(f"Total: ${sum(nums[i] for i in robbed)}")

    return dp[n - 1]


def visualize_decision_tree(nums):
    """
    Show the decision tree for the recursive approach.
    """
    print(f"\nDecision tree for nums = {nums}")
    print("=" * 60)

    def build_tree(i, depth=0):
        indent = "  " * depth

        # Base case
        if i >= len(nums):
            print(f"{indent}house {i}: out of bounds → $0")
            return

        if depth > 4:  # Limit depth for readability
            print(f"{indent}house {i}: ... (continuing)")
            return

        print(f"{indent}house {i} (money=${nums[i]})")

        # Show two branches
        print(f"{indent}├─ Rob house {i}:")
        if i + 2 < len(nums):
            build_tree(i + 2, depth + 1)
        else:
            print(f"{indent}   → No more houses")

        print(f"{indent}└─ Skip house {i}:")
        if i + 1 < len(nums):
            build_tree(i + 1, depth + 1)
        else:
            print(f"{indent}   → No more houses")

    build_tree(0)


def test_rob():
    """Comprehensive test cases."""

    # Test case 1: Standard example
    assert rob([1, 2, 3, 1]) == 4

    # Test case 2: Longer array
    assert rob([2, 7, 9, 3, 1]) == 12

    # Test case 3: Single house
    assert rob([5]) == 5

    # Test case 4: Two houses
    assert rob([1, 2]) == 2
    assert rob([2, 1]) == 2

    # Test case 5: Three houses
    assert rob([1, 2, 3]) == 4  # Rob houses 0 and 2

    # Test case 6: All same values
    assert rob([5, 5, 5, 5]) == 10  # Rob houses 0 and 2, or 1 and 3

    # Test case 7: Increasing values
    assert rob([1, 2, 3, 4, 5]) == 9  # Rob houses 0, 2, 4

    # Test case 8: Decreasing values
    assert rob([5, 4, 3, 2, 1]) == 9  # Rob houses 0, 2, 4

    # Test case 9: Large gap in middle
    assert rob([2, 1, 1, 2]) == 4  # Rob houses 0 and 3

    # Test case 10: Zeros
    assert rob([0, 0, 0, 0]) == 0
    assert rob([1, 0, 0, 1]) == 2

    # Verify all implementations give same results
    test_cases = [
        [1, 2, 3, 1],
        [2, 7, 9, 3, 1],
        [5, 3, 4, 11, 2],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    ]

    for nums in test_cases:
        r1 = rob(nums)
        r2 = rob_space_optimized(nums)
        r3 = rob_recursive(nums)
        money, _ = rob_with_houses(nums)

        assert r1 == r2 == r3 == money, f"Mismatch for {nums}"

    # Verify robbed houses are valid
    for nums in test_cases:
        money, houses = rob_with_houses(nums)

        # Check no adjacent houses
        for i in range(len(houses) - 1):
            assert houses[i + 1] - houses[i] >= 2, "Adjacent houses robbed!"

        # Check total money
        assert sum(nums[h] for h in houses) == money

    print("All test cases passed!")


def explain_recurrence():
    """
    Explain the recurrence relation in detail.
    """
    print("\n" + "="*60)
    print("UNDERSTANDING THE RECURRENCE RELATION")
    print("="*60)

    print("\nAt each house i, you face a choice:")
    print("\n1. Rob this house:")
    print("   - Take money: nums[i]")
    print("   - Add max from houses up to i-2: dp[i-2]")
    print("   - Total: nums[i] + dp[i-2]")
    print("   - Why i-2? Can't rob i-1 (adjacent)")

    print("\n2. Skip this house:")
    print("   - Take max from houses up to i-1: dp[i-1]")
    print("   - This includes all previous optimizations")

    print("\nRecurrence: dp[i] = max(dp[i-1], nums[i] + dp[i-2])")

    print("\nExample: nums = [2,7,9,3,1]")
    print("\nAt house 2 (money=$9):")
    print("  Option 1 (skip): dp[1] = $7")
    print("  Option 2 (rob):  $9 + dp[0] = $9 + $2 = $11")
    print("  Choose: max($7, $11) = $11 ✓")

    print("\nAt house 3 (money=$3):")
    print("  Option 1 (skip): dp[2] = $11")
    print("  Option 2 (rob):  $3 + dp[1] = $3 + $7 = $10")
    print("  Choose: max($11, $10) = $11 ✓")


def compare_variations():
    """
    Compare with variations of the problem.
    """
    print("\n" + "="*60)
    print("PROBLEM VARIATIONS")
    print("="*60)

    print("\n1. House Robber (this problem):")
    print("   - Linear street")
    print("   - Can't rob adjacent houses")
    print("   - Complexity: O(n) time, O(1) space")

    print("\n2. House Robber II (LeetCode #213):")
    print("   - Circular street (houses in a circle)")
    print("   - First and last houses are adjacent")
    print("   - Solution: Run twice (exclude first OR exclude last)")

    print("\n3. House Robber III (LeetCode #337):")
    print("   - Houses arranged in binary tree")
    print("   - Can't rob parent and child")
    print("   - Solution: Tree DP")


def analyze_complexity():
    """
    Analyze time and space complexity with measurements.
    """
    import time

    print("\n" + "="*60)
    print("COMPLEXITY ANALYSIS")
    print("="*60)

    print("\nTime Complexity: O(n)")
    print("  Single pass through array")
    print("  Constant work per house")

    print("\nSpace Complexity:")
    print("  Array version: O(n)")
    print("  Optimized version: O(1)")

    # Benchmark
    print("\n" + "-"*60)
    print("Performance measurements:")
    print("-"*60)

    sizes = [100, 1000, 10000]

    for size in sizes:
        nums = list(range(size))

        # Array version
        start = time.time()
        rob(nums)
        time_array = (time.time() - start) * 1000

        # Optimized version
        start = time.time()
        rob_space_optimized(nums)
        time_opt = (time.time() - start) * 1000

        print(f"\nn = {size:5d}:")
        print(f"  Array version:     {time_array:8.4f} ms")
        print(f"  Optimized version: {time_opt:8.4f} ms")


if __name__ == "__main__":
    # Run tests
    test_rob()

    # Explain recurrence relation
    explain_recurrence()

    # Visualization examples
    print("\n" + "="*60)
    print("VISUALIZATION EXAMPLES")
    print("="*60)

    print("\nExample 1: Simple case [1,2,3,1]")
    print("-" * 60)
    visualize_rob([1, 2, 3, 1])

    print("\n" + "="*60)
    print("\nExample 2: Standard case [2,7,9,3,1]")
    print("-" * 60)
    visualize_rob([2, 7, 9, 3, 1])

    print("\n" + "="*60)
    print("\nExample 3: Decreasing values [5,4,3,2,1]")
    print("-" * 60)
    visualize_rob([5, 4, 3, 2, 1])

    # Show decision tree
    print("\n" + "="*60)
    print("DECISION TREE")
    print("="*60)
    visualize_decision_tree([2, 7, 9, 3])

    # Compare variations
    compare_variations()

    # Analyze complexity
    analyze_complexity()

    # Show interesting examples
    print("\n" + "="*60)
    print("INTERESTING EXAMPLES")
    print("="*60)

    examples = [
        [2, 1, 1, 2],           # Rob first and last
        [5, 3, 4, 11, 2],       # Big payoff in middle
        [1, 2, 3, 4, 5, 6, 7],  # All increasing
        [100, 1, 1, 100],       # Rob both ends
    ]

    for nums in examples:
        money, houses = rob_with_houses(nums)
        print(f"\nHouses: {nums}")
        print(f"Rob houses: {houses} → Money: {[nums[i] for i in houses]}")
        print(f"Total: ${money}")
