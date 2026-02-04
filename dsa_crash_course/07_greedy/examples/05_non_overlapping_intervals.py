"""
Non-overlapping Intervals (LeetCode #435)

Problem:
Given an array of intervals where intervals[i] = [start_i, end_i], return the
minimum number of intervals you need to remove to make the rest of the intervals
non-overlapping.

Example 1:
Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
Explanation: Remove [1,3] to make others non-overlapping.

Example 2:
Input: intervals = [[1,2],[1,2],[1,2]]
Output: 2
Explanation: Remove 2 intervals, keep 1.

Example 3:
Input: intervals = [[1,2],[2,3]]
Output: 0
Explanation: Already non-overlapping.

Constraints:
- 1 <= intervals.length <= 10^5
- intervals[i].length == 2
- -5 * 10^4 <= start_i < end_i <= 5 * 10^4
"""


def erase_overlap_intervals(intervals):
    """
    Greedy solution - sort by end time.
    
    Greedy Strategy:
    1. Sort intervals by end time
    2. Always keep interval that ends earliest
    3. Skip intervals that overlap with last kept interval
    4. Count skipped intervals
    
    Why Greedy Works:
    - This is classic "Activity Selection" problem
    - Goal: maximize non-overlapping intervals (minimize removals)
    - Greedy choice: Always pick interval that ends earliest
    - Why? Ends earliest → leaves most room for future intervals
    
    Proof (Exchange Argument):
    - Let G = greedy solution (sort by end, pick non-overlapping)
    - Let O = some optimal solution
    - If G ≠ O, let first interval where they differ be position i
    - G picks interval g_i (ends earliest among remaining)
    - O picks interval o_i (ends at same time or later)
    - Replace o_i with g_i in O → still valid (g_i ends no later)
    - New solution is at least as good as O
    - By induction, G is optimal
    
    Time Complexity: O(n log n) for sorting
    Space Complexity: O(1) excluding sort space
    
    Args:
        intervals: List of [start, end] intervals
        
    Returns:
        Minimum number of intervals to remove
    """
    if not intervals:
        return 0
    
    # Sort by end time (greedy criterion)
    intervals.sort(key=lambda x: x[1])
    
    removals = 0
    last_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        start, end = intervals[i]
        
        if start < last_end:
            # Overlapping, must remove this interval
            removals += 1
        else:
            # Non-overlapping, keep this interval
            last_end = end
    
    return removals


def erase_overlap_intervals_max_keep(intervals):
    """
    Alternative view: find maximum non-overlapping, then compute removals.
    
    This makes the connection to activity selection more explicit.
    
    removals = total - maximum_non_overlapping
    
    Time Complexity: O(n log n)
    Space Complexity: O(1)
    """
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[1])
    
    count = 1  # Keep first interval
    last_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] >= last_end:
            # Non-overlapping, keep it
            count += 1
            last_end = intervals[i][1]
    
    # Return number to remove
    return len(intervals) - count


def erase_overlap_intervals_sort_start(intervals):
    """
    What if we sort by start time instead?
    
    This is WRONG greedy choice! Included to show why end time is correct.
    
    Counter-example:
    intervals = [[1,10], [2,3], [4,5]]
    Sorted by start: [[1,10], [2,3], [4,5]]
    - Keep [1,10]
    - Remove [2,3] (overlaps)
    - Remove [4,5] (overlaps)
    - Result: 2 removals
    
    But optimal is:
    - Keep [2,3] and [4,5]
    - Remove [1,10]
    - Result: 1 removal
    
    Sorting by start is greedy, but not optimal!
    """
    if not intervals:
        return 0
    
    # WRONG: sort by start time
    intervals.sort(key=lambda x: x[0])
    
    removals = 0
    last_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        start, end = intervals[i]
        
        if start < last_end:
            # Overlapping - remove the one that ends later
            removals += 1
            last_end = min(last_end, end)
        else:
            last_end = end
    
    return removals


