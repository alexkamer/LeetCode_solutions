"""
Longest Common Subsequence (LeetCode #1143)

Problem:
Given two strings text1 and text2, return the length of their longest common subsequence.
If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some
characters (can be none) deleted without changing the relative order of the remaining
characters.

For example, "ace" is a subsequence of "abcde".

A common subsequence of two strings is a subsequence that is common to both strings.

Example 1:
Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" and its length is 3.

Example 2:
Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.

Example 3:
Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.

Constraints:
- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English characters

KEY INSIGHT:
This is a classic 2D DP problem. At each position (i, j), we have two choices:
1. If text1[i] == text2[j]: Characters match, include both and add 1
2. If text1[i] != text2[j]: Skip one character from either string, take max
"""


def longest_common_subsequence(text1, text2):
    """
    2D Dynamic Programming solution - bottom-up approach.

    State Definition:
    dp[i][j] = length of LCS of text1[0:i] and text2[0:j]

    Recurrence Relation:
    - If text1[i-1] == text2[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1  (match, include both)
    - Else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])  (skip one, take max)

    Base Case:
    dp[0][j] = 0 (empty text1)
    dp[i][0] = 0 (empty text2)

    Example: text1="abcde", text2="ace"

    DP Table:
        ""  a  c  e
    ""   0  0  0  0
    a    0  1  1  1    (a matches a)
    b    0  1  1  1
    c    0  1  2  2    (c matches c)
    d    0  1  2  2
    e    0  1  2  3    (e matches e)

    Answer: dp[5][3] = 3 (LCS = "ace")

    Time Complexity: O(m * n)
    - Fill (m+1) × (n+1) table
    - Each cell takes O(1)

    Space Complexity: O(m * n)
    - DP table of size (m+1) × (n+1)

    Args:
        text1: First string
        text2: Second string

    Returns:
        Length of longest common subsequence
    """
    m, n = len(text1), len(text2)

    # Create DP table with (m+1) x (n+1) dimensions
    # dp[i][j] represents LCS length of text1[0:i] and text2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                # Characters match: include both
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Characters don't match: skip one, take max
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def longest_common_subsequence_space_optimized(text1, text2):
    """
    Space-optimized version using only two rows.

    Observation: We only need the previous row to compute current row.

    Time Complexity: O(m * n)
    Space Complexity: O(n) - only store two rows

    This is a significant improvement when strings are long.
    """
    m, n = len(text1), len(text2)

    # Use two arrays instead of 2D table
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])

        # Swap arrays for next iteration
        prev, curr = curr, prev

    return prev[n]


