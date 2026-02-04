"""
N-Queens (LeetCode #51)

Problem:
The n-queens puzzle is the problem of placing n queens on an n×n chessboard such that
no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. You may
return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement,
where 'Q' and '.' both indicate a queen and an empty space, respectively.

Example 1:
Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
Explanation: There exist two distinct solutions to the 4-queens puzzle as shown.

Example 2:
Input: n = 1
Output: [["Q"]]

Constraints:
- 1 <= n <= 9

VISUAL EXAMPLE (n=4):
Solution 1:        Solution 2:
. Q . .            . . Q .
. . . Q            Q . . .
Q . . .            . . . Q
. . Q .            . Q . .

ATTACK PATTERNS:
Queens attack:
1. Horizontally (same row)
2. Vertically (same column)
3. Diagonally (two diagonal directions)

KEY INSIGHT:
- Place one queen per row (ensures no row conflicts)
- Track columns and diagonals to prevent conflicts
- Diagonals can be identified by:
  - Main diagonal: row - col (constant)
  - Anti-diagonal: row + col (constant)
"""


def solve_n_queens(n):
    """
    Classic backtracking solution with set-based conflict tracking.

    Strategy:
    1. Place queens row by row (one queen per row)
    2. For each row, try each column
    3. Check if placement is valid (no conflicts)
    4. Recursively place queens in remaining rows
    5. Backtrack if no valid placement found

    Conflict Tracking:
    - cols: Set of occupied columns
    - diag1: Set of occupied main diagonals (row - col)
    - diag2: Set of occupied anti-diagonals (row + col)

    Why this works:
    - All cells on same main diagonal have same (row - col)
    - All cells on same anti-diagonal have same (row + col)

    Time Complexity: O(n!)
    - For first row: n choices
    - For second row: ~(n-2) choices (exclude column and 2 diagonals)
    - Roughly n * (n-2) * (n-4) * ... ≈ n!

    Space Complexity: O(n²)
    - Board storage: O(n²)
    - Recursion depth: O(n)
    - Sets: O(n)

    Args:
        n: Board size (n×n)

    Returns:
        List of all valid board configurations
    """
    result = []

    # Track occupied columns and diagonals
    cols = set()      # Columns that have queens
    diag1 = set()     # Main diagonals (row - col)
    diag2 = set()     # Anti-diagonals (row + col)

    # Current board state
    board = [['.'] * n for _ in range(n)]

    def backtrack(row):
        """
        Place queens starting from the given row.

        Args:
            row: Current row to place a queen
        """
        # Base case: placed all n queens
        if row == n:
            # Convert board to required format
            solution = [''.join(row) for row in board]
            result.append(solution)
            return

        # Try placing queen in each column of current row
        for col in range(n):
            # Check if this position is under attack
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            # CHOOSE: Place queen at (row, col)
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            # EXPLORE: Move to next row
            backtrack(row + 1)

            # UNCHOOSE: Remove queen (backtrack)
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result


def solve_n_queens_array_tracking(n):
    """
    Alternative approach using arrays instead of sets for conflict tracking.

    Slightly faster due to array access vs set operations.

    Time Complexity: O(n!)
    Space Complexity: O(n²)
    """
    result = []

    # Track conflicts using boolean arrays
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)  # row - col ranges from -(n-1) to (n-1)
    diag2 = [False] * (2 * n - 1)  # row + col ranges from 0 to 2(n-1)

    board = [['.'] * n for _ in range(n)]

    def backtrack(row):
        if row == n:
            result.append([''.join(row) for row in board])
            return

        for col in range(n):
            # Convert diagonal indices to array indices
            d1 = row - col + n - 1  # Shift to make positive
            d2 = row + col

            if cols[col] or diag1[d1] or diag2[d2]:
                continue

            # CHOOSE
            board[row][col] = 'Q'
            cols[col] = True
            diag1[d1] = True
            diag2[d2] = True

            # EXPLORE
            backtrack(row + 1)

            # UNCHOOSE
            board[row][col] = '.'
            cols[col] = False
            diag1[d1] = False
            diag2[d2] = False

    backtrack(0)
    return result


