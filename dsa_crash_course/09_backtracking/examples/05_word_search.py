"""
Word Search (LeetCode #79)

Problem:
Given an m x n grid of characters board and a string word, return true if word exists
in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent
cells are horizontally or vertically neighboring. The same letter cell may not be used
more than once.

Example 1:
Input: board = [["A","B","C","E"],
                ["S","F","C","S"],
                ["A","D","E","E"]], word = "ABCCED"
Output: true

Visual:
[A][B][C] E      Path: A→B→C→C→E→D
 S [F][C] S             ↓     ↑
 A [D][E][E]            └─────┘

Example 2:
Input: board = [["A","B","C","E"],
                ["S","F","C","S"],
                ["A","D","E","E"]], word = "SEE"
Output: true

Visual:
 A  B  C  E
[S] F  C  S      Path: S→E→E
 A  D [E][E]          ↓ ↗

Example 3:
Input: board = [["A","B","C","E"],
                ["S","F","C","S"],
                ["A","D","E","E"]], word = "ABCB"
Output: false

Explanation: Cannot reuse cell [0][1] (B) after using it.

Constraints:
- m == board.length
- n = board[i].length
- 1 <= m, n <= 6
- 1 <= word.length <= 15
- board and word consists of only lowercase and uppercase English letters
"""


def exist(board, word):
    """
    DFS backtracking solution with visited tracking.

    Strategy:
    1. Find all starting positions (cells matching first letter)
    2. From each starting position, try to build the word using DFS
    3. Mark cells as visited to prevent reuse
    4. Backtrack if path doesn't work

    Key Points:
    - Explore 4 directions: up, down, left, right
    - Mark cell as visited before exploring
    - Restore cell after backtracking
    - Early termination when word is found

    Time Complexity: O(m * n * 4^L)
    - m * n: Try each cell as starting point
    - 4^L: For each position in word, try 4 directions (worst case)
    - L = len(word)

    Space Complexity: O(L)
    - Recursion depth is at most L (length of word)
    - Visited set: O(L) (max L cells on current path)

    Args:
        board: 2D grid of characters
        word: Target word to find

    Returns:
        True if word exists in grid, False otherwise
    """
    if not board or not board[0]:
        return False

    rows = len(board)
    cols = len(board[0])

    def dfs(row, col, index, visited):
        """
        DFS to find word starting from (row, col).

        Args:
            row, col: Current position
            index: Current index in word we're matching
            visited: Set of visited positions (row, col)

        Returns:
            True if we can build word from this position
        """
        # Base case: matched entire word
        if index == len(word):
            return True

        # Boundary checks
        if (row < 0 or row >= rows or
            col < 0 or col >= cols or
            (row, col) in visited):
            return False

        # Character doesn't match
        if board[row][col] != word[index]:
            return False

        # CHOOSE: Mark this cell as visited
        visited.add((row, col))

        # EXPLORE: Try all 4 directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        for dr, dc in directions:
            if dfs(row + dr, col + dc, index + 1, visited):
                return True  # Found the word!

        # UNCHOOSE: Backtrack - mark cell as unvisited
        visited.remove((row, col))

        return False

    # Try starting from each cell
    for r in range(rows):
        for c in range(cols):
            # Optimization: Only start if first letter matches
            if board[r][c] == word[0]:
                if dfs(r, c, 0, set()):
                    return True

    return False


def exist_modify_board(board, word):
    """
    Alternative: Modify board in-place instead of using visited set.

    We temporarily change the cell value to mark it as visited.
    This saves space but modifies the input.

    Time Complexity: O(m * n * 4^L)
    Space Complexity: O(L) - only recursion stack

    Note: This modifies the input board. In practice, prefer the visited set approach.
    """
    if not board or not board[0]:
        return False

    rows = len(board)
    cols = len(board[0])

    def dfs(row, col, index):
        # Base case: matched entire word
        if index == len(word):
            return True

        # Boundary checks
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return False

        # Character doesn't match or already visited
        if board[row][col] != word[index]:
            return False

        # CHOOSE: Mark as visited by changing value
        temp = board[row][col]
        board[row][col] = '#'  # Use a marker that won't appear in input

        # EXPLORE: Try all 4 directions
        found = (dfs(row + 1, col, index + 1) or
                 dfs(row - 1, col, index + 1) or
                 dfs(row, col + 1, index + 1) or
                 dfs(row, col - 1, index + 1))

        # UNCHOOSE: Restore original value
        board[row][col] = temp

        return found

    # Try starting from each cell
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if dfs(r, c, 0):
                    return True

    return False


