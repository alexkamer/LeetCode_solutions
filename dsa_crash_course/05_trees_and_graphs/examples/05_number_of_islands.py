"""
Number of Islands (LeetCode #200)

Problem:
Given an m x n 2D binary grid which represents a map of '1's (land) and '0's
(water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands
horizontally or vertically. You may assume all four edges of the grid are
surrounded by water.

Example 1:
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Example 2:
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 300
- grid[i][j] is '0' or '1'
"""


def num_islands_dfs_recursive(grid):
    """
    DFS recursive approach - most intuitive solution.

    Approach:
    1. Iterate through each cell in grid
    2. When we find a '1', we've found a new island
    3. Use DFS to mark all connected land cells as visited
    4. Count how many times we start a new DFS (= number of islands)

    The key insight: treat the grid as an implicit graph where
    each land cell is a node, and edges connect adjacent land cells.

    Time Complexity: O(m * n) - visit each cell at most twice
                     (once in main loop, once in DFS)
    Space Complexity: O(m * n) - worst case: entire grid is one island,
                      recursion depth could be m * n

    Args:
        grid: 2D list of strings ('0' or '1')

    Returns:
        Integer count of islands
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def dfs(r, c):
        """Mark all cells in current island as visited."""
        # Base cases: out of bounds, water, or already visited
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or grid[r][c] == '0'):
            return

        visited.add((r, c))

        # Explore all 4 directions (up, down, left, right)
        dfs(r + 1, c)  # down
        dfs(r - 1, c)  # up
        dfs(r, c + 1)  # right
        dfs(r, c - 1)  # left

    # Check every cell
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                count += 1

    return count


def num_islands_dfs_iterative(grid):
    """
    DFS iterative approach using explicit stack.

    Same logic as recursive DFS but using a stack to avoid
    potential stack overflow on very large grids.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n) - stack size

    Args:
        grid: 2D list of strings ('0' or '1')

    Returns:
        Integer count of islands
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def dfs_iterative(start_r, start_c):
        """Iteratively explore island using stack."""
        stack = [(start_r, start_c)]

        while stack:
            r, c = stack.pop()

            if (r < 0 or r >= rows or c < 0 or c >= cols or
                (r, c) in visited or grid[r][c] == '0'):
                continue

            visited.add((r, c))

            # Add all 4 neighbors to stack
            stack.append((r + 1, c))
            stack.append((r - 1, c))
            stack.append((r, c + 1))
            stack.append((r, c - 1))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs_iterative(r, c)
                count += 1

    return count


def num_islands_bfs(grid):
    """
    BFS approach using queue.

    BFS explores island level by level, visiting all immediate
    neighbors before moving to next layer.

    For this problem, DFS vs BFS doesn't matter for correctness,
    but BFS might be preferred if we needed shortest path info.

    Time Complexity: O(m * n)
    Space Complexity: O(min(m, n)) - queue size in worst case

    Args:
        grid: 2D list of strings ('0' or '1')

    Returns:
        Integer count of islands
    """
    if not grid or not grid[0]:
        return 0

    from collections import deque

    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def bfs(start_r, start_c):
        """Explore island using BFS."""
        queue = deque([(start_r, start_c)])
        visited.add((start_r, start_c))

        while queue:
            r, c = queue.popleft()

            # Check all 4 directions
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if (0 <= nr < rows and 0 <= nc < cols and
                    (nr, nc) not in visited and grid[nr][nc] == '1'):
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                bfs(r, c)
                count += 1

    return count