def solve_n_queens_bitmask(n):
    """
    Highly optimized approach using bit manipulation.

    Instead of sets/arrays, use integers as bit masks.
    Each bit represents whether a position is under attack.

    This is the fastest approach but harder to understand.

    Time Complexity: O(n!)
    Space Complexity: O(n²)
    """
    result = []
    board = [['.'] * n for _ in range(n)]

    def backtrack(row, cols, diag1, diag2):
        """
        Args:
            cols, diag1, diag2: Bit masks where 1 = under attack
        """
        if row == n:
            result.append([''.join(row) for row in board])
            return

        # Available positions = positions not under attack
        # ((1 << n) - 1) creates n bits of 1s
        available = ((1 << n) - 1) & ~(cols | diag1 | diag2)

        # Try each available position
        while available:
            # Get rightmost set bit (lowest available column)
            position = available & -available

            # Find column number
            col = bin(position - 1).count('1')

            # CHOOSE
            board[row][col] = 'Q'

            # EXPLORE
            # Shift diagonals as we move down a row
            backtrack(
                row + 1,
                cols | position,
                (diag1 | position) << 1,
                (diag2 | position) >> 1
            )

            # UNCHOOSE
            board[row][col] = '.'

            # Remove this position from available
            available &= available - 1

    backtrack(0, 0, 0, 0)
    return result


def total_n_queens(n):
    """
    LeetCode #52: Return only the count of solutions (faster).

    When we only need the count, we can optimize by not building the board.

    Time Complexity: O(n!)
    Space Complexity: O(n)
    """
    count = [0]

    cols = set()
    diag1 = set()
    diag2 = set()

    def backtrack(row):
        if row == n:
            count[0] += 1
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return count[0]


def visualize_n_queens(n):
    """
    Visualize the search process for n-queens.
    """
    print(f"\nSolving {n}-Queens problem")
    print("=" * 60)

    result = []
    cols = set()
    diag1 = set()
    diag2 = set()
    board = [['.'] * n for _ in range(n)]
    call_count = [0]

    def print_board(highlight_row=None, highlight_col=None):
        """Print board with optional highlighting."""
        for r in range(n):
            row_str = ""
            for c in range(n):
                cell = board[r][c]
                if r == highlight_row and c == highlight_col:
                    row_str += f"[{cell}]"
                else:
                    row_str += f" {cell} "
            print(f"    {row_str}")

    def backtrack(row, depth=0):
        call_count[0] += 1
        indent = "  " * depth

        print(f"\n{indent}Row {row}: Trying to place queen")

        if row == n:
            result.append([''.join(row) for row in board])
            print(f"{indent}✓ Found solution #{len(result)}!")
            print_board()
            return

        tried = 0
        for col in range(n):
            tried += 1

            # Check conflicts
            conflicts = []
            if col in cols:
                conflicts.append("column")
            if (row - col) in diag1:
                conflicts.append("main diagonal")
            if (row + col) in diag2:
                conflicts.append("anti-diagonal")

            if conflicts:
                print(f"{indent}  Col {col}: ✗ Conflicts with {', '.join(conflicts)}")
                continue

            print(f"{indent}  Col {col}: ✓ Valid, placing queen")

            # CHOOSE
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            # EXPLORE
            backtrack(row + 1, depth + 1)

            # UNCHOOSE
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

            print(f"{indent}  Backtracked from col {col}")

        if tried == n:
            print(f"{indent}  Tried all columns in row {row}, backtracking...")

    backtrack(0)

    print(f"\n{'='*60}")
    print(f"Total recursive calls: {call_count[0]}")
    print(f"Total solutions found: {len(result)}")

    return result


def visualize_attack_patterns(n, row, col):
    """
    Show which cells are under attack from a queen at (row, col).
    """
    print(f"\nQueen at ({row}, {col}) on {n}×{n} board:")
    print("=" * 60)

    board = [['.' for _ in range(n)] for _ in range(n)]
    board[row][col] = 'Q'

    # Mark attacked cells
    for r in range(n):
        for c in range(n):
            if r == row or c == col:  # Row or column
                if board[r][c] != 'Q':
                    board[r][c] = 'x'
            elif r - c == row - col:  # Main diagonal
                if board[r][c] != 'Q':
                    board[r][c] = 'x'
            elif r + c == row + col:  # Anti-diagonal
                if board[r][c] != 'Q':
                    board[r][c] = 'x'

    # Print board
    for r in range(n):
        print("  " + " ".join(board[r]))

    print("\nLegend: Q = queen, x = under attack, . = safe")


def explain_diagonal_formula():
    """
    Explain how diagonal formulas work.
    """
    print("\n" + "="*60)
    print("UNDERSTANDING DIAGONALS")
    print("="*60)

    n = 4
    print(f"\n4×4 Board with coordinates:")
    print("     0   1   2   3")

    for r in range(n):
        row_str = f"  {r} "
        for c in range(n):
            row_str += f"({r},{c}) "
        print(row_str)

    print("\nMain Diagonal (↘) - Same (row - col):")
    print("  (0,0): 0-0 = 0")
    print("  (1,1): 1-1 = 0  ← Same diagonal!")
    print("  (2,2): 2-2 = 0  ← Same diagonal!")
    print("  (0,1): 0-1 = -1 (different diagonal)")
    print("  (1,2): 1-2 = -1 (different diagonal)")

    print("\nAnti-Diagonal (↙) - Same (row + col):")
    print("  (0,3): 0+3 = 3")
    print("  (1,2): 1+2 = 3  ← Same diagonal!")
    print("  (2,1): 2+1 = 3  ← Same diagonal!")
    print("  (0,2): 0+2 = 2  (different diagonal)")

    print("\nVisualization:")
    print("\nMain diagonals (row-col):")
    for r in range(n):
        row_str = "  "
        for c in range(n):
            row_str += f" {r-c:2d} "
        print(row_str)

    print("\nAnti-diagonals (row+col):")
    for r in range(n):
        row_str = "  "
        for c in range(n):
            row_str += f" {r+c:2d} "
        print(row_str)


