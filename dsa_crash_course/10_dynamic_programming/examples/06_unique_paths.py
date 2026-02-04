"""
Unique Paths (LeetCode #62)

Problem:
There is a robot on an m x n grid. The robot is initially located at the top-left
corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner
(i.e., grid[m-1][n-1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the
robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to 2 * 10^9.

Example 1:
Input: m = 3, n = 7
Output: 28

Visual (3×7 grid):
Start → → → → → → Goal
  ↓                 ↓
  ↓                 ↓

Example 2:
Input: m = 3, n = 2
Output: 3
Explanation: From the top-left corner, there are a total of 3 ways to reach
the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Right -> Down
3. Down -> Down -> Right

Example 3:
Input: m = 3, n = 3
Output: 6

Constraints:
- 1 <= m, n <= 100

KEY INSIGHT:
To reach any cell (i, j), you must come from either:
- Cell above: (i-1, j)
- Cell to the left: (i, j-1)

So: paths to (i,j) = paths to (i-1,j) + paths to (i,j-1)

This is a classic 2D DP problem!
"""


def unique_paths(m, n):
    """
    2D Dynamic Programming solution.

    State Definition:
    dp[i][j] = number of unique paths to reach cell (i, j)

    Recurrence Relation:
    dp[i][j] = dp[i-1][j] + dp[i][j-1]
    (paths from above + paths from left)

    Base Case:
    dp[0][j] = 1 for all j (only one way: go right)
    dp[i][0] = 1 for all i (only one way: go down)

    Example: m=3, n=3

        0   1   2
      ┌───┬───┬───┐
    0 │ 1 │ 1 │ 1 │
      ├───┼───┼───┤
    1 │ 1 │ 2 │ 3 │
      ├───┼───┼───┤
    2 │ 1 │ 3 │ 6 │
      └───┴───┴───┘

    dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2
    dp[1][2] = dp[0][2] + dp[1][1] = 1 + 2 = 3
    dp[2][2] = dp[1][2] + dp[2][1] = 3 + 3 = 6

    Time Complexity: O(m * n)
    - Fill entire m×n table
    - Each cell takes O(1)

    Space Complexity: O(m * n)
    - DP table of size m×n

    Args:
        m: Number of rows
        n: Number of columns

    Returns:
        Number of unique paths from (0,0) to (m-1,n-1)
    """
    # Create dp table
    dp = [[0] * n for _ in range(m)]

    # Base case: first row (can only go right)
    for j in range(n):
        dp[0][j] = 1

    # Base case: first column (can only go down)
    for i in range(m):
        dp[i][0] = 1

    # Fill the rest of the table
    for i in range(1, m):
        for j in range(1, n):
            # Number of ways = ways from above + ways from left
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp[m - 1][n - 1]


def unique_paths_space_optimized(m, n):
    """
    Space-optimized solution using only one row.

    Observation: We only need the previous row to compute current row.
    Actually, we can do it with just one array!

    Key insight: Process left to right, updating in place.
    - dp[j] initially contains value from previous row (from above)
    - dp[j-1] contains value from current row (from left)

    Time Complexity: O(m * n)
    Space Complexity: O(n) - single array

    This is the preferred solution for interviews.
    """
    # Single array representing current row
    dp = [1] * n  # Initialize with 1s (base case: first row)

    # Process each row
    for i in range(1, m):
        for j in range(1, n):
            # dp[j] currently has value from previous row (above)
            # dp[j-1] has value from current row (left)
            dp[j] = dp[j] + dp[j - 1]

    return dp[n - 1]


