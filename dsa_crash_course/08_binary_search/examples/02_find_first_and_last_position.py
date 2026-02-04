"""
Find First and Last Position of Element in Sorted Array

Problem:
Given an array of integers 'nums' sorted in non-decreasing order, find the starting
and ending position of a given 'target' value.

If 'target' is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Example 2:
Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]

Example 3:
Input: nums = [], target = 0
Output: [-1,-1]

Example 4:
Input: nums = [1], target = 1
Output: [0,0]

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- nums is a non-decreasing array
- -10^9 <= target <= 10^9
"""


def search_range(nums, target):
    """
    Find first and last position using two binary searches.

    Approach:
    1. Use binary search to find the leftmost (first) occurrence
    2. Use binary search to find the rightmost (last) occurrence
    3. Return [first, last] or [-1, -1] if not found

    This is the standard approach and cleanly separates the two searches.

    Time Complexity: O(log n) - two binary searches
    Space Complexity: O(1) - only using a few variables

    Args:
        nums: Sorted array of integers
        target: Value to find

    Returns:
        [first_index, last_index] or [-1, -1] if not found
    """
    if not nums:
        return [-1, -1]

    # Find first (leftmost) occurrence
    first = find_first_occurrence(nums, target)

    # If not found, return [-1, -1]
    if first == -1:
        return [-1, -1]

    # Find last (rightmost) occurrence
    last = find_last_occurrence(nums, target)

    return [first, last]


def find_first_occurrence(nums, target):
    """
    Find the leftmost (first) occurrence of target.

    Key insight: When we find target, we don't return immediately.
    We save it and keep searching in the left half to find earlier occurrences.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left = 0
    right = len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            result = mid      # Found it, but keep searching left
            right = mid - 1   # Continue in left half
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def find_last_occurrence(nums, target):
    """
    Find the rightmost (last) occurrence of target.

    Key insight: When we find target, save it and keep searching
    in the right half to find later occurrences.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left = 0
    right = len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            result = mid      # Found it, but keep searching right
            left = mid + 1    # Continue in right half
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def search_range_single_pass(nums, target):
    """
    Alternative: Find first, then find last starting from first.

    This is slightly more efficient when target appears many times,
    but has similar worst-case complexity.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    if not nums:
        return [-1, -1]

    # Find any occurrence first
    left = 0
    right = len(nums) - 1
    found_index = -1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            found_index = mid
            break
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    if found_index == -1:
        return [-1, -1]

    # Expand left and right from found position
    first = found_index
    while first > 0 and nums[first - 1] == target:
        first -= 1

    last = found_index
    while last < len(nums) - 1 and nums[last + 1] == target:
        last += 1

    return [first, last]


def search_range_boundary_template(nums, target):
    """
    Using the boundary search template style.

    This style is more elegant and avoids the 'result' variable.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    if not nums:
        return [-1, -1]

    # Find leftmost position where nums[i] >= target
    def find_left():
        left, right = 0, len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left

    # Find leftmost position where nums[i] > target
    def find_right():
        left, right = 0, len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] <= target:
                left = mid + 1
            else:
                right = mid
        return left

    left = find_left()
    right = find_right() - 1

    # Check if target exists
    if left <= right and left < len(nums) and nums[left] == target:
        return [left, right]
    return [-1, -1]