def find_word_path(board, word):
    """
    Extension: Return the actual path if word exists.

    Returns the sequence of positions that form the word.

    Returns:
        List of (row, col) tuples representing the path, or None if not found
    """
    if not board or not board[0]:
        return None

    rows = len(board)
    cols = len(board[0])

    def dfs(row, col, index, path):
        # Found complete word
        if index == len(word):
            return path[:]

        # Boundary and validity checks
        if (row < 0 or row >= rows or
            col < 0 or col >= cols or
            (row, col) in path):
            return None

        if board[row][col] != word[index]:
            return None

        # CHOOSE
        path.append((row, col))

        # EXPLORE
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            result = dfs(row + dr, col + dc, index + 1, path)
            if result:
                return result

        # UNCHOOSE
        path.pop()

        return None

    # Try each cell as starting point
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                result = dfs(r, c, 0, [])
                if result:
                    return result

    return None


def visualize_word_search(board, word):
    """
    Visualize the search process step by step.
    """
    print(f"\nSearching for word '{word}' in board:")
    print("=" * 60)

    # Print board
    print("\nBoard:")
    for row in board:
        print("  " + " ".join(row))

    if not board or not board[0]:
        print("Empty board!")
        return False

    rows = len(board)
    cols = len(board[0])
    call_count = [0]

    def print_board_state(visited, current_pos=None):
        """Print board with visited cells marked."""
        print()
        for r in range(rows):
            row_str = "  "
            for c in range(cols):
                if (r, c) == current_pos:
                    row_str += f"[{board[r][c]}]"
                elif (r, c) in visited:
                    row_str += f" {board[r][c]}*"
                else:
                    row_str += f" {board[r][c]} "
            print(row_str)

    def dfs(row, col, index, visited, depth=0):
        call_count[0] += 1
        indent = "  " * depth

        print(f"\n{indent}Call #{call_count[0]}: pos=({row},{col}), "
              f"looking for word[{index}]='{word[index] if index < len(word) else '?'}'")

        # Base case: matched entire word
        if index == len(word):
            print(f"{indent}✓ Matched entire word!")
            return True

        # Boundary checks
        if row < 0 or row >= rows or col < 0 or col >= cols:
            print(f"{indent}✗ Out of bounds")
            return False

        if (row, col) in visited:
            print(f"{indent}✗ Already visited")
            return False

        # Character check
        if board[row][col] != word[index]:
            print(f"{indent}✗ Character mismatch: got '{board[row][col]}', "
                  f"need '{word[index]}'")
            return False

        print(f"{indent}✓ Match! '{board[row][col]}' == '{word[index]}'")

        # CHOOSE
        visited.add((row, col))
        print(f"{indent}Marked ({row},{col}) as visited")

        if depth <= 2:  # Only show board for first few levels
            print_board_state(visited, (row, col))

        # EXPLORE
        directions = [
            (0, 1, "right"),
            (1, 0, "down"),
            (0, -1, "left"),
            (-1, 0, "up")
        ]

        for dr, dc, direction in directions:
            new_row, new_col = row + dr, col + dc
            print(f"{indent}Trying {direction} to ({new_row},{new_col})")

            if dfs(new_row, new_col, index + 1, visited, depth + 1):
                return True

        # UNCHOOSE
        visited.remove((row, col))
        print(f"{indent}Backtracking from ({row},{col})")

        return False

    # Try each starting position
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                print(f"\n{'='*60}")
                print(f"Trying starting position ({r},{c})")
                print(f"{'='*60}")

                if dfs(r, c, 0, set()):
                    print(f"\n{'='*60}")
                    print(f"✓ WORD FOUND! Total calls: {call_count[0]}")
                    print(f"{'='*60}")
                    return True

    print(f"\n{'='*60}")
    print(f"✗ WORD NOT FOUND. Total calls: {call_count[0]}")
    print(f"{'='*60}")
    return False


def visualize_path(board, word):
    """
    Find and visualize the path through the board.
    """
    print(f"\nFinding path for word '{word}':")
    print("=" * 60)

    path = find_word_path(board, word)

    if not path:
        print("Word not found in board!")
        return

    print(f"\nPath found with {len(path)} steps:")
    for i, (r, c) in enumerate(path):
        print(f"  Step {i+1}: ({r},{c}) = '{board[r][c]}'")

    print("\nVisualization:")
    rows = len(board)
    cols = len(board[0])

    # Create visual board
    for r in range(rows):
        row_str = "  "
        for c in range(cols):
            if (r, c) in path:
                step = path.index((r, c)) + 1
                row_str += f"[{board[r][c]}{step}]"
            else:
                row_str += f" {board[r][c]} "
        print(row_str)

    print("\nPath sequence:", " → ".join([board[r][c] for r, c in path]))