def longest_common_subsequence_with_string(text1, text2):
    """
    Extension: Return the actual LCS string, not just length.

    We need to track how we arrived at each cell to reconstruct the path.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n)

    Returns:
        Tuple of (length, lcs_string)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Build DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct the LCS string by backtracking through the table
    lcs = []
    i, j = m, n

    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            # This character is in LCS
            lcs.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            # Came from top
            i -= 1
        else:
            # Came from left
            j -= 1

    lcs.reverse()  # We built it backwards
    return dp[m][n], ''.join(lcs)


def longest_common_subsequence_recursive(text1, text2):
    """
    Recursive solution with memoization (top-down DP).

    This is more intuitive but less efficient in practice due to
    function call overhead.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n) for memo + O(m + n) for recursion stack
    """
    memo = {}

    def dp(i, j):
        """
        Returns LCS length of text1[i:] and text2[j:].
        """
        # Base case: reached end of either string
        if i == len(text1) or j == len(text2):
            return 0

        # Check memo
        if (i, j) in memo:
            return memo[(i, j)]

        # Recursive case
        if text1[i] == text2[j]:
            # Characters match
            result = 1 + dp(i + 1, j + 1)
        else:
            # Characters don't match: try skipping from either string
            result = max(dp(i + 1, j), dp(i, j + 1))

        memo[(i, j)] = result
        return result

    return dp(0, 0)


def visualize_lcs_table(text1, text2):
    """
    Visualize the DP table construction step by step.
    """
    print(f"\nBuilding LCS table for:")
    print(f"  text1 = '{text1}'")
    print(f"  text2 = '{text2}'")
    print("=" * 60)

    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Print initial table
    print("\nInitial table (all zeros):")
    print_table(dp, text1, text2)

    # Fill table with explanation
    print("\nFilling the table:")
    print("-" * 60)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            char1 = text1[i - 1]
            char2 = text2[j - 1]

            if char1 == char2:
                dp[i][j] = dp[i - 1][j - 1] + 1
                print(f"\nPosition ({i},{j}): '{char1}' == '{char2}'")
                print(f"  Match! dp[{i}][{j}] = dp[{i-1}][{j-1}] + 1 = {dp[i-1][j-1]} + 1 = {dp[i][j]}")
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                print(f"\nPosition ({i},{j}): '{char1}' != '{char2}'")
                print(f"  No match. dp[{i}][{j}] = max(dp[{i-1}][{j}], dp[{i}][{j-1}])")
                print(f"           = max({dp[i-1][j]}, {dp[i][j-1]}) = {dp[i][j]}")

    print("\n" + "=" * 60)
    print("Final table:")
    print_table(dp, text1, text2)

    print(f"\nLCS Length: {dp[m][n]}")

    # Show the LCS
    _, lcs = longest_common_subsequence_with_string(text1, text2)
    print(f"LCS String: '{lcs}'")


def print_table(dp, text1, text2):
    """
    Pretty print the DP table.
    """
    m, n = len(text1), len(text2)

    # Header
    header = "      " + "  ".join([" "] + list(text2))
    print(header)

    # Rows
    for i in range(m + 1):
        row_label = " " if i == 0 else text1[i - 1]
        row_str = f"  {row_label}  "
        row_str += "  ".join(str(dp[i][j]) for j in range(n + 1))
        print(row_str)


def visualize_backtracking(text1, text2):
    """
    Visualize how we backtrack to find the actual LCS string.
    """
    print(f"\nBacktracking to find LCS:")
    print(f"  text1 = '{text1}'")
    print(f"  text2 = '{text2}'")
    print("=" * 60)

    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Build table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    print("\nDP Table:")
    print_table(dp, text1, text2)

    # Backtrack
    print("\n" + "-" * 60)
    print("Backtracking process:")
    print("-" * 60)

    lcs = []
    i, j = m, n
    step = 0

    while i > 0 and j > 0:
        step += 1
        char1 = text1[i - 1]
        char2 = text2[j - 1]

        print(f"\nStep {step}: At dp[{i}][{j}] = {dp[i][j]}")
        print(f"  Comparing text1[{i-1}]='{char1}' and text2[{j-1}]='{char2}'")

        if char1 == char2:
            print(f"  ✓ Match! Add '{char1}' to LCS")
            lcs.append(char1)
            i -= 1
            j -= 1
            print(f"  Move diagonally to dp[{i}][{j}]")
        elif dp[i - 1][j] > dp[i][j - 1]:
            print(f"  No match. dp[{i-1}][{j}]={dp[i-1][j]} > dp[{i}][{j-1}]={dp[i][j-1]}")
            print(f"  Move up to dp[{i-1}][{j}]")
            i -= 1
        else:
            print(f"  No match. dp[{i}][{j-1}]={dp[i][j-1]} >= dp[{i-1}][{j}]={dp[i-1][j]}")
            print(f"  Move left to dp[{i}][{j-1}]")
            j -= 1

    lcs.reverse()
    print("\n" + "=" * 60)
    print(f"LCS: '{' → '.join(lcs)}' = '{''.join(lcs)}'")


def compare_approaches():
    """
    Compare different approaches in terms of performance.
    """
    import time

    text1 = "abcdefghijklmnopqrstuvwxyz" * 20  # Long string
    text2 = "acegikmoqsuwy" * 40

    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    print(f"text1 length: {len(text1)}")
    print(f"text2 length: {len(text2)}")

    approaches = [
        ("2D DP (standard)", longest_common_subsequence),
        ("Space optimized", longest_common_subsequence_space_optimized),
        ("Recursive + memo", longest_common_subsequence_recursive),
    ]

    for name, func in approaches:
        start = time.time()
        result = func(text1, text2)
        elapsed = (time.time() - start) * 1000

        print(f"\n{name:25s}: {elapsed:8.4f} ms → LCS length = {result}")


def test_lcs():
    """Comprehensive test cases."""

    # Test case 1: Standard example
    assert longest_common_subsequence("abcde", "ace") == 3

    # Test case 2: Identical strings
    assert longest_common_subsequence("abc", "abc") == 3

    # Test case 3: No common subsequence
    assert longest_common_subsequence("abc", "def") == 0

    # Test case 4: One character match
    assert longest_common_subsequence("abc", "xyz") == 0
    assert longest_common_subsequence("abc", "ayz") == 1

    # Test case 5: Complete overlap
    assert longest_common_subsequence("abc", "aebdc") == 3

    # Test case 6: Empty strings
    assert longest_common_subsequence("", "abc") == 0
    assert longest_common_subsequence("abc", "") == 0

    # Test case 7: Single characters
    assert longest_common_subsequence("a", "a") == 1
    assert longest_common_subsequence("a", "b") == 0

    # Test case 8: Different lengths
    assert longest_common_subsequence("abc", "a") == 1
    assert longest_common_subsequence("a", "abc") == 1

    # Test case 9: Multiple possible LCS
    # "abac" and "cab" → LCS could be "ab" or "ca", both length 2
    assert longest_common_subsequence("abac", "cab") == 2

    # Test case 10: Longer strings
    assert longest_common_subsequence("programming", "gaming") == 6  # "gramin"

    # Verify all implementations give same results
    test_cases = [
        ("abcde", "ace"),
        ("abc", "abc"),
        ("abc", "def"),
        ("programming", "gaming"),
    ]

    for text1, text2 in test_cases:
        r1 = longest_common_subsequence(text1, text2)
        r2 = longest_common_subsequence_space_optimized(text1, text2)
        r3 = longest_common_subsequence_recursive(text1, text2)
        length, _ = longest_common_subsequence_with_string(text1, text2)

        assert r1 == r2 == r3 == length, f"Mismatch for ({text1}, {text2})"

    # Verify LCS string is correct
    length, lcs = longest_common_subsequence_with_string("abcde", "ace")
    assert length == 3
    assert lcs == "ace"

    print("All test cases passed!")


def explain_recurrence():
    """
    Explain the recurrence relation in detail.
    """
    print("\n" + "="*60)
    print("UNDERSTANDING THE RECURRENCE RELATION")
    print("="*60)

    print("\nRecurrence Relation:")
    print("  If text1[i-1] == text2[j-1]:")
    print("    dp[i][j] = dp[i-1][j-1] + 1")
    print("  Else:")
    print("    dp[i][j] = max(dp[i-1][j], dp[i][j-1])")

    print("\nIntuition:")
    print("\n1. When characters match (text1[i-1] == text2[j-1]):")
    print("   - This character is part of the LCS")
    print("   - Include it and add 1 to the LCS of previous positions")
    print("   - Example: LCS('ab', 'ab') = LCS('a', 'a') + 1")

    print("\n2. When characters don't match:")
    print("   - This character won't be in LCS together")
    print("   - Try two options:")
    print("     a) Skip character from text1: dp[i-1][j]")
    print("     b) Skip character from text2: dp[i][j-1]")
    print("   - Take the maximum")

    print("\nExample: text1='abc', text2='ac'")
    print("  At position (2,2): comparing 'b' and 'c'")
    print("  They don't match, so:")
    print("    Option 1: Skip 'b', use LCS('a', 'ac') = 1")
    print("    Option 2: Skip 'c', use LCS('ab', 'a') = 1")
    print("    Result: max(1, 1) = 1")


if __name__ == "__main__":
    # Run tests
    test_lcs()

    # Explain recurrence relation
    explain_recurrence()

    # Visualization examples
    print("\n" + "="*60)
    print("VISUALIZATION EXAMPLES")
    print("="*60)

    print("\nExample 1: Simple case")
    print("-" * 60)
    visualize_lcs_table("abc", "ac")

    print("\n" + "="*60)
    print("\nExample 2: Standard case")
    print("-" * 60)
    visualize_lcs_table("abcde", "ace")

    print("\n" + "="*60)
    print("\nExample 3: No common subsequence")
    print("-" * 60)
    visualize_lcs_table("abc", "def")

    # Show backtracking
    print("\n" + "="*60)
    print("BACKTRACKING EXAMPLES")
    print("="*60)

    print("\nExample 1: Backtracking for 'abcde' and 'ace'")
    print("-" * 60)
    visualize_backtracking("abcde", "ace")

    print("\n" + "="*60)
    print("\nExample 2: Backtracking for 'programming' and 'gaming'")
    print("-" * 60)
    visualize_backtracking("programming", "gaming")

    # Compare approaches
    compare_approaches()

    # Show some interesting examples
    print("\n" + "="*60)
    print("INTERESTING EXAMPLES")
    print("="*60)

    examples = [
        ("AGGTAB", "GXTXAYB"),
        ("programming", "gaming"),
        ("ABCDGH", "AEDFHR"),
    ]

    for text1, text2 in examples:
        length, lcs = longest_common_subsequence_with_string(text1, text2)
        print(f"\ntext1: '{text1}'")
        print(f"text2: '{text2}'")
        print(f"LCS: '{lcs}' (length={length})")