def num_islands_modify_input(grid):
    """
    Space-optimized approach that modifies input.

    Instead of using visited set, mark visited cells by changing
    '1' to '0' in the original grid.

    This saves O(m * n) space but modifies the input!
    Always ask interviewer if modifying input is acceptable.

    Time Complexity: O(m * n)
    Space Complexity: O(1) - only recursion stack (or O(m*n) for recursion)

    Args:
        grid: 2D list of strings ('0' or '1')

    Returns:
        Integer count of islands
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        """Mark all cells in current island as '0'."""
        if (r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0'):
            return

        grid[r][c] = '0'  # Mark as visited by changing to water

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1

    return count


def num_islands_with_size(grid):
    """
    Variation: return list of island sizes.

    Useful extension that shows how to track additional info
    during traversal.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n)

    Args:
        grid: 2D list of strings ('0' or '1')

    Returns:
        List of integers representing size of each island
    """
    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])
    visited = set()
    island_sizes = []

    def dfs(r, c):
        """Return size of current island."""
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or grid[r][c] == '0'):
            return 0

        visited.add((r, c))

        size = 1
        size += dfs(r + 1, c)
        size += dfs(r - 1, c)
        size += dfs(r, c + 1)
        size += dfs(r, c - 1)

        return size

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                island_size = dfs(r, c)
                island_sizes.append(island_size)

    return island_sizes


def visualize_grid(grid):
    """Print grid in readable format."""
    print("Grid:")
    for row in grid:
        print(" ".join(row))


def test_num_islands():
    """Test cases covering various scenarios."""

    # Test case 1: Single island
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    assert num_islands_dfs_recursive([row[:] for row in grid1]) == 1
    assert num_islands_dfs_iterative([row[:] for row in grid1]) == 1
    assert num_islands_bfs([row[:] for row in grid1]) == 1

    # Test case 2: Multiple islands
    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    assert num_islands_dfs_recursive([row[:] for row in grid2]) == 3
    assert num_islands_dfs_iterative([row[:] for row in grid2]) == 3
    assert num_islands_bfs([row[:] for row in grid2]) == 3

    # Test case 3: No islands
    grid3 = [
        ["0", "0", "0"],
        ["0", "0", "0"],
        ["0", "0", "0"]
    ]
    assert num_islands_dfs_recursive([row[:] for row in grid3]) == 0
    assert num_islands_dfs_iterative([row[:] for row in grid3]) == 0
    assert num_islands_bfs([row[:] for row in grid3]) == 0

    # Test case 4: All land (one big island)
    grid4 = [
        ["1", "1", "1"],
        ["1", "1", "1"],
        ["1", "1", "1"]
    ]
    assert num_islands_dfs_recursive([row[:] for row in grid4]) == 1
    assert num_islands_dfs_iterative([row[:] for row in grid4]) == 1
    assert num_islands_bfs([row[:] for row in grid4]) == 1

    # Test case 5: Each cell is separate island
    grid5 = [
        ["1", "0", "1"],
        ["0", "1", "0"],
        ["1", "0", "1"]
    ]
    assert num_islands_dfs_recursive([row[:] for row in grid5]) == 5
    assert num_islands_dfs_iterative([row[:] for row in grid5]) == 5
    assert num_islands_bfs([row[:] for row in grid5]) == 5

    # Test case 6: Single cell
    grid6 = [["1"]]
    assert num_islands_dfs_recursive([row[:] for row in grid6]) == 1

    grid7 = [["0"]]
    assert num_islands_dfs_recursive([row[:] for row in grid7]) == 0

    # Test case 7: Test island sizes
    island_sizes = num_islands_with_size([row[:] for row in grid2])
    assert sorted(island_sizes) == [1, 2, 4]

    print("All test cases passed!")


if __name__ == "__main__":
    test_num_islands()

    # Example usage with visualization
    print("\nExample 1: Single Large Island")
    print("=" * 50)

    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]

    visualize_grid(grid1)
    print(f"Number of islands: {num_islands_dfs_recursive([row[:] for row in grid1])}")

    print("\n" + "=" * 50)
    print("Example 2: Multiple Islands")
    print("=" * 50)

    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]

    visualize_grid(grid2)
    print(f"Number of islands: {num_islands_dfs_recursive([row[:] for row in grid2])}")

    island_sizes = num_islands_with_size([row[:] for row in grid2])
    print(f"Island sizes: {sorted(island_sizes)}")

    print("\n" + "=" * 50)
    print("Example 3: Complex Pattern")
    print("=" * 50)

    grid3 = [
        ["1", "0", "1", "0", "1"],
        ["0", "1", "0", "1", "0"],
        ["1", "0", "1", "0", "1"],
        ["0", "1", "0", "1", "0"]
    ]

    visualize_grid(grid3)
    print(f"Number of islands: {num_islands_dfs_recursive([row[:] for row in grid3])}")
    print("(Each '1' is a separate island)")

    print("\n" + "=" * 50)
    print("Approach Comparison:")
    print("=" * 50)
    print("1. DFS Recursive: Clean, but may stack overflow on huge grids")
    print("2. DFS Iterative: Avoids stack overflow, uses explicit stack")
    print("3. BFS: Good for level-by-level processing")
    print("4. Modify Input: O(1) extra space, but changes input")
    print("\nAll have O(m*n) time complexity!")