def erase_overlap_intervals_dp(intervals):
    """
    Dynamic programming solution (overkill for this problem).
    
    dp[i] = minimum removals for intervals[0..i] ending with intervals[i] kept
    
    Time Complexity: O(n^2)
    Space Complexity: O(n)
    
    Shows that greedy is superior when it works!
    """
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[1])
    n = len(intervals)
    
    # dp[i] = max non-overlapping intervals ending at i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if intervals[j][1] <= intervals[i][0]:
                # Non-overlapping
                dp[i] = max(dp[i], dp[j] + 1)
    
    max_keep = max(dp)
    return n - max_keep


def find_overlaps(intervals):
    """
    Helper function to identify which intervals overlap.
    
    Returns list of overlapping pairs.
    """
    overlaps = []
    n = len(intervals)
    
    for i in range(n):
        for j in range(i + 1, n):
            # Check if intervals[i] and intervals[j] overlap
            if intervals[i][0] < intervals[j][1] and intervals[j][0] < intervals[i][1]:
                overlaps.append((i, j))
    
    return overlaps


def test_non_overlapping_intervals():
    """Comprehensive test cases."""
    
    # Test case 1: Example from problem
    intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
    assert erase_overlap_intervals(intervals) == 1
    assert erase_overlap_intervals_max_keep(intervals) == 1
    
    # Test case 2: All same intervals
    intervals = [[1, 2], [1, 2], [1, 2]]
    assert erase_overlap_intervals(intervals) == 2
    
    # Test case 3: Already non-overlapping
    intervals = [[1, 2], [2, 3]]
    assert erase_overlap_intervals(intervals) == 0
    
    # Test case 4: All overlap
    intervals = [[1, 5], [2, 4], [3, 6]]
    result = erase_overlap_intervals(intervals)
    assert result == 2  # Keep [2,4], remove others
    
    # Test case 5: Chain of overlaps
    intervals = [[1, 3], [2, 4], [3, 5], [4, 6]]
    assert erase_overlap_intervals(intervals) == 2
    
    # Test case 6: No overlap, random order
    intervals = [[5, 6], [1, 2], [3, 4]]
    assert erase_overlap_intervals(intervals) == 0
    
    # Test case 7: One interval
    intervals = [[1, 2]]
    assert erase_overlap_intervals(intervals) == 0
    
    # Test case 8: Nested intervals
    intervals = [[1, 10], [2, 3], [4, 5], [6, 7]]
    assert erase_overlap_intervals(intervals) == 1
    
    # Test case 9: Adjacent intervals (touching but not overlapping)
    intervals = [[1, 2], [2, 3], [3, 4]]
    assert erase_overlap_intervals(intervals) == 0
    
    # Test case 10: Complex case
    intervals = [[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]]
    result = erase_overlap_intervals(intervals)
    assert result == 2
    
    print("All test cases passed!")


def demonstrate_greedy_vs_wrong():
    """
    Demonstrate why sorting by end time is correct, but start time is wrong.
    """
    print("Counter-example for sorting by START time:")
    print("-" * 60)
    
    intervals = [[1, 10], [2, 3], [4, 5]]
    print(f"Intervals: {intervals}")
    print()
    
    # Correct greedy (sort by end)
    result_correct = erase_overlap_intervals(intervals[:])
    print(f"Greedy (sort by END):   {result_correct} removals")
    print(f"  Keep: [2,3], [4,5]")
    print(f"  Remove: [1,10]")
    print()
    
    # Wrong greedy (sort by start) 
    result_wrong = erase_overlap_intervals_sort_start(intervals[:])
    print(f"Greedy (sort by START): {result_wrong} removals")
    print(f"  Keep: [1,10]")
    print(f"  Remove: [2,3], [4,5]")
    print()
    
    print(f"Correct greedy is better: {result_correct} < {result_wrong}")