def print_all_solutions(n):
    """
    Print all solutions for n-queens in a nice format.
    """
    solutions = solve_n_queens(n)

    print(f"\n{n}-Queens: {len(solutions)} solution(s)")
    print("=" * 60)

    for i, solution in enumerate(solutions, 1):
        print(f"\nSolution {i}:")
        for row in solution:
            print(f"  {row}")


def test_n_queens():
    """Comprehensive test cases."""

    # Test case 1: n=1
    result1 = solve_n_queens(1)
    assert len(result1) == 1
    assert result1[0] == ["Q"]

    # Test case 2: n=4
    result2 = solve_n_queens(4)
    assert len(result2) == 2

    # Test case 3: n=8 (classic 8-queens)
    result3 = solve_n_queens(8)
    assert len(result3) == 92  # Known result

    # Verify each solution is valid
    def is_valid_solution(solution):
        n = len(solution)
        queens = []

        # Find all queen positions
        for r in range(n):
            for c in range(n):
                if solution[r][c] == 'Q':
                    queens.append((r, c))

        # Check we have n queens
        if len(queens) != n:
            return False

        # Check no two queens attack each other
        for i in range(len(queens)):
            for j in range(i + 1, len(queens)):
                r1, c1 = queens[i]
                r2, c2 = queens[j]

                # Same row/column
                if r1 == r2 or c1 == c2:
                    return False

                # Same diagonal
                if abs(r1 - r2) == abs(c1 - c2):
                    return False

        return True

    # Verify all solutions for n=4
    for solution in result2:
        assert is_valid_solution(solution), f"Invalid solution: {solution}"

    # Test count-only version
    assert total_n_queens(4) == 2
    assert total_n_queens(8) == 92

    # Verify all three implementations give same results
    for n in [1, 4, 5]:
        r1 = solve_n_queens(n)
        r2 = solve_n_queens_array_tracking(n)
        r3 = solve_n_queens_bitmask(n)
        assert len(r1) == len(r2) == len(r3)

    print("All test cases passed!")


def analyze_complexity():
    """
    Analyze time complexity with measurements.
    """
    import time

    print("\n" + "="*60)
    print("COMPLEXITY ANALYSIS")
    print("="*60)

    print("\nTime Complexity: O(n!)")
    print("  Each row has fewer valid options than the previous")
    print("  Roughly: n * (n-2) * (n-4) * ... ≈ n!")

    print("\n" + "-"*60)
    print("Number of solutions for different n:")
    print("-"*60)
    print(f"{'n':>3} | {'Solutions':>10} | {'Time (ms)':>12}")
    print("-"*60)

    for n in range(1, 10):
        start = time.time()
        count = total_n_queens(n)
        elapsed = (time.time() - start) * 1000

        print(f"{n:3d} | {count:10d} | {elapsed:12.4f}")


if __name__ == "__main__":
    # Run tests
    test_n_queens()

    # Explain diagonal formulas
    explain_diagonal_formula()

    # Show attack patterns
    print("\n" + "="*60)
    print("ATTACK PATTERNS")
    print("="*60)
    visualize_attack_patterns(5, 2, 2)

    # Print all solutions for small n
    print("\n" + "="*60)
    print_all_solutions(4)

    # Visualize search process (only for small n)
    if True:  # Set to False to skip visualization
        print("\n" + "="*60)
        print("DETAILED SEARCH PROCESS (n=4)")
        print("="*60)
        visualize_n_queens(4)

    # Analyze complexity
    analyze_complexity()

    # Compare implementations
    print("\n" + "="*60)
    print("COMPARING IMPLEMENTATIONS")
    print("="*60)

    import time

    n = 8
    implementations = [
        ("Set-based", solve_n_queens),
        ("Array-based", solve_n_queens_array_tracking),
        ("Bit manipulation", solve_n_queens_bitmask),
    ]

    print(f"\nSolving {n}-Queens with different implementations:")
    print("-"*60)

    for name, func in implementations:
        start = time.time()
        result = func(n)
        elapsed = (time.time() - start) * 1000

        print(f"{name:20s}: {len(result)} solutions in {elapsed:8.4f} ms")
