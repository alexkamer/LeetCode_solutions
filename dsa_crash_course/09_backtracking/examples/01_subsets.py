"""
Subsets (LeetCode #78)

Problem:
Given an integer array nums of unique elements, return all possible subsets
(the power set).

The solution set must not contain duplicate subsets. Return the solution in
any order.

Example 1:
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

Example 2:
Input: nums = [0]
Output: [[],[0]]

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of nums are unique.

DECISION TREE VISUALIZATION for [1,2,3]:

                         []
                    /          \
              include 1      exclude 1
                  [1]             []
                /    \          /    \
             [1,2]   [1]      [2]    []
            /  \    /  \     /  \   /  \
        [1,2,3][1,2][1,3][1] [2,3][2] [3] []

At each level, we decide: include or exclude the current element.
Every node in the tree represents a valid subset!
"""


def subsets_backtracking(nums):
    """
    Classic backtracking approach - most intuitive.

    Approach:
    1. Start with empty subset
    2. At each step, decide whether to include current element
    3. Use start index to avoid duplicates
    4. Every state is a valid subset

    Key Insight:
    We don't need a base case that checks validity - every node in our
    decision tree is a valid subset. We just add to result at every step.

    Time Complexity: O(n * 2^n)
    - 2^n subsets total
    - O(n) to copy each subset into result

    Space Complexity: O(n)
    - Recursion depth is n
    - Not counting output array

    Args:
        nums: List of unique integers

    Returns:
        List of all possible subsets
    """
    result = []

    def backtrack(start, path):
        # Every node is a valid subset - add it to result
        result.append(path[:])  # Must copy the current path

        # Try including each remaining element
        for i in range(start, len(nums)):
            # CHOOSE: Include nums[i]
            path.append(nums[i])

            # EXPLORE: Continue with next elements
            backtrack(i + 1, path)

            # UNCHOOSE: Remove nums[i] to try other options
            path.pop()

    backtrack(0, [])
    return result


def subsets_iterative(nums):
    """
    Iterative approach - build subsets incrementally.

    Approach:
    1. Start with empty subset [[]]
    2. For each number, add it to all existing subsets
    3. This creates new subsets

    Example: [1,2,3]
    Start: [[]]
    Add 1: [[], [1]]
    Add 2: [[], [1], [2], [1,2]]
    Add 3: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]

    Time Complexity: O(n * 2^n)
    Space Complexity: O(1) not counting output
    """
    result = [[]]  # Start with empty subset

    for num in nums:
        # Add current number to all existing subsets
        new_subsets = []
        for subset in result:
            new_subsets.append(subset + [num])
        result.extend(new_subsets)

    return result


def subsets_bit_manipulation(nums):
    """
    Bit manipulation approach - very clever!

    Approach:
    For n elements, there are 2^n subsets.
    Each subset corresponds to a binary number from 0 to 2^n - 1.
    If bit i is set, include nums[i] in the subset.

    Example: [1,2,3]
    000 (0) -> []
    001 (1) -> [3]
    010 (2) -> [2]
    011 (3) -> [2,3]
    100 (4) -> [1]
    101 (5) -> [1,3]
    110 (6) -> [1,2]
    111 (7) -> [1,2,3]

    Time Complexity: O(n * 2^n)
    Space Complexity: O(1) not counting output
    """
    n = len(nums)
    result = []

    # Generate all 2^n possible subsets
    for mask in range(1 << n):  # 1 << n is 2^n
        subset = []
        for i in range(n):
            # Check if i-th bit is set
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)

    return result


def subsets_include_exclude(nums):
    """
    Explicit include/exclude recursion - shows the tree structure clearly.

    This approach explicitly shows the two branches at each node:
    - Left branch: include current element
    - Right branch: exclude current element

    Time Complexity: O(n * 2^n)
    Space Complexity: O(n)
    """
    result = []

    def backtrack(index, path):
        # Base case: processed all elements
        if index == len(nums):
            result.append(path[:])
            return

        # INCLUDE current element (left branch)
        path.append(nums[index])
        backtrack(index + 1, path)
        path.pop()

        # EXCLUDE current element (right branch)
        backtrack(index + 1, path)

    backtrack(0, [])
    return result


