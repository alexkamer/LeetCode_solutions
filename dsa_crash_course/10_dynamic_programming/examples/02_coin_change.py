"""
Coin Change (LeetCode #322)

Problem:
You are given an integer array 'coins' representing coins of different
denominations and an integer 'amount' representing a total amount of money.

Return the fewest number of coins that you need to make up that amount.
If that amount of money cannot be made up by any combination of the coins,
return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Example 2:
Input: coins = [2], amount = 3
Output: -1

Example 3:
Input: coins = [1], amount = 0
Output: 0

Constraints:
- 1 <= coins.length <= 12
- 1 <= coins[i] <= 2^31 - 1
- 0 <= amount <= 10^4
"""


def coin_change_recursive(coins, amount):
    """
    Naive recursive approach - explores all possibilities.

    Intuition:
    For each amount, try using each coin and recursively solve for
    the remaining amount. Take the minimum across all choices.

    Problem: Massive overlapping subproblems.
    - Making amount 11 with [1,2,5] will compute amount 10 many times
    - Exponential time complexity

    Time Complexity: O(amount^coins) - exponential
    Space Complexity: O(amount) - recursion depth

    Args:
        coins: List of coin denominations
        amount: Target amount

    Returns:
        Minimum number of coins, or -1 if impossible
    """
    # Base case: amount exactly reached
    if amount == 0:
        return 0

    # Base case: negative amount (invalid)
    if amount < 0:
        return -1

    min_coins = float('inf')

    # Try using each coin
    for coin in coins:
        result = coin_change_recursive(coins, amount - coin)
        # If this path is valid, update minimum
        if result != -1:
            min_coins = min(min_coins, result + 1)

    # Return -1 if no valid combination found
    return min_coins if min_coins != float('inf') else -1


def coin_change_memoization(coins, amount, memo=None):
    """
    Top-down DP with memoization.

    Approach:
    Same recursive logic, but cache results for each amount.
    Key insight: The minimum coins for amount k is always the same,
    regardless of how we reached amount k.

    Time Complexity: O(amount × coins) - each amount computed once
    Space Complexity: O(amount) - memo + recursion stack

    Args:
        coins: List of coin denominations
        amount: Target amount
        memo: Dictionary caching results

    Returns:
        Minimum number of coins, or -1 if impossible
    """
    # Initialize memo
    if memo is None:
        memo = {}

    # Base cases
    if amount == 0:
        return 0
    if amount < 0:
        return -1

    # Check memo
    if amount in memo:
        return memo[amount]

    min_coins = float('inf')

    # Try each coin
    for coin in coins:
        result = coin_change_memoization(coins, amount - coin, memo)
        if result != -1:
            min_coins = min(min_coins, result + 1)

    # Store and return result
    memo[amount] = min_coins if min_coins != float('inf') else -1
    return memo[amount]


def coin_change_tabulation(coins, amount):
    """
    Bottom-up DP with tabulation - optimal solution.

    Approach:
    Build a table where dp[i] = minimum coins needed to make amount i.
    - Start with dp[0] = 0 (0 coins for amount 0)
    - For each amount from 1 to target:
      - Try using each coin
      - Take minimum across all valid choices

    State Definition:
    dp[i] = minimum number of coins to make amount i

    Recurrence Relation:
    dp[i] = min(dp[i - coin] + 1) for all coins where coin <= i

    Why bottom-up is better here:
    - No recursion overhead
    - Sequential memory access
    - Easier to understand the table

    Time Complexity: O(amount × coins)
    - Outer loop: amount iterations
    - Inner loop: coins iterations
    - Total: amount × coins

    Space Complexity: O(amount) - dp array

    Args:
        coins: List of coin denominations
        amount: Target amount

    Returns:
        Minimum number of coins, or -1 if impossible
    """
    # Initialize DP table with impossible values
    # dp[i] = min coins needed to make amount i
    dp = [float('inf')] * (amount + 1)

    # Base case: 0 coins needed for amount 0
    dp[0] = 0

    # Build table for each amount
    for i in range(1, amount + 1):
        # Try using each coin
        for coin in coins:
            # Can only use coin if it doesn't exceed current amount
            if coin <= i:
                # Update if using this coin gives better result
                dp[i] = min(dp[i], dp[i - coin] + 1)

    # Return result (or -1 if impossible)
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_with_path(coins, amount):
    """
    Modified version that also returns which coins to use.

    Approach:
    Same as tabulation, but also track which coin was used
    for each amount. Then backtrack to reconstruct the solution.

    Returns:
        Tuple of (min_coins, coin_list) or (-1, [])
    """
    dp = [float('inf')] * (amount + 1)
    parent = [-1] * (amount + 1)  # Track which coin was used
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                parent[i] = coin  # Remember which coin we used

    if dp[amount] == float('inf'):
        return -1, []

    # Reconstruct path
    path = []
    curr = amount
    while curr > 0:
        coin_used = parent[curr]
        path.append(coin_used)
        curr -= coin_used

    return dp[amount], path