def visualize_solution(intervals):
    """
    Visualize the interval removal process.
    """
    if not intervals:
        return
    
    print(f"\nOriginal intervals: {intervals}")
    print(f"Number of intervals: {len(intervals)}")
    
    # Find overlaps
    overlaps = find_overlaps(intervals)
    print(f"Overlapping pairs: {len(overlaps)}")
    
    # Sort and process
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    print(f"\nSorted by end time: {sorted_intervals}")
    print()
    
    kept = []
    removed = []
    last_end = float('-inf')
    
    for interval in sorted_intervals:
        start, end = interval
        if start >= last_end:
            kept.append(interval)
            last_end = end
            print(f"Keep   {interval} (end={end})")
        else:
            removed.append(interval)
            print(f"Remove {interval} (overlaps with previous)")
    
    print(f"\nFinal result:")
    print(f"  Kept: {kept}")
    print(f"  Removed: {removed}")
    print(f"  Minimum removals: {len(removed)}")


def explain_greedy_proof():
    """
    Detailed proof of correctness.
    
    PROBLEM: Minimize removals = Maximize kept intervals
    
    CLAIM: Greedy algorithm (sort by end time, keep non-overlapping) is optimal.
    
    PROOF BY EXCHANGE ARGUMENT:
    
    1. SETUP:
       - Let G = greedy solution (intervals kept by greedy)
       - Let O = optimal solution (some maximal non-overlapping set)
       - Sort both by end time
    
    2. ASSUMPTION:
       Suppose G ≠ O. We'll show we can transform O into G without losing optimality.
    
    3. FIND FIRST DIFFERENCE:
       - Let i be first position where G and O differ
       - Let g_i be the interval in G at position i
       - Let o_i be the interval in O at position i
       - By greedy choice: end(g_i) ≤ end(o_i)
    
    4. EXCHANGE:
       - Replace o_i with g_i in O
       - New set O' is still non-overlapping:
         * g_i doesn't overlap with intervals before (greedy ensures this)
         * g_i ends no later than o_i, so doesn't create new overlaps
       - |O'| = |O| (same size)
       - O' is still optimal
    
    5. INDUCTION:
       - O' now matches G in first i positions
       - Repeat for positions i+1, i+2, ...
       - Eventually O' = G
       - Therefore |G| = |O|, so G is optimal
    
    6. CONCLUSION:
       Greedy solution is optimal!
    
    WHY SORT BY END TIME?
    - Ending earlier leaves more room for future intervals
    - This is the greedy choice property
    - Sorting by start time doesn't have this property
    
    COUNTEREXAMPLE FOR START TIME:
    intervals = [[1,10], [2,3], [4,5]]
    - Sort by start: Keep [1,10], remove [2,3] and [4,5] → 2 removals
    - Sort by end: Keep [2,3] and [4,5], remove [1,10] → 1 removal
    - Start time greedy is suboptimal!
    
    TIME COMPLEXITY:
    - Sort: O(n log n)
    - Scan: O(n)
    - Total: O(n log n)
    
    SPACE COMPLEXITY:
    - O(1) extra space (excluding sort)
    - In-place sorting uses O(log n) stack space
    """
    print(__doc__)


if __name__ == "__main__":
    test_non_overlapping_intervals()
    
    print("\n" + "="*60)
    print("Example 1:")
    print("="*60)
    intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
    visualize_solution(intervals)
    
    print("\n" + "="*60)
    print("Example 2:")
    print("="*60)
    intervals = [[1, 2], [1, 2], [1, 2]]
    visualize_solution(intervals)
    
    print("\n" + "="*60)
    print("Why Sorting by END is Correct:")
    print("="*60)
    demonstrate_greedy_vs_wrong()
    
    print("\n" + "="*60)
    print("Greedy Correctness Proof:")
    print("="*60)
    explain_greedy_proof()