def test_subsets():
    """Comprehensive test cases."""

    # Test case 1: Standard example
    nums1 = [1, 2, 3]
    result1 = subsets_backtracking(nums1)
    expected1 = [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
    assert len(result1) == len(expected1) == 8
    assert all(subset in result1 for subset in expected1)

    # Test case 2: Single element
    nums2 = [0]
    result2 = subsets_backtracking(nums2)
    expected2 = [[], [0]]
    assert len(result2) == 2
    assert all(subset in result2 for subset in expected2)

    # Test case 3: Two elements
    nums3 = [1, 2]
    result3 = subsets_backtracking(nums3)
    expected3 = [[], [1], [2], [1,2]]
    assert len(result3) == 4

    # Test case 4: Four elements - 2^4 = 16 subsets
    nums4 = [1, 2, 3, 4]
    result4 = subsets_backtracking(nums4)
    assert len(result4) == 16

    # Test case 5: Negative numbers
    nums5 = [-1, 0, 1]
    result5 = subsets_backtracking(nums5)
    assert len(result5) == 8
    assert [] in result5
    assert [-1, 0, 1] in result5

    # Verify all approaches give same results
    for nums in [nums1, nums2, nums3]:
        r1 = sorted([sorted(s) for s in subsets_backtracking(nums)])
        r2 = sorted([sorted(s) for s in subsets_iterative(nums)])
        r3 = sorted([sorted(s) for s in subsets_bit_manipulation(nums)])
        r4 = sorted([sorted(s) for s in subsets_include_exclude(nums)])
        assert r1 == r2 == r3 == r4

    print("All test cases passed!")


def visualize_subsets(nums):
    """
    Visualize the backtracking process step by step.
    """
    print(f"\nGenerating subsets for: {nums}")
    print("=" * 60)

    result = []
    call_count = [0]

    def backtrack(start, path, depth=0):
        call_count[0] += 1
        indent = "  " * depth

        # Show current state
        print(f"{indent}Call #{call_count[0]}: start={start}, path={path}")

        # Add current subset
        result.append(path[:])
        print(f"{indent}  -> Added subset: {path}")

        # Try including each remaining element
        for i in range(start, len(nums)):
            print(f"{indent}  Trying to include nums[{i}]={nums[i]}")
            path.append(nums[i])
            backtrack(i + 1, path, depth + 1)
            path.pop()
            print(f"{indent}  Backtracked, removed {nums[i]}")

    backtrack(0, [])

    print(f"\nTotal function calls: {call_count[0]}")
    print(f"Total subsets generated: {len(result)}")
    print(f"Subsets: {result}")
    return result


def visualize_decision_tree(nums):
    """
    Show the decision tree structure explicitly.
    """
    print(f"\nDecision Tree for {nums}:")
    print("=" * 60)

    def build_tree(start, path, depth=0):
        indent = "  " * depth
        arrow = "|-> " if depth > 0 else ""
        print(f"{indent}{arrow}{path}")

        if start < len(nums):
            # Show which element we're deciding on
            if depth < len(nums):
                print(f"{indent}  Deciding on {nums[start]}:")

            # Show branches
            for i in range(start, len(nums)):
                build_tree(i + 1, path + [nums[i]], depth + 1)

    build_tree(0, [])


def compare_approaches():
    """
    Compare performance of different approaches.
    """
    import time

    test_nums = list(range(15))  # 15 elements = 32,768 subsets

    approaches = [
        ("Backtracking", subsets_backtracking),
        ("Iterative", subsets_iterative),
        ("Bit Manipulation", subsets_bit_manipulation),
        ("Include/Exclude", subsets_include_exclude),
    ]

    print(f"\nPerformance comparison with {len(test_nums)} elements:")
    print("=" * 60)

    results = []
    for name, func in approaches:
        start = time.time()
        result = func(test_nums)
        elapsed = time.time() - start
        results.append((name, elapsed, len(result)))
        print(f"{name:20s}: {elapsed:.4f}s - {len(result)} subsets")

    # Find fastest
    fastest = min(results, key=lambda x: x[1])
    print(f"\nFastest: {fastest[0]}")

    # Show relative speeds
    print("\nRelative speeds:")
    for name, elapsed, count in results:
        ratio = elapsed / fastest[1]
        print(f"  {name:20s}: {ratio:.2f}x")


def analyze_complexity(n_values):
    """
    Demonstrate exponential growth.
    """
    import time

    print("\nComplexity Analysis - Growth Rate:")
    print("=" * 60)
    print(f"{'n':>3} | {'Subsets':>10} | {'Time (s)':>10} | {'Theoretical':>12}")
    print("-" * 60)

    for n in n_values:
        nums = list(range(n))

        start = time.time()
        result = subsets_backtracking(nums)
        elapsed = time.time() - start

        theoretical = 2 ** n
        print(f"{n:>3} | {len(result):>10} | {elapsed:>10.6f} | {theoretical:>12}")


if __name__ == "__main__":
    # Run tests
    test_subsets()

    # Visualize small example
    visualize_subsets([1, 2, 3])

    # Show decision tree
    visualize_decision_tree([1, 2, 3])

    # Compare approaches
    print("\n" + "=" * 60)
    compare_approaches()

    # Show complexity growth
    print("\n" + "=" * 60)
    analyze_complexity([5, 8, 10, 12, 15])
