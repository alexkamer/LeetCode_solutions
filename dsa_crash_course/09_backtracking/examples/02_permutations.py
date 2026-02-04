"""
Permutations (LeetCode #46)

Problem:
Given an array nums of distinct integers, return all the possible permutations.
You can return the answer in any order.

Example 1:
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Example 2:
Input: nums = [0,1]
Output: [[0,1],[1,0]]

Example 3:
Input: nums = [1]
Output: [[1]]

Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique.

DECISION TREE VISUALIZATION for [1,2,3]:

Level 0:            []
                 /  |  \
Level 1:       [1] [2] [3]
              / \  / \  / \
Level 2:  [1,2][1,3][2,1][2,3][3,1][3,2]
           |    |    |    |    |    |
Level 3: [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]

At each level, we choose from remaining unused elements.
Only leaf nodes (length = n) are complete permutations.
"""


def permute_with_used_set(nums):
    """
    Backtracking with set to track used elements - most intuitive.

    Approach:
    1. Build permutation one element at a time
    2. At each position, try each unused element
    3. Use a set to track which elements are already used
    4. When permutation is complete (length = n), add to result

    Key Insight:
    Unlike subsets where every node is valid, only complete permutations
    (leaves of the tree) are valid solutions.

    Time Complexity: O(n * n!)
    - n! permutations
    - O(n) to copy each permutation

    Space Complexity: O(n)
    - Recursion depth is n
    - Used set takes O(n) space

    Args:
        nums: List of distinct integers

    Returns:
        List of all permutations
    """
    result = []

    def backtrack(path, used):
        # Base case: permutation is complete
        if len(path) == len(nums):
            result.append(path[:])  # Must copy!
            return

        # Try each unused element
        for i, num in enumerate(nums):
            if i in used:
                continue

            # CHOOSE: Use this element
            path.append(num)
            used.add(i)

            # EXPLORE: Continue building permutation
            backtrack(path, used)

            # UNCHOOSE: Remove element and mark as unused
            path.pop()
            used.remove(i)

    backtrack([], set())
    return result


def permute_with_used_array(nums):
    """
    Backtracking with boolean array - slightly faster than set.

    Using an array instead of set for tracking used elements
    can be faster due to better cache locality.

    Time Complexity: O(n * n!)
    Space Complexity: O(n)
    """
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            # CHOOSE
            path.append(nums[i])
            used[i] = True

            # EXPLORE
            backtrack(path)

            # UNCHOOSE
            path.pop()
            used[i] = False

    backtrack([])
    return result


def permute_swap_based(nums):
    """
    Swap-based approach - modifies input array in place.

    Approach:
    Instead of building path separately, we swap elements in the
    original array. At index i, we try putting each element from
    position i to end at position i.

    This is more space-efficient but modifies the input.

    Time Complexity: O(n * n!)
    Space Complexity: O(n) - only recursion stack
    """
    result = []
    nums = nums[:]  # Make a copy so we don't modify original

    def backtrack(start):
        # Base case: reached the end
        if start == len(nums):
            result.append(nums[:])
            return

        # Try each element at position 'start'
        for i in range(start, len(nums)):
            # CHOOSE: Put nums[i] at position 'start'
            nums[start], nums[i] = nums[i], nums[start]

            # EXPLORE: Fix this position and permute rest
            backtrack(start + 1)

            # UNCHOOSE: Restore original order
            nums[start], nums[i] = nums[i], nums[start]

    backtrack(0)
    return result


def permute_iterative(nums):
    """
    Iterative approach using queue - builds permutations level by level.

    Approach:
    Start with empty permutation. For each number, insert it at
    every possible position in each existing permutation.

    Example: [1,2,3]
    Start: [[]]
    Add 1: [[1]]
    Add 2: [[2,1], [1,2]]
    Add 3: [[3,2,1], [2,3,1], [2,1,3], [3,1,2], [1,3,2], [1,2,3]]

    Time Complexity: O(n * n!)
    Space Complexity: O(n * n!)
    """
    from collections import deque

    queue = deque([[]])

    for num in nums:
        # Process all permutations at current level
        level_size = len(queue)
        for _ in range(level_size):
            perm = queue.popleft()
            # Insert num at every possible position
            for i in range(len(perm) + 1):
                new_perm = perm[:i] + [num] + perm[i:]
                queue.append(new_perm)

    return list(queue)