def test_word_search():
    """Comprehensive test cases."""

    # Test case 1: Word exists (zigzag path)
    board1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    assert exist(board1, "ABCCED") == True

    # Test case 2: Word exists (simple path)
    assert exist(board1, "SEE") == True

    # Test case 3: Word doesn't exist (would require reusing cell)
    assert exist(board1, "ABCB") == False

    # Test case 4: Single cell
    assert exist([["A"]], "A") == True
    assert exist([["A"]], "B") == False

    # Test case 5: Word longer than available cells
    assert exist([["A", "B"]], "ABC") == False

    # Test case 6: All cells used
    board2 = [["A", "B"], ["C", "D"]]
    assert exist(board2, "ABDC") == True

    # Test case 7: Horizontal word
    board3 = [["A", "B", "C", "D"]]
    assert exist(board3, "ABCD") == True

    # Test case 8: Vertical word
    board4 = [["A"], ["B"], ["C"], ["D"]]
    assert exist(board4, "ABCD") == True

    # Test case 9: Word exists but tricky path
    board5 = [
        ["C", "A", "A"],
        ["A", "A", "A"],
        ["B", "C", "D"]
    ]
    assert exist(board5, "AAB") == True

    # Test case 10: First letter appears multiple times
    board6 = [["A", "A"], ["A", "A"]]
    assert exist(board6, "AAAA") == True
    assert exist(board6, "AAAAA") == False

    # Verify both implementations match
    test_boards = [board1, board2, board3, board4, board5]
    test_words = ["ABCCED", "ABDC", "ABCD", "ABCD", "AAB"]

    for board, word in zip(test_boards, test_words):
        result1 = exist([row[:] for row in board], word)  # Copy board
        result2 = exist_modify_board([row[:] for row in board], word)  # Copy board
        assert result1 == result2, f"Mismatch for {word}"

    # Test path finding
    path = find_word_path(board1, "SEE")
    assert path is not None
    assert len(path) == 3

    print("All test cases passed!")


def analyze_complexity():
    """
    Analyze and explain time complexity.
    """
    print("\n" + "="*60)
    print("COMPLEXITY ANALYSIS")
    print("="*60)

    print("\nTime Complexity: O(m * n * 4^L)")
    print("  m * n: Try each cell as starting point")
    print("  4^L: For each position, try up to 4 directions")
    print("  L: Length of word")

    print("\nWhy 4^L?")
    print("  At each step, we can go in 4 directions: ↑ ↓ ← →")
    print("  We need L steps to build the word")
    print("  Worst case: 4 * 4 * 4 * ... (L times) = 4^L")

    print("\nPractical optimizations:")
    print("  1. Early termination: Stop when word is found")
    print("  2. Character matching: Only explore matching cells")
    print("  3. Visited tracking: Prevents cycles and redundant work")
    print("  4. Pruning: Many branches terminate early")

    print("\nSpace Complexity: O(L)")
    print("  Recursion stack: L levels deep")
    print("  Visited set: At most L cells in current path")


def demonstrate_backtracking():
    """
    Demonstrate the backtracking mechanism.
    """
    print("\n" + "="*60)
    print("BACKTRACKING MECHANISM")
    print("="*60)

    print("\nKey operations:")
    print("1. CHOOSE: Mark cell as visited")
    print("2. EXPLORE: Try all 4 directions")
    print("3. UNCHOOSE: Unmark cell (backtrack)")

    print("\nExample: Searching for 'ABC'")
    print("\nBoard:")
    print("  A B")
    print("  C D")

    print("\nProcess:")
    print("1. Start at A(0,0), mark visited")
    print("2. Try right → B(0,1), mark visited")
    print("3. Try down → D(1,1), doesn't match C")
    print("4. BACKTRACK to B(0,1)")
    print("5. Try other directions from B")
    print("6. BACKTRACK to A(0,0)")
    print("7. Try down → C(1,0), mark visited")
    print("8. Success! Found 'ABC'")

    print("\nWithout backtracking:")
    print("  Once we visit B(0,1), we'd be stuck")
    print("  Backtracking lets us try alternative paths")


if __name__ == "__main__":
    # Run tests
    test_word_search()

    # Explain complexity
    analyze_complexity()

    # Demonstrate backtracking
    demonstrate_backtracking()

    # Visualization examples
    print("\n" + "="*60)
    print("VISUALIZATION EXAMPLES")
    print("="*60)

    board1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]

    print("\nExample 1: Word exists - 'SEE'")
    print("-" * 60)
    visualize_path(board1, "SEE")

    print("\n" + "-" * 60)
    print("\nExample 2: Word exists - 'ABCCED'")
    print("-" * 60)
    visualize_path(board1, "ABCCED")

    print("\n" + "-" * 60)
    print("\nExample 3: Word doesn't exist - 'ABCB'")
    print("-" * 60)
    visualize_path(board1, "ABCB")

    # Detailed search process (only for small examples)
    print("\n" + "="*60)
    print("DETAILED SEARCH PROCESS")
    print("="*60)

    small_board = [["A", "B"], ["C", "D"]]

    print("\nExample: Simple 2×2 board, searching for 'ABC'")
    print("-" * 60)
    visualize_word_search(small_board, "ABC")

    print("\n" + "-" * 60)
    print("\nExample: Searching for 'ABD' (doesn't exist)")
    print("-" * 60)
    visualize_word_search(small_board, "ABD")