def unique_paths_math(m, n):
    """
    Mathematical solution using combinatorics.

    Insight: To reach (m-1, n-1) from (0, 0), we need:
    - (m-1) down moves
    - (n-1) right moves
    - Total: (m-1) + (n-1) = m+n-2 moves

    Problem becomes: Choose (m-1) positions for down moves out of (m+n-2) total moves.
    Answer: C(m+n-2, m-1) = (m+n-2)! / ((m-1)! * (n-1)!)

    Example: m=3, n=3
    - Need 2 down moves and 2 right moves
    - Total 4 moves, choose 2 positions for down: C(4,2) = 6

    Time Complexity: O(min(m, n))
    - Computing combinations

    Space Complexity: O(1)

    This is the most efficient solution!
    """
    # Need (m-1) down moves and (n-1) right moves
    # Total moves: m + n - 2
    # Choose (m-1) positions: C(m+n-2, m-1)

    # Use smaller value for efficiency
    if m < n:
        m, n = n, m

    # Calculate C(m+n-2, n-1)
    result = 1
    for i in range(1, n):
        result = result * (m + n - 1 - i) // i

    return result


def unique_paths_recursive(m, n):
    """
    Recursive solution with memoization (top-down DP).

    More intuitive but less efficient due to recursion overhead.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n) for memo + O(m + n) for recursion
    """
    memo = {}

    def dp(i, j):
        """
        Returns number of unique paths from (i, j) to (m-1, n-1).
        """
        # Base case: reached destination
        if i == m - 1 and j == n - 1:
            return 1

        # Base case: out of bounds
        if i >= m or j >= n:
            return 0

        # Check memo
        if (i, j) in memo:
            return memo[(i, j)]

        # Two choices: go right or go down
        result = dp(i + 1, j) + dp(i, j + 1)

        memo[(i, j)] = result
        return result

    return dp(0, 0)


def unique_paths_with_obstacles(grid):
    """
    Extension: Unique Paths II (LeetCode #63)
    Grid contains obstacles (marked as 1).

    Args:
        grid: 2D array where grid[i][j] = 1 means obstacle

    Returns:
        Number of unique paths avoiding obstacles
    """
    if not grid or not grid[0] or grid[0][0] == 1:
        return 0

    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]

    # Base case: start position
    dp[0][0] = 1

    # Fill first row
    for j in range(1, n):
        if grid[0][j] == 0:
            dp[0][j] = dp[0][j - 1]
        else:
            dp[0][j] = 0  # Obstacle blocks all paths

    # Fill first column
    for i in range(1, m):
        if grid[i][0] == 0:
            dp[i][0] = dp[i - 1][0]
        else:
            dp[i][0] = 0

    # Fill rest of table
    for i in range(1, m):
        for j in range(1, n):
            if grid[i][j] == 1:
                dp[i][j] = 0  # Obstacle
            else:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp[m - 1][n - 1]


def visualize_unique_paths(m, n):
    """
    Visualize the DP table construction.
    """
    print(f"\nFinding unique paths for {m}×{n} grid")
    print("=" * 60)

    dp = [[0] * n for _ in range(m)]

    # Initialize first row and column
    for j in range(n):
        dp[0][j] = 1
    for i in range(m):
        dp[i][0] = 1

    print("\nAfter initialization:")
    print_grid(dp)

    # Fill table with explanation
    print("\nFilling the table:")
    print("-" * 60)

    for i in range(1, m):
        for j in range(1, n):
            from_above = dp[i - 1][j]
            from_left = dp[i][j - 1]
            dp[i][j] = from_above + from_left

            print(f"\nCell ({i},{j}):")
            print(f"  Paths from above ({i-1},{j}): {from_above}")
            print(f"  Paths from left ({i},{j-1}): {from_left}")
            print(f"  Total paths: {from_above} + {from_left} = {dp[i][j]}")

    print("\n" + "=" * 60)
    print("Final DP table:")
    print_grid(dp)

    print(f"\nTotal unique paths: {dp[m-1][n-1]}")


