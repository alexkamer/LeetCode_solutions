"""
Combination Sum (LeetCode #39)

Problem:
Given an array of distinct integers candidates and a target integer target, return
a list of all unique combinations of candidates where the chosen numbers sum to target.
You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two
combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up
to target is less than 150 combinations for the given input.

Example 1:
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.

Example 2:
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]

Example 3:
Input: candidates = [2], target = 1
Output: []

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct
- 1 <= target <= 40

DECISION TREE for candidates=[2,3,6,7], target=7:

                        []
        ┌───────┬───────┼───────┬───────┐
      [2]     [3]     [6]     [7]      STOP
     ┌─┼─┐   ┌─┼─┐    ├─┐      └─→ Valid! (7=7)
   [2,2] ... [3,3] [3,6] [3,7] [6,6] [6,7]
    ┌┴┐      └─→ Valid! (3+3+...>7)
  [2,2,2] [2,2,3]
    ├─┐    └─→ Valid! (2+2+3=7)
  [2,2,2,2] [2,2,2,3]
    ...      (sum>7, prune)

Key insight: At each step, we can choose the SAME element again (unlimited reuse).
"""


def combination_sum(candidates, target):
    """
    Backtracking with index tracking to allow reuse and avoid duplicates.

    Key Insights:
    1. We can reuse the same number multiple times
    2. To avoid duplicate combinations, we process candidates in order
    3. Once we skip a candidate, we never come back to it in that branch

    Approach:
    - At each position, try all candidates from current index onwards
    - After using a candidate, we can use it again (don't increment index)
    - This naturally avoids duplicates like [2,3] and [3,2]

    Example: candidates=[2,3], target=5
    - Try [2]: remaining=3, can try [2,2], [2,3], ... or [3]
    - Try [3]: remaining=2, can try [3,2] - NO! Would duplicate [2,3]
    - Solution: When trying [3], only try [3,...] not earlier numbers

    Time Complexity: O(n^(t/m))
    - n = number of candidates
    - t = target value
    - m = minimum candidate
    - In worst case, we can go t/m levels deep, with n choices per level

    Space Complexity: O(t/m) - recursion depth

    Args:
        candidates: List of distinct positive integers
        target: Target sum

    Returns:
        List of all unique combinations that sum to target
    """
    result = []

    def backtrack(start, path, remaining):
        """
        Args:
            start: Index to start searching from (prevents duplicates)
            path: Current combination being built
            remaining: Remaining sum needed to reach target
        """
        # Base case: found a valid combination
        if remaining == 0:
            result.append(path[:])  # Must copy!
            return

        # Base case: exceeded target (pruning)
        if remaining < 0:
            return

        # Try each candidate from start index onwards
        for i in range(start, len(candidates)):
            candidate = candidates[i]

            # CHOOSE: Add candidate to current combination
            path.append(candidate)

            # EXPLORE: Continue from same index (can reuse this number)
            # remaining - candidate: update remaining target
            backtrack(i, path, remaining - candidate)

            # UNCHOOSE: Remove candidate for next iteration
            path.pop()

    backtrack(0, [], target)
    return result


def combination_sum_optimized(candidates, target):
    """
    Optimized version with early termination.

    Optimization: Sort candidates first, then we can break early
    when a candidate is too large.

    Time Complexity: O(n^(t/m)) - same as before but with better constants
    Space Complexity: O(t/m)
    """
    result = []
    candidates.sort()  # Sort for early termination

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            candidate = candidates[i]

            # Early termination: if this candidate is too large,
            # all remaining candidates are also too large (since sorted)
            if candidate > remaining:
                break

            path.append(candidate)
            backtrack(i, path, remaining - candidate)
            path.pop()

    backtrack(0, [], target)
    return result


def combination_sum_iterative(candidates, target):
    """
    Iterative approach using a stack (BFS-like).

    Less common but shows the iterative equivalent of recursion.

    Time Complexity: O(n^(t/m))
    Space Complexity: O(n^(t/m)) - stores all partial solutions
    """
    result = []
    stack = [(0, [], target)]  # (start_index, path, remaining)

    while stack:
        start, path, remaining = stack.pop()

        if remaining == 0:
            result.append(path)
            continue

        if remaining < 0:
            continue

        for i in range(start, len(candidates)):
            candidate = candidates[i]
            if candidate <= remaining:
                # Create new path (must copy!)
                new_path = path + [candidate]
                stack.append((i, new_path, remaining - candidate))

    return result