def permute_pythonic(nums):
    """
    Using Python's itertools.permutations - for reference.

    This is the most concise way in Python, but doesn't show
    the backtracking algorithm.

    Time Complexity: O(n * n!)
    Space Complexity: O(n * n!)
    """
    from itertools import permutations
    return [list(p) for p in permutations(nums)]


def test_permutations():
    """Comprehensive test cases."""

    # Test case 1: Standard example
    nums1 = [1, 2, 3]
    result1 = permute_with_used_set(nums1)
    assert len(result1) == 6  # 3! = 6
    expected1 = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    for perm in expected1:
        assert perm in result1

    # Test case 2: Two elements
    nums2 = [0, 1]
    result2 = permute_with_used_set(nums2)
    assert len(result2) == 2  # 2! = 2
    assert [0, 1] in result2
    assert [1, 0] in result2

    # Test case 3: Single element
    nums3 = [1]
    result3 = permute_with_used_set(nums3)
    assert len(result3) == 1
    assert result3 == [[1]]

    # Test case 4: Four elements
    nums4 = [1, 2, 3, 4]
    result4 = permute_with_used_set(nums4)
    assert len(result4) == 24  # 4! = 24

    # Test case 5: Negative numbers
    nums5 = [-1, 0, 1]
    result5 = permute_with_used_set(nums5)
    assert len(result5) == 6

    # Verify all approaches give same results (sorted for comparison)
    for nums in [nums1, nums2, nums3]:
        r1 = sorted([sorted(p) for p in permute_with_used_set(nums)])
        r2 = sorted([sorted(p) for p in permute_with_used_array(nums)])
        r3 = sorted([sorted(p) for p in permute_swap_based(nums)])
        r4 = sorted([sorted(p) for p in permute_iterative(nums)])
        r5 = sorted([sorted(p) for p in permute_pythonic(nums)])
        assert r1 == r2 == r3 == r4 == r5

    # Verify all permutations are unique
    for nums in [nums1, nums2, nums4]:
        result = permute_with_used_set(nums)
        result_set = [tuple(p) for p in result]
        assert len(result_set) == len(set(result_set))  # No duplicates

    print("All test cases passed!")


def visualize_permutations(nums):
    """
    Visualize the backtracking process step by step.
    """
    print(f"\nGenerating permutations for: {nums}")
    print("=" * 60)

    result = []
    call_count = [0]

    def backtrack(path, used, depth=0):
        call_count[0] += 1
        indent = "  " * depth

        # Show current state
        unused = [nums[i] for i in range(len(nums)) if i not in used]
        print(f"{indent}Call #{call_count[0]}: path={path}, unused={unused}")

        # Base case: complete permutation
        if len(path) == len(nums):
            result.append(path[:])
            print(f"{indent}  -> Complete! Added: {path}")
            return

        # Try each unused element
        for i, num in enumerate(nums):
            if i in used:
                continue

            print(f"{indent}  Trying to add {num}")
            path.append(num)
            used.add(i)

            backtrack(path, used, depth + 1)

            path.pop()
            used.remove(i)
            print(f"{indent}  Backtracked, removed {num}")

    backtrack([], set())

    print(f"\nTotal function calls: {call_count[0]}")
    print(f"Total permutations: {len(result)}")
    print(f"Result: {result}")
    return result


def visualize_decision_tree(nums):
    """
    Show the decision tree structure.
    """
    print(f"\nDecision Tree for {nums}:")
    print("=" * 60)

    def build_tree(path, used, depth=0):
        indent = "  " * depth
        marker = "|-> " if depth > 0 else ""

        # Show current path
        if len(path) == len(nums):
            print(f"{indent}{marker}{path} (LEAF)")
        else:
            print(f"{indent}{marker}{path if path else 'START'}")

        # Show branches
        if len(path) < len(nums):
            for i, num in enumerate(nums):
                if i not in used:
                    new_used = used | {i}
                    build_tree(path + [num], new_used, depth + 1)

    build_tree([], set())