def print_grid(grid):
    """
    Pretty print a grid with proper alignment.
    """
    m, n = len(grid), len(grid[0])

    # Find max width for alignment
    max_width = max(len(str(grid[i][j])) for i in range(m) for j in range(n))

    # Print header
    header = "     " + "  ".join(f"{j:>{max_width}}" for j in range(n))
    print(header)

    # Print separator
    sep = "   ┌" + "┬".join("─" * (max_width + 2) for _ in range(n)) + "┐"
    print(sep)

    # Print rows
    for i in range(m):
        row_str = f" {i} │"
        for j in range(n):
            row_str += f" {grid[i][j]:>{max_width}} │"
        print(row_str)

        if i < m - 1:
            sep = "   ├" + "┼".join("─" * (max_width + 2) for _ in range(n)) + "┤"
            print(sep)

    # Print bottom
    sep = "   └" + "┴".join("─" * (max_width + 2) for _ in range(n)) + "┘"
    print(sep)


def visualize_all_paths(m, n):
    """
    Show some example paths for small grids.
    """
    if m > 4 or n > 4:
        print("Grid too large to show all paths")
        return

    print(f"\nShowing all unique paths for {m}×{n} grid:")
    print("=" * 60)

    paths = []

    def find_paths(i, j, path):
        """
        Recursively find all paths.
        """
        # Add current position
        path = path + [(i, j)]

        # Reached destination
        if i == m - 1 and j == n - 1:
            paths.append(path)
            return

        # Try going right
        if j < n - 1:
            find_paths(i, j + 1, path)

        # Try going down
        if i < m - 1:
            find_paths(i + 1, j, path)

    find_paths(0, 0, [])

    # Display each path
    for idx, path in enumerate(paths, 1):
        print(f"\nPath {idx}:")
        moves = []
        for i in range(len(path) - 1):
            if path[i + 1][0] > path[i][0]:
                moves.append("Down")
            else:
                moves.append("Right")
        print(f"  Route: {' → '.join(moves)}")
        print(f"  Cells: {' → '.join(f'({i},{j})' for i, j in path)}")

    print(f"\nTotal: {len(paths)} unique paths")


def test_unique_paths():
    """Comprehensive test cases."""

    # Test case 1: Standard examples
    assert unique_paths(3, 7) == 28
    assert unique_paths(3, 2) == 3
    assert unique_paths(3, 3) == 6

    # Test case 2: Single row or column
    assert unique_paths(1, 5) == 1  # Only one way: right
    assert unique_paths(5, 1) == 1  # Only one way: down

    # Test case 3: Square grids
    assert unique_paths(2, 2) == 2
    assert unique_paths(4, 4) == 20
    assert unique_paths(5, 5) == 70

    # Test case 4: Rectangular grids
    assert unique_paths(2, 3) == 3
    assert unique_paths(3, 4) == 10

    # Test case 5: Single cell
    assert unique_paths(1, 1) == 1

    # Verify all implementations give same results
    test_cases = [(3, 7), (3, 2), (3, 3), (4, 4), (5, 5)]

    for m, n in test_cases:
        r1 = unique_paths(m, n)
        r2 = unique_paths_space_optimized(m, n)
        r3 = unique_paths_math(m, n)
        r4 = unique_paths_recursive(m, n)

        assert r1 == r2 == r3 == r4, f"Mismatch for ({m}, {n})"

    # Test with obstacles
    grid1 = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    assert unique_paths_with_obstacles(grid1) == 2

    grid2 = [
        [0, 1],
        [0, 0]
    ]
    assert unique_paths_with_obstacles(grid2) == 1

    print("All test cases passed!")