def combination_sum_with_count(candidates, target):
    """
    Alternative representation: Return combinations as dictionaries
    showing count of each candidate.

    Example: [2,2,3] becomes {2: 2, 3: 1}

    This is useful when you need to know how many times each number is used.
    """
    result = []

    def backtrack(start, counts, remaining):
        if remaining == 0:
            result.append(counts.copy())
            return

        for i in range(start, len(candidates)):
            candidate = candidates[i]

            if candidate > remaining:
                continue

            # CHOOSE: Increment count
            counts[candidate] = counts.get(candidate, 0) + 1

            # EXPLORE
            backtrack(i, counts, remaining - candidate)

            # UNCHOOSE: Decrement count
            counts[candidate] -= 1
            if counts[candidate] == 0:
                del counts[candidate]

    backtrack(0, {}, target)
    return result


def visualize_combination_sum(candidates, target):
    """
    Visualize the backtracking process step by step.
    """
    print(f"\nFinding combinations for candidates={candidates}, target={target}")
    print("=" * 70)

    result = []
    call_count = [0]

    def backtrack(start, path, remaining, depth=0):
        call_count[0] += 1
        indent = "  " * depth

        # Show current state
        current_sum = sum(path)
        available = candidates[start:]
        print(f"{indent}Call #{call_count[0]}: path={path}, sum={current_sum}, "
              f"remaining={remaining}, available={available}")

        # Base case: found solution
        if remaining == 0:
            result.append(path[:])
            print(f"{indent}  ✓ Found valid combination: {path}")
            return

        # Base case: exceeded target (prune)
        if remaining < 0:
            print(f"{indent}  ✗ Sum exceeded target, backtrack")
            return

        # Try each candidate
        for i in range(start, len(candidates)):
            candidate = candidates[i]

            print(f"{indent}  Trying to add {candidate}")

            path.append(candidate)
            backtrack(i, path, remaining - candidate, depth + 1)
            path.pop()

            print(f"{indent}  Backtracked, removed {candidate}")

    backtrack(0, [], target)

    print(f"\n{'='*70}")
    print(f"Total function calls: {call_count[0]}")
    print(f"Valid combinations found: {len(result)}")
    print(f"Results: {result}")

    return result


def visualize_decision_tree(candidates, target):
    """
    Show the decision tree structure more compactly.
    """
    print(f"\nDecision Tree for candidates={candidates}, target={target}")
    print("=" * 70)

    def build_tree(start, path, remaining, depth=0):
        indent = "  " * depth
        current_sum = sum(path)

        # Show current node
        if remaining == 0:
            print(f"{indent}{path} = {current_sum} ✓ VALID")
            return

        if remaining < 0:
            print(f"{indent}{path} = {current_sum} ✗ EXCEEDED")
            return

        if depth == 0:
            print(f"{indent}START (target={target})")
        else:
            print(f"{indent}{path} = {current_sum} (need {remaining} more)")

        # Show branches
        for i in range(start, len(candidates)):
            candidate = candidates[i]
            if remaining - candidate >= 0 or depth < 3:  # Limit depth for readability
                build_tree(i, path + [candidate], remaining - candidate, depth + 1)

    build_tree(0, [], target)


def analyze_why_no_duplicates():
    """
    Explain why the algorithm doesn't produce duplicate combinations.
    """
    print("\n" + "="*70)
    print("WHY NO DUPLICATES?")
    print("="*70)

    print("\nKey insight: Use 'start' index to maintain ordering")
    print("\nExample: candidates=[2,3], target=5")
    print("\nWithout index constraint (WRONG):")
    print("  []")
    print("  ├─ [2]")
    print("  │  ├─ [2,2]")
    print("  │  │  └─ [2,2,2] ✗")
    print("  │  └─ [2,3] ✓")
    print("  └─ [3]")
    print("     └─ [3,2] ✓  ← DUPLICATE of [2,3]!")

    print("\nWith index constraint (CORRECT):")
    print("  []")
    print("  ├─ [2] (can use 2, 3)")
    print("  │  ├─ [2,2] (can use 2, 3)")
    print("  │  │  └─ [2,2,2] ✗")
    print("  │  └─ [2,3] ✓")
    print("  └─ [3] (can only use 3)")
    print("     └─ [3,3] ✗")

    print("\nRule: After choosing index i, next choice starts from i (not 0)")
    print("This ensures: Always build combinations in non-decreasing order")
    print("Result: [2,3] is found, but [3,2] is never generated")