def count_occurrences(nums, target):
    """
    Bonus: Count how many times target appears.

    Uses the same technique as search_range.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    first = find_first_occurrence(nums, target)
    if first == -1:
        return 0

    last = find_last_occurrence(nums, target)
    return last - first + 1


def visualize_search(nums, target):
    """
    Visualize finding first and last occurrences.
    """
    print(f"\nSearching for {target} in {nums}")
    print(f"Array indices: {list(range(len(nums)))}")

    # Find first occurrence
    print("\n--- Finding FIRST occurrence ---")
    left, right = 0, len(nums) - 1
    result = -1
    iteration = 0

    while left <= right:
        iteration += 1
        mid = left + (right - left) // 2

        visual = [' '] * len(nums)
        visual[left] = 'L'
        visual[right] = 'R'
        visual[mid] = 'M'

        print(f"\nIteration {iteration}:")
        print(f"  Array:   {nums}")
        print(f"  Markers: {visual}")
        print(f"  nums[mid]={nums[mid]}")

        if nums[mid] == target:
            result = mid
            print(f"  Found {target} at {mid}, but searching left for first occurrence")
            right = mid - 1
        elif nums[mid] < target:
            print(f"  {nums[mid]} < {target}, search right")
            left = mid + 1
        else:
            print(f"  {nums[mid]} > {target}, search left")
            right = mid - 1

    print(f"\nFirst occurrence: {result}")

    # Find last occurrence
    print("\n--- Finding LAST occurrence ---")
    left, right = 0, len(nums) - 1
    last_result = -1
    iteration = 0

    while left <= right:
        iteration += 1
        mid = left + (right - left) // 2

        visual = [' '] * len(nums)
        visual[left] = 'L'
        visual[right] = 'R'
        visual[mid] = 'M'

        print(f"\nIteration {iteration}:")
        print(f"  Array:   {nums}")
        print(f"  Markers: {visual}")
        print(f"  nums[mid]={nums[mid]}")

        if nums[mid] == target:
            last_result = mid
            print(f"  Found {target} at {mid}, but searching right for last occurrence")
            left = mid + 1
        elif nums[mid] < target:
            print(f"  {nums[mid]} < {target}, search right")
            left = mid + 1
        else:
            print(f"  {nums[mid]} > {target}, search left")
            right = mid - 1

    print(f"\nLast occurrence: {last_result}")
    print(f"\nFinal result: [{result}, {last_result}]")


def test_search_range():
    """Comprehensive test cases."""

    # Test case 1: Multiple occurrences in middle
    assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4]

    # Test case 2: Target not found
    assert search_range([5, 7, 7, 8, 8, 10], 6) == [-1, -1]

    # Test case 3: Empty array
    assert search_range([], 0) == [-1, -1]

    # Test case 4: Single element - found
    assert search_range([1], 1) == [0, 0]

    # Test case 5: Single element - not found
    assert search_range([1], 2) == [-1, -1]

    # Test case 6: All elements are target
    assert search_range([5, 5, 5, 5], 5) == [0, 3]

    # Test case 7: Target at start
    assert search_range([1, 1, 2, 3, 4], 1) == [0, 1]

    # Test case 8: Target at end
    assert search_range([1, 2, 3, 4, 4], 4) == [3, 4]

    # Test case 9: Single occurrence
    assert search_range([1, 2, 3, 4, 5], 3) == [2, 2]

    # Test case 10: Two elements, both target
    assert search_range([1, 1], 1) == [0, 1]

    # Test case 11: Large array with many duplicates
    arr = [1] * 1000 + [2] * 1000 + [3] * 1000
    assert search_range(arr, 2) == [1000, 1999]

    # Test case 12: Negative numbers
    assert search_range([-10, -5, -5, -5, 0, 5], -5) == [1, 3]

    # Test alternative implementations
    assert search_range_boundary_template([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert search_range_boundary_template([5, 7, 7, 8, 8, 10], 6) == [-1, -1]

    # Test count function
    assert count_occurrences([5, 7, 7, 8, 8, 10], 8) == 2
    assert count_occurrences([5, 7, 7, 8, 8, 10], 6) == 0
    assert count_occurrences([5, 5, 5, 5], 5) == 4

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_search_range()

    # Visualize examples
    print("\n" + "="*60)
    print("VISUALIZATION EXAMPLES")
    print("="*60)

    print("\nExample 1: Multiple occurrences")
    print("-" * 60)
    visualize_search([5, 7, 7, 8, 8, 10], 8)

    print("\n" + "-" * 60)
    print("Example 2: All same elements")
    print("-" * 60)
    visualize_search([8, 8, 8, 8, 8], 8)

    print("\n" + "-" * 60)
    print("Example 3: Count occurrences")
    print("-" * 60)
    test_array = [1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5]
    print(f"Array: {test_array}")
    for target in range(1, 6):
        count = count_occurrences(test_array, target)
        range_result = search_range(test_array, target)
        print(f"  {target}: appears {count} times at {range_result}")