def compare_approaches():
    """
    Compare performance of different approaches.
    """
    import time

    test_nums = list(range(8))  # 8! = 40,320 permutations

    approaches = [
        ("Used Set", permute_with_used_set),
        ("Used Array", permute_with_used_array),
        ("Swap-based", permute_swap_based),
        ("Iterative", permute_iterative),
        ("Pythonic", permute_pythonic),
    ]

    print(f"\nPerformance comparison with {len(test_nums)} elements:")
    print("=" * 60)

    results = []
    for name, func in approaches:
        start = time.time()
        result = func(test_nums)
        elapsed = time.time() - start
        results.append((name, elapsed, len(result)))
        print(f"{name:15s}: {elapsed:.4f}s - {len(result)} permutations")

    # Find fastest
    fastest = min(results, key=lambda x: x[1])
    print(f"\nFastest: {fastest[0]}")

    # Show relative speeds
    print("\nRelative speeds:")
    for name, elapsed, count in results:
        ratio = elapsed / fastest[1]
        print(f"  {name:15s}: {ratio:.2f}x")


def analyze_complexity(n_values):
    """
    Demonstrate factorial growth.
    """
    import time
    import math

    print("\nComplexity Analysis - Factorial Growth:")
    print("=" * 70)
    print(f"{'n':>3} | {'Permutations':>15} | {'Time (s)':>10} | {'Theoretical':>15}")
    print("-" * 70)

    for n in n_values:
        if n > 9:  # Skip very large values
            print(f"{n:>3} | {'Too large':>15} | {'-':>10} | {math.factorial(n):>15}")
            continue

        nums = list(range(n))

        start = time.time()
        result = permute_with_used_array(nums)
        elapsed = time.time() - start

        theoretical = math.factorial(n)
        print(f"{n:>3} | {len(result):>15} | {elapsed:>10.6f} | {theoretical:>15}")


def demonstrate_swap_algorithm():
    """
    Show how the swap-based algorithm works step by step.
    """
    nums = [1, 2, 3]
    print(f"\nSwap-based algorithm visualization for {nums}:")
    print("=" * 60)

    result = []
    nums = nums[:]
    step = [0]

    def backtrack(start, depth=0):
        indent = "  " * depth

        if start == len(nums):
            step[0] += 1
            print(f"{indent}Step {step[0]}: Array = {nums} -> Add to result")
            result.append(nums[:])
            return

        for i in range(start, len(nums)):
            # Show swap
            if i != start:
                print(f"{indent}Swap nums[{start}]={nums[start]} with nums[{i}]={nums[i]}")
                nums[start], nums[i] = nums[i], nums[start]
                print(f"{indent}  Array is now: {nums}")
            else:
                print(f"{indent}Keep nums[{start}]={nums[start]} at position {start}")

            # Recurse
            backtrack(start + 1, depth + 1)

            # Show restore
            if i != start:
                print(f"{indent}Restore: Swap back nums[{start}]={nums[start]} with nums[{i}]={nums[i]}")
                nums[start], nums[i] = nums[i], nums[start]
                print(f"{indent}  Array is now: {nums}")

    backtrack(0)
    print(f"\nFinal result: {result}")


if __name__ == "__main__":
    # Run tests
    test_permutations()

    # Visualize small example
    visualize_permutations([1, 2, 3])

    # Show decision tree
    print("\n" + "=" * 60)
    visualize_decision_tree([1, 2, 3])

    # Show swap algorithm
    print("\n" + "=" * 60)
    demonstrate_swap_algorithm()

    # Compare approaches
    print("\n" + "=" * 60)
    compare_approaches()

    # Show complexity growth
    print("\n" + "=" * 60)
    analyze_complexity([3, 4, 5, 6, 7, 8, 9, 10])