def visualize_dp_table(coins, amount):
    """
    Visualize how the DP table is built.
    Shows the minimum coins needed for each amount from 0 to target.
    """
    print(f"Building DP table for coins={coins}, amount={amount}")
    print("=" * 60)

    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    print(f"dp[0] = 0 (base case: 0 coins for amount 0)\n")

    for i in range(1, amount + 1):
        options = []
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                coins_needed = dp[i - coin] + 1
                options.append((coin, dp[i - coin], coins_needed))
                dp[i] = min(dp[i], coins_needed)

        if options:
            print(f"dp[{i}]:")
            for coin, prev, total in options:
                marker = "✓" if total == dp[i] else " "
                print(f"  {marker} Use coin {coin}: dp[{i-coin}] + 1 = {prev} + 1 = {total}")
            print(f"  → dp[{i}] = {dp[i]}\n")
        else:
            print(f"dp[{i}] = impossible (no valid coins)\n")

    result = dp[amount] if dp[amount] != float('inf') else -1
    print(f"Final answer: {result} coins")

    if result != -1:
        _, path = coin_change_with_path(coins, amount)
        print(f"Coins used: {' + '.join(map(str, path))} = {amount}")


def test_coin_change():
    """Test cases covering various scenarios."""

    # Test case 1: Standard case
    assert coin_change_tabulation([1, 2, 5], 11) == 3
    result, path = coin_change_with_path([1, 2, 5], 11)
    assert result == 3
    assert sum(path) == 11

    # Test case 2: Impossible
    assert coin_change_tabulation([2], 3) == -1

    # Test case 3: Zero amount
    assert coin_change_tabulation([1], 0) == 0

    # Test case 4: Single coin
    assert coin_change_tabulation([1], 5) == 5

    # Test case 5: Large coins
    assert coin_change_tabulation([1, 3, 4], 6) == 2  # 3+3, not 4+1+1

    # Test case 6: Greedy fails
    # Greedy would choose 4+1+1=3 coins, but optimal is 3+3=2 coins
    assert coin_change_tabulation([1, 3, 4], 6) == 2

    # Test case 7: Multiple same-value coins
    assert coin_change_tabulation([1, 5, 10, 25], 41) == 4  # 25+10+5+1

    # Test all approaches match
    test_cases = [
        ([1, 2, 5], 11),
        ([2], 3),
        ([1], 0),
        ([1, 3, 4], 6),
    ]

    for coins, amount in test_cases:
        memo = coin_change_memoization(coins, amount)
        tab = coin_change_tabulation(coins, amount)
        assert memo == tab, f"Mismatch for coins={coins}, amount={amount}"

    print("All test cases passed!")


def demonstrate_greedy_failure():
    """
    Demonstrate why greedy approach doesn't work for coin change.
    """
    coins = [1, 3, 4]
    amount = 6

    print("Why Greedy Fails:")
    print("=" * 60)
    print(f"Coins: {coins}, Amount: {amount}\n")

    print("Greedy approach (always take largest coin):")
    remaining = amount
    greedy_coins = []
    for coin in sorted(coins, reverse=True):
        while remaining >= coin:
            greedy_coins.append(coin)
            remaining -= coin
    print(f"  Uses: {' + '.join(map(str, greedy_coins))} = {len(greedy_coins)} coins")

    print("\nOptimal DP approach:")
    min_coins, optimal_path = coin_change_with_path(coins, amount)
    print(f"  Uses: {' + '.join(map(str, optimal_path))} = {min_coins} coins")

    print(f"\nDP saves {len(greedy_coins) - min_coins} coin(s)!")


if __name__ == "__main__":
    # Run tests
    test_coin_change()
    print()

    # Visualize DP table
    visualize_dp_table([1, 2, 5], 11)
    print()

    # Demonstrate greedy failure
    demonstrate_greedy_failure()
    print()

    # Example usage
    coins = [1, 5, 10, 25]
    amount = 41
    min_coins, path = coin_change_with_path(coins, amount)
    print(f"Example: coins = {coins}, amount = {amount}")
    print(f"Minimum coins: {min_coins}")
    print(f"Coins used: {' + '.join(map(str, sorted(path, reverse=True)))} = {amount}")