def compare_with_and_without_reuse():
    """
    Compare this problem with Combination Sum II (no reuse allowed).
    """
    print("\n" + "="*70)
    print("COMPARISON: With vs Without Reuse")
    print("="*70)

    candidates = [2, 3]
    target = 6

    print(f"\nCandidates: {candidates}, Target: {target}")

    print("\n1. WITH REUSE (this problem - Combination Sum):")
    print("   Can use each number unlimited times")
    result1 = combination_sum(candidates, target)
    for combo in result1:
        print(f"   {combo} = {sum(combo)}")

    print("\n2. WITHOUT REUSE (Combination Sum II):")
    print("   Can use each number only once")
    print("   Would need: backtrack(i+1, ...) instead of backtrack(i, ...)")
    print("   Results would be different (fewer combinations)")


def test_combination_sum():
    """Comprehensive test cases."""

    # Test case 1: Standard example
    result1 = combination_sum([2, 3, 6, 7], 7)
    assert sorted(map(sorted, result1)) == sorted([[2, 2, 3], [7]])

    # Test case 2: Multiple solutions
    result2 = combination_sum([2, 3, 5], 8)
    expected2 = [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert sorted(map(sorted, result2)) == sorted(map(sorted, expected2))

    # Test case 3: No solution
    result3 = combination_sum([2], 1)
    assert result3 == []

    # Test case 4: Single element solution
    result4 = combination_sum([1], 5)
    assert result4 == [[1, 1, 1, 1, 1]]

    # Test case 5: Exact match
    result5 = combination_sum([5, 10, 15], 15)
    assert [15] in result5
    assert [5, 5, 5] in result5

    # Test case 6: All candidates too large
    result6 = combination_sum([10, 20, 30], 5)
    assert result6 == []

    # Test case 7: Large target
    result7 = combination_sum([2], 10)
    assert result7 == [[2, 2, 2, 2, 2]]

    # Verify optimized version gives same results
    for candidates, target in [
        ([2, 3, 6, 7], 7),
        ([2, 3, 5], 8),
        ([2], 1),
    ]:
        r1 = sorted(map(sorted, combination_sum(candidates, target)))
        r2 = sorted(map(sorted, combination_sum_optimized(candidates, target)))
        assert r1 == r2

    # Verify iterative version
    r3 = sorted(map(sorted, combination_sum_iterative([2, 3, 6, 7], 7)))
    assert r3 == sorted([[2, 2, 3], [7]])

    print("All test cases passed!")


def analyze_complexity():
    """
    Analyze and demonstrate the time complexity.
    """
    import time

    print("\n" + "="*70)
    print("COMPLEXITY ANALYSIS")
    print("="*70)

    print("\nTime Complexity: O(n^(t/m))")
    print("  n = number of candidates")
    print("  t = target")
    print("  m = minimum candidate value")
    print("\nWhy? Maximum recursion depth is t/m")
    print("     At each level, we can branch n ways")

    print("\n" + "-"*70)
    print("Practical measurements:")
    print("-"*70)

    test_cases = [
        ([2, 3], 10),
        ([2, 3, 5], 10),
        ([2, 3, 5, 7], 10),
    ]

    for candidates, target in test_cases:
        start = time.time()
        result = combination_sum(candidates, target)
        elapsed = time.time() - start

        print(f"\ncandidates={candidates}, target={target}")
        print(f"  Solutions found: {len(result)}")
        print(f"  Time: {elapsed*1000:.4f} ms")


if __name__ == "__main__":
    # Run tests
    test_combination_sum()

    # Explain the no-duplicates mechanism
    analyze_why_no_duplicates()

    # Compare with/without reuse
    compare_with_and_without_reuse()

    # Visualization examples
    print("\n" + "="*70)
    print("VISUALIZATION EXAMPLES")
    print("="*70)

    print("\nExample 1: Small tree")
    print("-" * 70)
    visualize_decision_tree([2, 3], 5)

    print("\n" + "-" * 70)
    print("\nExample 2: Detailed backtracking")
    print("-" * 70)
    visualize_combination_sum([2, 3, 6, 7], 7)

    print("\n" + "-" * 70)
    print("\nExample 3: No solution")
    print("-" * 70)
    visualize_combination_sum([5, 10], 7)

    # Analyze complexity
    analyze_complexity()

    # Show count representation
    print("\n" + "="*70)
    print("ALTERNATIVE REPRESENTATION")
    print("="*70)
    candidates = [2, 3, 5]
    target = 8
    result_lists = combination_sum(candidates, target)
    result_counts = combination_sum_with_count(candidates, target)

    print(f"\nCandidates: {candidates}, Target: {target}")
    print("\nAs lists:")
    for combo in result_lists:
        print(f"  {combo}")

    print("\nAs counts:")
    for counts in result_counts:
        print(f"  {counts}")
