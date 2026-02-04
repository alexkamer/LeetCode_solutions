"""
Binary Search (Classic)

Problem:
Given a sorted array of integers 'nums' and an integer 'target', write a function
to search for 'target' in 'nums'. If 'target' exists, return its index. Otherwise,
return -1.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4

Example 2:
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1

Example 3:
Input: nums = [5], target = 5
Output: 0

Constraints:
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- All integers in nums are unique
- nums is sorted in ascending order
"""


def binary_search(nums, target):
    """
    Classic binary search implementation - the foundation of all binary search variants.

    Approach:
    1. Start with two pointers: left at 0, right at len(nums) - 1
    2. While left <= right:
       - Calculate mid point
       - If nums[mid] equals target, found it!
       - If nums[mid] < target, search right half (left = mid + 1)
       - If nums[mid] > target, search left half (right = mid - 1)
    3. If loop exits, target not found

    Why this works:
    - Array is sorted, so we can eliminate half the search space at each step
    - Each comparison tells us which half contains the target (if it exists)
    - Guaranteed to find target if it exists, or determine it doesn't exist

    Time Complexity: O(log n) - halve search space each iteration
    Space Complexity: O(1) - only using a few variables

    Args:
        nums: Sorted array of integers
        target: Value to find

    Returns:
        Index of target if found, -1 otherwise
    """
    left = 0
    right = len(nums) - 1

    while left <= right:
        # Calculate mid (avoiding overflow in languages with fixed int size)
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid  # Found it!
        elif nums[mid] < target:
            # Target is in right half
            left = mid + 1
        else:
            # Target is in left half
            right = mid - 1

    # Target not found
    return -1


def binary_search_recursive(nums, target):
    """
    Recursive implementation of binary search.

    Same logic as iterative version, but uses recursion.
    Less commonly used in practice due to O(log n) space complexity.

    Time Complexity: O(log n)
    Space Complexity: O(log n) - due to recursion call stack
    """
    def helper(left, right):
        if left > right:
            return -1

        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return helper(mid + 1, right)
        else:
            return helper(left, mid - 1)

    return helper(0, len(nums) - 1)


def binary_search_alternative(nums, target):
    """
    Alternative boundary style - uses 'right = len(nums)' instead of 'len(nums) - 1'.

    This style is useful for certain variants (like finding insert position).

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left = 0
    right = len(nums)  # Note: not len(nums) - 1

    while left < right:  # Note: not <=
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid  # Note: not mid - 1

    # Check if we found it (left will point to where it should be)
    if left < len(nums) and nums[left] == target:
        return left
    return -1


def visualize_binary_search(nums, target):
    """
    Visualize how binary search works step by step.

    This helps understand the algorithm by showing each iteration.
    """
    left = 0
    right = len(nums) - 1
    iteration = 0

    print(f"Searching for {target} in {nums}")
    print(f"Array indices: {list(range(len(nums)))}\n")

    while left <= right:
        iteration += 1
        mid = left + (right - left) // 2

        # Visual representation
        visual = [' '] * len(nums)
        visual[left] = 'L'
        visual[right] = 'R'
        visual[mid] = 'M'

        print(f"Iteration {iteration}:")
        print(f"  Array:   {nums}")
        print(f"  Markers: {visual}")
        print(f"  Left={left}, Mid={mid}, Right={right}")
        print(f"  nums[mid]={nums[mid]}")

        if nums[mid] == target:
            print(f"  ✓ Found {target} at index {mid}!")
            return mid
        elif nums[mid] < target:
            print(f"  {nums[mid]} < {target}, search right half")
            left = mid + 1
        else:
            print(f"  {nums[mid]} > {target}, search left half")
            right = mid - 1
        print()

    print(f"  ✗ {target} not found in array")
    return -1


def test_binary_search():
    """Comprehensive test cases for binary search."""

    # Test case 1: Target in middle
    assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4

    # Test case 2: Target not present
    assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1

    # Test case 3: Single element - found
    assert binary_search([5], 5) == 0

    # Test case 4: Single element - not found
    assert binary_search([5], 3) == -1

    # Test case 5: Target at start
    assert binary_search([1, 2, 3, 4, 5], 1) == 0

    # Test case 6: Target at end
    assert binary_search([1, 2, 3, 4, 5], 5) == 4

    # Test case 7: Two elements - first
    assert binary_search([1, 3], 1) == 0

    # Test case 8: Two elements - second
    assert binary_search([1, 3], 3) == 1

    # Test case 9: Two elements - not found
    assert binary_search([1, 3], 2) == -1

    # Test case 10: Large array
    assert binary_search(list(range(1000)), 500) == 500

    # Test case 11: Negative numbers
    assert binary_search([-100, -50, -10, 0, 10, 50, 100], -10) == 2

    # Test case 12: All same except one
    assert binary_search([1, 1, 1, 1, 2], 2) == 4

    # Test recursive version
    assert binary_search_recursive([-1, 0, 3, 5, 9, 12], 9) == 4
    assert binary_search_recursive([-1, 0, 3, 5, 9, 12], 2) == -1

    # Test alternative version
    assert binary_search_alternative([-1, 0, 3, 5, 9, 12], 9) == 4
    assert binary_search_alternative([-1, 0, 3, 5, 9, 12], 2) == -1

    print("All test cases passed!")


def compare_with_linear_search():
    """
    Compare binary search with linear search to demonstrate the speedup.
    """
    import time

    # Create large sorted array
    size = 1000000
    nums = list(range(size))
    target = 999999

    # Linear search
    start = time.time()
    for i, num in enumerate(nums):
        if num == target:
            linear_result = i
            break
    linear_time = time.time() - start

    # Binary search
    start = time.time()
    binary_result = binary_search(nums, target)
    binary_time = time.time() - start

    print(f"\nPerformance Comparison (n = {size:,}):")
    print(f"Linear Search: {linear_time:.6f} seconds")
    print(f"Binary Search: {binary_time:.6f} seconds")
    print(f"Speedup: {linear_time / binary_time:.1f}x faster")
    print(f"\nBoth found target at index {binary_result}")


if __name__ == "__main__":
    # Run tests
    test_binary_search()

    # Visualize some searches
    print("\n" + "="*60)
    print("VISUALIZATION EXAMPLES")
    print("="*60 + "\n")

    print("Example 1: Target found")
    print("-" * 60)
    visualize_binary_search([-1, 0, 3, 5, 9, 12], 9)

    print("\n" + "-" * 60)
    print("Example 2: Target not found")
    print("-" * 60)
    visualize_binary_search([-1, 0, 3, 5, 9, 12], 2)

    print("\n" + "-" * 60)
    print("Example 3: Target at beginning")
    print("-" * 60)
    visualize_binary_search([1, 2, 3, 4, 5, 6, 7], 1)

    # Compare with linear search
    print("\n" + "="*60)
    compare_with_linear_search()