def explain_recurrence():
    """
    Explain the recurrence relation in detail.
    """
    print("\n" + "="*60)
    print("UNDERSTANDING THE RECURRENCE RELATION")
    print("="*60)

    print("\nKey Insight:")
    print("  To reach any cell (i, j), you must come from either:")
    print("    1. The cell above: (i-1, j)")
    print("    2. The cell to the left: (i, j-1)")

    print("\nRecurrence Relation:")
    print("  dp[i][j] = dp[i-1][j] + dp[i][j-1]")

    print("\nWhy?")
    print("  - All paths to (i,j) must pass through either (i-1,j) or (i,j-1)")
    print("  - These are mutually exclusive (can't come from both)")
    print("  - So we add the number of paths from each")

    print("\nExample: 3×3 grid, finding dp[2][2]")
    print("\n     0   1   2")
    print("   ┌───┬───┬───┐")
    print(" 0 │ 1 │ 1 │ 1 │")
    print("   ├───┼───┼───┤")
    print(" 1 │ 1 │ 2 │ 3 │← dp[1][2] = 3")
    print("   ├───┼───┼───┤")
    print(" 2 │ 1 │ 3 │ ? │")
    print("   └───┴───┴───┘")
    print("            ↑")
    print("       dp[2][1] = 3")

    print("\ndp[2][2] = dp[1][2] + dp[2][1] = 3 + 3 = 6")


def compare_approaches():
    """
    Compare different approaches.
    """
    import time

    print("\n" + "="*60)
    print("COMPARING APPROACHES")
    print("="*60)

    test_cases = [(10, 10), (15, 15), (20, 20)]

    for m, n in test_cases:
        print(f"\nGrid size: {m}×{n}")
        print("-" * 40)

        # 2D DP
        start = time.time()
        r1 = unique_paths(m, n)
        t1 = (time.time() - start) * 1000

        # Space optimized
        start = time.time()
        r2 = unique_paths_space_optimized(m, n)
        t2 = (time.time() - start) * 1000

        # Mathematical
        start = time.time()
        r3 = unique_paths_math(m, n)
        t3 = (time.time() - start) * 1000

        print(f"  2D DP:           {t1:8.4f} ms → {r1:,} paths")
        print(f"  Space optimized: {t2:8.4f} ms → {r2:,} paths")
        print(f"  Mathematical:    {t3:8.4f} ms → {r3:,} paths")


def analyze_growth():
    """
    Show how the number of paths grows with grid size.
    """
    print("\n" + "="*60)
    print("PATH COUNT GROWTH")
    print("="*60)

    print("\nSquare grids (n×n):")
    print("-" * 40)
    print(f"{'Size':>6} | {'Paths':>15}")
    print("-" * 40)

    for n in range(1, 11):
        paths = unique_paths(n, n)
        print(f"{n:>6} | {paths:>15,}")

    print("\nObservation: Exponential growth!")
    print("This is because we're essentially choosing (n-1) moves")
    print("from (2n-2) total moves → combinations grow exponentially")


if __name__ == "__main__":
    # Run tests
    test_unique_paths()

    # Explain recurrence
    explain_recurrence()

    # Visualization examples
    print("\n" + "="*60)
    print("VISUALIZATION EXAMPLES")
    print("="*60)

    print("\nExample 1: Small 3×3 grid")
    print("-" * 60)
    visualize_unique_paths(3, 3)

    print("\n" + "="*60)
    print("\nExample 2: All paths in 3×2 grid")
    print("-" * 60)
    visualize_all_paths(3, 2)

    print("\n" + "="*60)
    print("\nExample 3: 4×4 grid")
    print("-" * 60)
    visualize_unique_paths(4, 4)

    # Compare approaches
    compare_approaches()

    # Show growth pattern
    analyze_growth()

    # Demonstrate with obstacles
    print("\n" + "="*60)
    print("WITH OBSTACLES (Unique Paths II)")
    print("="*60)

    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]

    print("\nGrid (1 = obstacle):")
    for row in grid:
        print("  " + " ".join(str(x) for x in row))

    result = unique_paths_with_obstacles(grid)
    print(f"\nUnique paths avoiding obstacles: {result}")

    print("\nExplanation:")
    print("  Without obstacle: 6 paths")
    print("  With obstacle at (1,1): 2 paths")
    print("  The obstacle blocks 4 possible paths")
