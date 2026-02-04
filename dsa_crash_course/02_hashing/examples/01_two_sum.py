"""
Two Sum (LeetCode #1)

Problem:
Given an array of integers 'nums' and an integer 'target', return indices of
the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may
not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists

Follow-up: Can you come up with an algorithm that is less than O(n²) time?
"""


def two_sum_brute_force(nums, target):
    """
    Brute force approach - try all pairs.

    Approach:
    1. Use two nested loops
    2. For each number, check all numbers after it
    3. If sum equals target, return indices

    Time Complexity: O(n²) - nested loops
    Space Complexity: O(1) - no extra space

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        List of two indices [i, j] where nums[i] + nums[j] = target
    """
    n = len(nums)

    # Try every pair of numbers
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]

    return []


def two_sum(nums, target):
    """
    Optimal hash map approach - one pass with complement lookup.

    Approach:
    1. Use hash map to store seen numbers and their indices
    2. For each number, calculate complement (target - num)
    3. Check if complement exists in hash map
    4. If yes, return indices; if no, add current to hash map

    Why this works:
    - For two numbers a and b where a + b = target
    - When we see 'a', complement is 'b' (not seen yet)
    - When we see 'b', complement is 'a' (already in hash map)
    - Hash map gives O(1) lookup for complement

    Time Complexity: O(n) - single pass through array
    Space Complexity: O(n) - hash map stores up to n elements

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        List of two indices [i, j] where nums[i] + nums[j] = target
    """
    seen = {}  # value -> index mapping

    for i, num in enumerate(nums):
        complement = target - num

        # Check if complement was seen before
        if complement in seen:
            # Found the pair!
            return [seen[complement], i]

        # Store current number and its index
        seen[num] = i

    return []


def two_sum_two_pass(nums, target):
    """
    Two-pass hash map approach.

    Approach:
    1. First pass: Build hash map of all numbers and indices
    2. Second pass: For each number, check if complement exists

    Note: This is less efficient than one-pass but easier to understand.

    Time Complexity: O(n) - two passes
    Space Complexity: O(n) - hash map
    """
    # First pass: Build hash map
    num_to_index = {}
    for i, num in enumerate(nums):
        num_to_index[num] = i

    # Second pass: Look for complement
    for i, num in enumerate(nums):
        complement = target - num

        # Check if complement exists and is not the same element
        if complement in num_to_index and num_to_index[complement] != i:
            return [i, num_to_index[complement]]

    return []


def visualize_two_sum(nums, target):
    """
    Helper function to visualize the two sum process.

    Shows step-by-step how the hash map approach works.
    """
    print(f"\nFinding two numbers in {nums} that sum to {target}")
    print("=" * 60)

    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        print(f"\nStep {i + 1}:")
        print(f"  Current number: {num} at index {i}")
        print(f"  Looking for complement: {complement}")
        print(f"  Hash map before: {seen}")

        if complement in seen:
            print(f"  ✓ Found complement at index {seen[complement]}!")
            print(f"  Answer: [{seen[complement]}, {i}]")
            print(f"  Verification: {nums[seen[complement]]} + {num} = {target}")
            return [seen[complement], i]

        seen[num] = i
        print(f"  ✗ Complement not found, storing {num} -> {i}")

    print("\nNo solution found")
    return []


def test_two_sum():
    """Test cases covering various scenarios."""

    # Test case 1: Basic example
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum_brute_force([2, 7, 11, 15], 9) == [0, 1]

    # Test case 2: Answer not at beginning
    assert two_sum([3, 2, 4], 6) == [1, 2]

    # Test case 3: Same number twice
    assert two_sum([3, 3], 6) == [0, 1]

    # Test case 4: Negative numbers
    assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]

    # Test case 5: Zero in array
    assert two_sum([0, 4, 3, 0], 0) == [0, 3]

    # Test case 6: Large array
    test_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = two_sum(test_nums, 19)
    assert test_nums[result[0]] + test_nums[result[1]] == 19

    # Test case 7: Answer at end
    assert two_sum([1, 2, 3, 4, 5], 9) == [3, 4]

    # Test case 8: Minimum array size
    assert two_sum([1, 2], 3) == [0, 1]

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_two_sum()

    # Example with visualization
    nums = [2, 7, 11, 15]
    target = 9
    print("\n" + "=" * 60)
    print("EXAMPLE WITH VISUALIZATION")
    print("=" * 60)
    result = visualize_two_sum(nums, target)

    # Compare approaches
    print("\n" + "=" * 60)
    print("COMPARING APPROACHES")
    print("=" * 60)

    test_cases = [
        ([2, 7, 11, 15], 9),
        ([3, 2, 4], 6),
        ([3, 3], 6),
    ]

    for nums, target in test_cases:
        print(f"\nInput: nums = {nums}, target = {target}")

        # Brute force
        result1 = two_sum_brute_force(nums, target)
        print(f"Brute Force (O(n²)): {result1}")

        # Hash map
        result2 = two_sum(nums, target)
        print(f"Hash Map (O(n)):     {result2}")

        # Two pass
        result3 = two_sum_two_pass(nums, target)
        print(f"Two Pass (O(n)):     {result3}")

    # Performance comparison
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS")
    print("=" * 60)
    print("""
Approach          Time         Space      Best For
-------------------------------------------------
Brute Force       O(n²)        O(1)       Small arrays, space constrained
Hash Map (1-pass) O(n)         O(n)       Large arrays, optimal solution
Hash Map (2-pass) O(n)         O(n)       Easier to understand
Two Pointers      O(n log n)   O(1)       Sorted arrays only

Key Insights:
1. Hash map trades space for time (O(n) space for O(n) time)
2. One-pass is more efficient than two-pass
3. Hash map gives O(1) lookup vs O(n) for array search
4. This pattern applies to many "find pair" problems
    """)
